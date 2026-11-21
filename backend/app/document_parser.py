"""Document Parser module for PDF and TXT technical documents.

Extracts text while strictly preserving 1-indexed page numbers, performs sentence-aware
chunking with configurable overlap, and handles encrypted or corrupted documents.
"""

import os
import re
from typing import List, Dict, Tuple, Optional
import pymupdf  # Modern PyMuPDF API

from .models.schemas import DocumentChunk

class DocumentParsingError(Exception):
    """Custom exception raised when document parsing fails."""
    pass

class DocumentParser:
    """Parses PDF and plain text documents into page-attributed chunks."""

    def __init__(self, chunk_size_chars: int = 1200, chunk_overlap_chars: int = 200):
        self.chunk_size_chars = chunk_size_chars
        self.chunk_overlap_chars = chunk_overlap_chars

    def parse_txt_file(self, file_path_or_text: str, is_raw_text: bool = False) -> Tuple[List[DocumentChunk], int, int]:
        """Parse raw text or a .txt file.

        Synthesizes logical pages based on page break markers or ~3,000 character logical pages.
        Returns: (chunks, page_count, word_count)
        """
        if is_raw_text:
            text = file_path_or_text
        else:
            if not os.path.exists(file_path_or_text):
                raise DocumentParsingError(f"File not found: {file_path_or_text}")
            try:
                with open(file_path_or_text, "r", encoding="utf-8", errors="replace") as f:
                    text = f.read()
            except Exception as e:
                raise DocumentParsingError(f"Failed to read TXT file: {str(e)}")

        if not text.strip():
            raise DocumentParsingError("Document is empty or contains no readable text.")

        # Check for explicit page break markers e.g. '--- Page 2 ---' or '\f' (formfeed)
        raw_pages = []
        if "\f" in text:
            raw_pages = text.split("\f")
        elif re.search(r"(?:-{3,}|\={3,})\s*(?:Page|\bP\.)\s*\d+\s*(?:-{3,}|\={3,})", text, re.IGNORECASE):
            raw_pages = re.split(r"(?:-{3,}|\={3,})\s*(?:Page|\bP\.)\s*\d+\s*(?:-{3,}|\={3,})", text, flags=re.IGNORECASE)
            # Remove any leading empty page from split
            raw_pages = [p for p in raw_pages if p.strip()]
        else:
            # Fallback: logical pages of ~2,500 characters
            target_page_len = 2500
            for i in range(0, len(text), target_page_len):
                raw_pages.append(text[i:i + target_page_len])

        chunks: List[DocumentChunk] = []
        total_word_count = len(re.findall(r"\b\w+\b", text))
        chunk_counter = 1

        for page_idx, page_str in enumerate(raw_pages, start=1):
            clean_page = page_str.strip()
            if not clean_page:
                continue

            # Split page into sentence-aware overlapping chunks if longer than chunk_size_chars
            page_chunks = self._chunk_page_text(clean_page, page_number=page_idx, start_counter=chunk_counter)
            chunks.extend(page_chunks)
            chunk_counter += len(page_chunks)

        if not chunks:
            # Single fallback chunk
            chunks.append(
                DocumentChunk(
                    chunk_id="chunk-1",
                    page_number=1,
                    text=text[:self.chunk_size_chars],
                    start_char=0,
                    end_char=len(text)
                )
            )

        return chunks, len(raw_pages), total_word_count

    def parse_pdf_bytes(self, pdf_bytes: bytes, filename: str = "document.pdf") -> Tuple[List[DocumentChunk], int, int]:
        """Parse PDF document from raw bytes using PyMuPDF (fitz).

        Strictly preserves 1-indexed physical page numbers.
        Returns: (chunks, page_count, word_count)
        """
        try:
            doc = pymupdf.open(stream=pdf_bytes, filetype="pdf")
        except Exception as e:
            raise DocumentParsingError(f"Failed to open PDF document: {str(e)}")

        page_count = len(doc)
        if page_count == 0:
            raise DocumentParsingError("PDF document contains 0 pages.")

        chunks: List[DocumentChunk] = []
        total_word_count = 0
        chunk_counter = 1

        for page_idx in range(page_count):
            page_number = page_idx + 1  # 1-indexed page
            page = doc[page_idx]

            # Extract clean layout-aware text
            try:
                page_text = page.get_text("text")
            except Exception:
                page_text = ""

            clean_text = page_text.strip()
            if not clean_text:
                # If text is empty, check for images or scanned content note
                clean_text = f"[Page {page_number} contains scanned imagery or unextracted graphical schematics]"

            page_words = len(re.findall(r"\b\w+\b", clean_text))
            total_word_count += page_words

            page_chunks = self._chunk_page_text(clean_text, page_number=page_number, start_counter=chunk_counter)
            chunks.extend(page_chunks)
            chunk_counter += len(page_chunks)

        doc.close()

        if not chunks:
            raise DocumentParsingError("No readable text chunks could be extracted from the PDF.")

        return chunks, page_count, total_word_count

    def parse_pdf_file(self, file_path: str) -> Tuple[List[DocumentChunk], int, int]:
        """Parse PDF document from a file path."""
        if not os.path.exists(file_path):
            raise DocumentParsingError(f"PDF file not found: {file_path}")
        with open(file_path, "rb") as f:
            pdf_bytes = f.read()
        return self.parse_pdf_bytes(pdf_bytes, filename=os.path.basename(file_path))

    def _chunk_page_text(self, text: str, page_number: int, start_counter: int) -> List[DocumentChunk]:
        """Split text of a single page into overlapping chunks respecting sentence boundaries."""
        if len(text) <= self.chunk_size_chars:
            return [
                DocumentChunk(
                    chunk_id=f"page-{page_number}-c{start_counter}",
                    page_number=page_number,
                    text=text,
                    start_char=0,
                    end_char=len(text)
                )
            ]

        # Break text on paragraph or sentence boundaries
        sentences = re.split(r"(?<=[.!?\n])\s+", text)
        # If no punctuation split occurred (e.g. continuous words), split by words
        if len(sentences) <= 1:
            words = text.split(" ")
            # Group words into blocks of ~chunk_size_chars
            sentences = []
            curr_words = []
            curr_len = 0
            for w in words:
                curr_words.append(w)
                curr_len += len(w) + 1
                if curr_len >= self.chunk_size_chars // 2:
                    sentences.append(" ".join(curr_words))
                    curr_words = []
                    curr_len = 0
            if curr_words:
                sentences.append(" ".join(curr_words))

        page_chunks: List[DocumentChunk] = []
        current_chunk_sentences: List[str] = []
        current_len = 0
        char_offset = 0

        for sentence in sentences:
            sentence_len = len(sentence)
            if current_len + sentence_len > self.chunk_size_chars and current_chunk_sentences:
                chunk_str = " ".join(current_chunk_sentences).strip()
                page_chunks.append(
                    DocumentChunk(
                        chunk_id=f"page-{page_number}-c{start_counter + len(page_chunks)}",
                        page_number=page_number,
                        text=chunk_str,
                        start_char=char_offset,
                        end_char=char_offset + len(chunk_str)
                    )
                )
                char_offset += len(chunk_str)

                # Keep last sentence for overlap
                overlap_sentences = current_chunk_sentences[-1:] if len(current_chunk_sentences) > 1 else []
                current_chunk_sentences = overlap_sentences + [sentence]
                current_len = sum(len(s) for s in current_chunk_sentences)
            else:
                current_chunk_sentences.append(sentence)
                current_len += sentence_len

        if current_chunk_sentences:
            chunk_str = " ".join(current_chunk_sentences).strip()
            page_chunks.append(
                DocumentChunk(
                    chunk_id=f"page-{page_number}-c{start_counter + len(page_chunks)}",
                    page_number=page_number,
                    text=chunk_str,
                    start_char=char_offset,
                    end_char=char_offset + len(chunk_str)
                )
            )

        return page_chunks
