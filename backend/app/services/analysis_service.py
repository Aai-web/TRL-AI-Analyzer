"""Core Orchestration Service for Document TRL Analysis.

Connects document parsing, evidence-based ordinal classification,
evidence extraction, gap analysis, and document history management.
"""

import os
import re
import uuid
from typing import List, Dict, Optional, Any
from datetime import datetime, timezone

from ..models.schemas import (
    DocumentChunk,
    EvidenceItem,
    TRLAlternative,
    ModelExplanation,
    TRLPredictionResult,
    DocumentAnalysisResponse,
    SampleDocumentInfo
)
from ..ml.trl_criteria import TRL_DEFINITIONS, TECHNICAL_DOMAINS
from ..ml.model import EvidenceOrdinalClassifier
from ..ml.evidence_extractor import EvidenceExtractor
from ..ml.gap_analyzer import GapAnalyzer
from ..ml.train import MODEL_PATH, train_and_evaluate

class AnalysisService:
    """Singleton service orchestrating ML inference and evidence analysis."""

    def __init__(self):
        self.evidence_extractor = EvidenceExtractor()
        self.gap_analyzer = GapAnalyzer()
        self.classifier: Optional[EvidenceOrdinalClassifier] = None
        self.history: List[DocumentAnalysisResponse] = []
        self._load_or_train_model()

    def _load_or_train_model(self):
        """Load pre-trained model or train on the benchmark dataset if weights are missing."""
        if os.path.exists(MODEL_PATH):
            try:
                self.classifier = EvidenceOrdinalClassifier.load(MODEL_PATH)
                print(f"Loaded existing TRL classifier from {MODEL_PATH}")
                return
            except Exception as e:
                print(f"Failed to load weights ({e}). Retraining...")

        # Train baseline model
        print("Training Frank & Hall Ordinal Classifier...")
        train_and_evaluate(save_artifacts=True)
        self.classifier = EvidenceOrdinalClassifier.load(MODEL_PATH)

    def _infer_technical_domain(self, text: str) -> str:
        """Infer the engineering or scientific domain from document vocabulary."""
        text_lower = text.lower()
        domain_keywords = {
            "Aerospace & Defence": ["flight", "scramjet", "hypersonic", "aerospace", "orbit", "cubesat", "spacecraft", "aircraft", "propulsion"],
            "Energy & Clean Tech": ["battery", "fuel cell", "solar", "photovoltaic", "energy storage", "co2 capture", "wind turbine", "inverter"],
            "Biomedical & Pharmaceuticals": ["in vitro", "clinical trial", "insulin", "biocompatibility", "perfusion", "cellular", "neural decoder", "macaques"],
            "Advanced Materials & Nanotechnology": ["graphene", "borophene", "nanocomposite", "polymer", "epoxy", "spectroscopic", "thin film"],
            "Electronics & Semiconductors": ["radar", "transceiver", "mmic", "inverter module", "sic", "silicon carbide", "die", "integrated circuit"],
            "Robotics & Autonomous Systems": ["gripper", "autonomous", "slam", "lidar", "submersible", "actuator", "motor", "robotic"],
            "Information Technology & AI": ["transformer", "speech-to-text", "optical logic", "inference engine", "cloud", "api", "neural network"],
            "Chemical Engineering": ["catalyst", "reactor", "synthesis", "adsorption", "chemical", "sorbent", "yield"]
        }

        best_domain = "Applied Science & Engineering"
        max_matches = 0

        for domain, keywords in domain_keywords.items():
            matches = sum(1 for kw in keywords if kw in text_lower)
            if matches > max_matches:
                max_matches = matches
                best_domain = domain

        return best_domain

    def analyze_document(
        self,
        chunks: List[DocumentChunk],
        filename: str,
        file_type: str,
        page_count: int,
        word_count: int
    ) -> DocumentAnalysisResponse:
        """Execute complete TRL assessment on document chunks."""
        # 1. Combine full text for global lexical/dense features
        full_text = "\n\n".join(chunk.text for chunk in chunks)
        char_count = len(full_text)

        # 2. ML Prediction using Ordinal Classifier
        if self.classifier is None:
            self._load_or_train_model()

        probas_matrix = self.classifier.predict_proba([full_text])
        probas = probas_matrix[0]  # Array of 9 probabilities for TRL 1..9

        predicted_trl = int(self.classifier.predict([full_text])[0])
        calibrated_conf = float(probas[predicted_trl - 1])

        # Confidence tier
        if calibrated_conf >= 0.50:
            confidence_tier = "High"
        elif calibrated_conf >= 0.30:
            confidence_tier = "Moderate"
        else:
            confidence_tier = "Preliminary"

        # Probability distribution dict {1: p1, ..., 9: p9}
        prob_dist = {trl: round(float(probas[trl - 1]), 4) for trl in range(1, 10)}

        # Alternative TRLs sorted by probability (excluding the predicted level)
        sorted_indices = sorted(range(9), key=lambda i: probas[i], reverse=True)
        alternatives: List[TRLAlternative] = []
        for idx in sorted_indices:
            trl_lvl = idx + 1
            if trl_lvl != predicted_trl and probas[idx] > 0.05:
                alternatives.append(
                    TRLAlternative(
                        trl=trl_lvl,
                        probability=round(float(probas[idx]), 4),
                        description=TRL_DEFINITIONS[trl_lvl]["title"]
                    )
                )

        # 3. Evidence Extraction
        evidence_items = self.evidence_extractor.extract_evidence(
            chunks=chunks,
            predicted_trl=predicted_trl,
            max_items_per_trl=4
        )

        # Counts by TRL
        evidence_counts = {trl: 0 for trl in range(1, 10)}
        for item in evidence_items:
            evidence_counts[item.trl_level] += 1

        # 4. Model Decision Explanations
        explanation_dict = self.classifier.explain_prediction(full_text, predicted_trl, probas)
        model_explanation = ModelExplanation(**explanation_dict)

        # 5. Gap Analysis and Prioritized Roadmap
        gap_requirements, next_barriers, roadmap = self.gap_analyzer.analyze_gaps(
            predicted_trl=predicted_trl,
            evidence_items=evidence_items,
            doc_text=full_text
        )

        missing_count = sum(1 for g in gap_requirements if g.status == "Missing")

        # 6. Technical Domain & Summary
        domain = self._infer_technical_domain(full_text)
        current_meta = TRL_DEFINITIONS[predicted_trl]
        summary = (
            f"The analyzed {domain.lower()} document corresponds to Technology Readiness Level {predicted_trl} "
            f"({current_meta['title']}) with a calibrated model confidence of {round(calibrated_conf * 100, 1)}%. "
            f"{len(evidence_items)} verifiable evidence statements were extracted across {page_count} pages. "
            f"Advancement to TRL {min(9, predicted_trl + 1)} is currently constrained by {len(next_barriers)} milestone gate(s)."
        )

        prediction_result = TRLPredictionResult(
            predicted_trl=predicted_trl,
            trl_title=current_meta["title"],
            trl_definition=current_meta["definition"],
            calibrated_confidence=round(calibrated_conf, 4),
            confidence_tier=confidence_tier,
            probability_distribution=prob_dist,
            alternatives=alternatives[:3],
            evidence_items=evidence_items,
            evidence_counts_by_trl=evidence_counts,
            gap_analysis=gap_requirements,
            missing_criteria_count=missing_count,
            next_trl_barriers=next_barriers,
            roadmap=roadmap,
            model_explanation=model_explanation,
            meta={"domain": domain}
        )

        doc_id = f"DOC-{uuid.uuid4().hex[:8].upper()}"
        analysis_response = DocumentAnalysisResponse(
            document_id=doc_id,
            filename=filename,
            file_type=file_type,
            page_count=page_count,
            word_count=word_count,
            char_count=char_count,
            processed_at=datetime.now(timezone.utc),
            prediction=prediction_result,
            summary=summary,
            technical_domain=domain
        )

        # Prepend to history (keep up to 25 items)
        self.history.insert(0, analysis_response)
        if len(self.history) > 25:
            self.history = self.history[:25]

        return analysis_response

    def get_history(self) -> List[DocumentAnalysisResponse]:
        """Return history of analyzed documents in current session."""
        return self.history

    def get_analysis_by_id(self, document_id: str) -> Optional[DocumentAnalysisResponse]:
        """Retrieve a specific assessment by document ID."""
        for item in self.history:
            if item.document_id == document_id:
                return item
        return None
