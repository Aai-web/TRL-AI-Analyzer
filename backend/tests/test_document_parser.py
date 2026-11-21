"""Tests for Document Parser (PDF & TXT)."""

import unittest
from backend.app.document_parser import DocumentParser, DocumentParsingError

class TestDocumentParser(unittest.TestCase):

    def setUp(self):
        self.parser = DocumentParser(chunk_size_chars=400, chunk_overlap_chars=80)

    def test_parse_multi_page_txt(self):
        sample_txt = (
            "--- Page 1 ---\n"
            "This is the first page of the technical report detailing initial basic research hypotheses.\n"
            "Fundamental governing physics were observed.\n"
            "--- Page 2 ---\n"
            "This is the second page discussing laboratory benchtop experiments and verified measurements.\n"
            "--- Page 3 ---\n"
            "This is the third page discussing future flight tests and operational deployment plans.\n"
        )
        chunks, page_count, word_count = self.parser.parse_txt_file(sample_txt, is_raw_text=True)

        self.assertEqual(page_count, 3)
        self.assertGreater(len(chunks), 0)
        self.assertGreater(word_count, 15)

        # Check page numbers
        pages_present = {c.page_number for c in chunks}
        self.assertIn(1, pages_present)
        self.assertIn(2, pages_present)
        self.assertIn(3, pages_present)

    def test_empty_document_raises_error(self):
        with self.assertRaises(DocumentParsingError):
            self.parser.parse_txt_file("   ", is_raw_text=True)

    def test_chunking_overlap(self):
        long_text = "Word " * 200  # ~1000 characters
        chunks, _, _ = self.parser.parse_txt_file(long_text, is_raw_text=True)
        self.assertGreater(len(chunks), 1)

if __name__ == "__main__":
    unittest.main()
