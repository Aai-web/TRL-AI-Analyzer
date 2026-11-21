"""High-precision Evidence Extraction Engine for Technology Readiness Assessment.

Extracts exact verbatim statements from document chunks with precise page numbers,
classifies evidence strength (Strong, Moderate, Weak), detects speculative claims vs verified results,
and links each evidence item to standardized TRL criteria.
"""

import re
import uuid
from typing import List, Dict, Any, Optional

from ..models.schemas import DocumentChunk, EvidenceItem, EvidenceStrength
from .trl_criteria import (
    TRL_DEFINITIONS,
    EMPIRICAL_VERBS,
    SPECULATIVE_MARKERS
)

class EvidenceExtractor:
    """Extracts, categorizes, and verifies evidence items from segmented document chunks."""

    def __init__(self):
        # Compiled regex patterns for speed and precision
        self.metric_regex = re.compile(
            r"\b\d+(?:\.\d+)?\s*(?:%|deg\s*c|k|kw|mw|mwe|ghz|mhz|khz|torr|dbm|mah/g|cycles|hours|days|weeks|months|years|m|cm|mm|nm|bar|mpa|kn|v|mv|db)\b",
            re.IGNORECASE
        )
        self.empirical_regex = re.compile(
            r"\b(?:" + "|".join(EMPIRICAL_VERBS) + r")\b",
            re.IGNORECASE
        )
        self.speculative_regex = re.compile(
            r"\b(?:" + "|".join(re.escape(m) for m in SPECULATIVE_MARKERS) + r")\b",
            re.IGNORECASE
        )

    def _split_into_sentences(self, text: str) -> List[str]:
        """Split text into individual sentences while preserving punctuation."""
        # Clean multi-newlines and normalize spaces
        clean_text = re.sub(r"\s+", " ", text).strip()
        if not clean_text:
            return []
        # Split on sentence boundaries (. ! ?) followed by whitespace and capital letter or end
        sentences = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9])", clean_text)
        # Filter out trivially short fragments
        return [s.strip() for s in sentences if len(s.strip()) > 25]

    def extract_evidence(
        self,
        chunks: List[DocumentChunk],
        predicted_trl: Optional[int] = None,
        max_items_per_trl: int = 4
    ) -> List[EvidenceItem]:
        """Extract exact evidence items with page numbers across all document chunks."""
        extracted_items: List[EvidenceItem] = []
        seen_quotes = set()

        # Iterate over all document chunks preserving page number
        for chunk in chunks:
            page_num = chunk.page_number
            sentences = self._split_into_sentences(chunk.text)

            for sentence in sentences:
                sentence_lower = sentence.lower()

                # Evaluate sentence against each TRL level (1 to 9)
                for trl in range(1, 10):
                    meta = TRL_DEFINITIONS[trl]
                    keywords = meta["keywords"]

                    # Count keyword hits for this TRL
                    matched_kws = [kw for kw in keywords if kw in sentence_lower]
                    if not matched_kws:
                        continue

                    # Clean quote for deduplication
                    norm_quote = re.sub(r"\s+", " ", sentence).strip()
                    if norm_quote in seen_quotes:
                        continue

                    # Analyze verification characteristics
                    has_metrics = bool(self.metric_regex.search(sentence_lower))
                    has_empirical = bool(self.empirical_regex.search(sentence_lower))
                    has_speculative = bool(self.speculative_regex.search(sentence_lower))

                    # Determine evidence strength, verification status, and confidence
                    if has_speculative and not has_empirical:
                        strength = "Weak"
                        status = "Unverified Claim"
                        base_confidence = 0.45
                        reasoning = (
                            f"Contains prospective or speculative wording ({self.speculative_regex.search(sentence_lower).group()}); "
                            f"identifies planned intent rather than empirical verification for {meta['title']}."
                        )
                    elif has_empirical and has_metrics:
                        strength = "Strong"
                        status = "Verified Result"
                        base_confidence = 0.92
                        reasoning = (
                            f"Direct empirical validation with quantitative performance metrics "
                            f"demonstrating {matched_kws[0]} milestone."
                        )
                    elif has_empirical:
                        strength = "Moderate"
                        status = "Empirical Observation"
                        base_confidence = 0.74
                        reasoning = (
                            f"Empirical observation confirming practical execution of {matched_kws[0]} "
                            f"under laboratory or test conditions."
                        )
                    else:
                        strength = "Moderate" if len(matched_kws) >= 2 else "Weak"
                        status = "Preliminary Validation"
                        base_confidence = 0.62 if strength == "Moderate" else 0.48
                        reasoning = (
                            f"Describes technical architecture and criteria corresponding to {matched_kws[0]}."
                        )

                    # Boost confidence if it matches the predicted TRL
                    if predicted_trl and trl == predicted_trl:
                        base_confidence = min(0.98, base_confidence + 0.05)

                    criterion_name = f"TRL {trl}: {meta['milestones'][0]}"
                    item = EvidenceItem(
                        evidence_id=f"EV-{trl}-{uuid.uuid4().hex[:6]}",
                        trl_level=trl,
                        criterion_name=criterion_name,
                        quote=norm_quote,
                        page_number=page_num,
                        strength=strength,
                        confidence_score=round(base_confidence, 2),
                        verification_status=status,
                        reasoning=reasoning
                    )

                    extracted_items.append(item)
                    seen_quotes.add(norm_quote)

        # Sort evidence: first by predicted TRL (if given), then by strength (Strong > Moderate > Weak), then confidence
        strength_rank = {"Strong": 3, "Moderate": 2, "Weak": 1}

        def sort_key(item: EvidenceItem):
            is_pred = 1 if (predicted_trl and item.trl_level == predicted_trl) else 0
            return (is_pred, strength_rank.get(item.strength, 0), item.confidence_score)

        extracted_items.sort(key=sort_key, reverse=True)

        # Limit per TRL level to provide a balanced, high-signal evidence portfolio
        grouped_by_trl: Dict[int, List[EvidenceItem]] = {}
        for item in extracted_items:
            grouped_by_trl.setdefault(item.trl_level, []).append(item)

        balanced_items: List[EvidenceItem] = []
        for trl, items in grouped_by_trl.items():
            balanced_items.extend(items[:max_items_per_trl])

        # Final sort by TRL level and strength
        balanced_items.sort(key=lambda x: (x.trl_level, -strength_rank.get(x.strength, 0)))
        return balanced_items
