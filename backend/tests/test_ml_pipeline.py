"""Tests for ML pipeline, Frank & Hall ordinal classification, evidence extractor, and gap analyzer."""

import unittest
import numpy as np
from backend.app.ml.dataset import get_dataset
from backend.app.ml.model import EvidenceOrdinalClassifier, FeatureExtractor
from backend.app.ml.evidence_extractor import EvidenceExtractor
from backend.app.ml.gap_analyzer import GapAnalyzer
from backend.app.models.schemas import DocumentChunk

class TestMLPipeline(unittest.TestCase):

    def setUp(self):
        self.train_samples = get_dataset("train")
        self.texts = [s["text"] for s in self.train_samples]
        self.labels = [s["trl"] for s in self.train_samples]

    def test_feature_extractor(self):
        fe = FeatureExtractor(max_features=500)
        X = fe.fit_transform(self.texts)
        self.assertEqual(X.shape[0], len(self.texts))
        self.assertGreater(X.shape[1], 18)  # TF-IDF + 18 dense features

    def test_ordinal_classifier_training_and_monotonicity(self):
        clf = EvidenceOrdinalClassifier()
        clf.fit(self.texts, self.labels)
        self.assertTrue(clf.is_trained)

        # Predict probabilities on training set
        probas = clf.predict_proba(self.texts)
        self.assertEqual(probas.shape, (len(self.texts), 9))

        # Check probability axioms: all non-negative and row sum == 1.0
        for i in range(len(self.texts)):
            row = probas[i]
            self.assertTrue(np.all(row >= 0.0))
            self.assertAlmostEqual(float(np.sum(row)), 1.0, places=4)

        # Predictions in [1, 9]
        preds = clf.predict(self.texts)
        self.assertTrue(all(1 <= p <= 9 for p in preds))

    def test_evidence_extractor_categorization(self):
        extractor = EvidenceExtractor()
        chunks = [
            DocumentChunk(
                chunk_id="c1",
                page_number=1,
                text="The 5 kW prototype was tested in an environmental chamber at -40 deg C for 500 hours with 98% efficiency."
            ),
            DocumentChunk(
                chunk_id="c2",
                page_number=2,
                text="Future work will be planned to test the system in an operational vehicle next quarter."
            )
        ]
        evidence = extractor.extract_evidence(chunks, predicted_trl=5)
        self.assertGreater(len(evidence), 0)

        # First chunk has empirical verbs & metrics -> should be Strong or Moderate
        strong_or_mod = [e for e in evidence if e.page_number == 1]
        self.assertTrue(any(e.strength in ["Strong", "Moderate"] for e in strong_or_mod))

        # Second chunk has speculative markers -> should be marked Weak or Unverified Claim
        speculative_items = [e for e in evidence if e.page_number == 2]
        if speculative_items:
            self.assertEqual(speculative_items[0].strength, "Weak")

    def test_gap_analyzer(self):
        analyzer = GapAnalyzer()
        gaps, barriers, roadmap = analyzer.analyze_gaps(
            predicted_trl=4,
            evidence_items=[],
            doc_text="Integrated breadboard tested in laboratory benchtop environment."
        )
        self.assertGreater(len(gaps), 0)
        self.assertGreater(len(barriers), 0)
        self.assertEqual(len(roadmap), 3)
        self.assertEqual(roadmap[0].target_trl, 4)
        self.assertEqual(roadmap[1].target_trl, 5)

if __name__ == "__main__":
    unittest.main()
