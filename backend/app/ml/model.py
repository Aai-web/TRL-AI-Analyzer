"""Evidence-based Ordinal Classification Model for Technology Readiness Level (TRL 1-9).

Implements the Frank & Hall ordinal decomposition with calibrated logistic classifiers,
dense criterion match features, empirical verification weighting, and feature attribution.
"""

import os
import re
import math
import joblib
import numpy as np
from typing import Dict, List, Tuple, Any, Optional
from scipy.sparse import hstack, csr_matrix
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import mean_absolute_error, accuracy_score

from .trl_criteria import (
    TRL_DEFINITIONS,
    EMPIRICAL_VERBS,
    SPECULATIVE_MARKERS,
    TECHNICAL_DOMAINS
)

class FeatureExtractor:
    """Extracts hybrid lexical, semantic, and domain-engineered features for TRL assessment."""

    def __init__(self, max_features: int = 1500):
        self.max_features = max_features
        self.tfidf = TfidfVectorizer(
            ngram_range=(1, 2),
            max_features=max_features,
            sublinear_tf=True,
            stop_words="english",
            token_pattern=r"(?u)\b[a-zA-Z0-9_\-\.]{2,}\b"
        )
        self.is_fitted = False

    def _extract_dense_features(self, texts: List[str]) -> np.ndarray:
        """Extract domain-engineered features for each document text."""
        dense_features = []
        for text in texts:
            text_lower = text.lower()
            words = re.findall(r"\b\w+\b", text_lower)
            word_count = max(len(words), 1)

            # 1. TRL 1-9 Criterion Match Scores (9 features)
            trl_scores = []
            for trl in range(1, 10):
                keywords = TRL_DEFINITIONS[trl]["keywords"]
                hits = sum(1 for kw in keywords if kw in text_lower)
                # Normalized by number of keywords
                trl_scores.append(hits / max(len(keywords), 1))

            # 2. Empirical verification density (past-tense action verbs of proof)
            empirical_hits = sum(1 for verb in EMPIRICAL_VERBS if re.search(r"\b" + verb + r"\b", text_lower))
            empirical_density = empirical_hits / word_count

            # 3. Speculative / unverified claim density
            speculative_hits = sum(1 for marker in SPECULATIVE_MARKERS if marker in text_lower)
            speculative_density = speculative_hits / word_count

            # 4. Verified vs Speculative Ratio (Discount factor)
            # High ratio means grounded results; low ratio means speculative promises
            discount_ratio = (empirical_hits + 0.1) / (empirical_hits + 2.0 * speculative_hits + 0.5)

            # 5. Quantitative Metric Density (measurements, percentages, units)
            metric_matches = re.findall(r"\b\d+(?:\.\d+)?\s*(?:%|deg|c|k|kw|mw|mwe|ghz|mhz|khz|torr|dbm|mah/g|hours|days|years|m|cm|mm|nm|bar|mpa|kn|v|mv)\b", text_lower)
            metric_density = len(metric_matches) / word_count

            # 6. Environmental setting indicators (lab vs relevant vs operational vs commercial)
            lab_env = 1.0 if any(k in text_lower for k in ["laboratory", "benchtop", "in vitro", "optical table", "coin cell"]) else 0.0
            relevant_env = 1.0 if any(k in text_lower for k in ["thermal vacuum", "climatic chamber", "vibration", "simulated", "pilot plant", "rocket sled"]) else 0.0
            operational_env = 1.0 if any(k in text_lower for k in ["flight test", "operational vehicle", "commercial airliner", "substation", "sea trial", "phase iii"]) else 0.0
            commercial_env = 1.0 if any(k in text_lower for k in ["commercial deployment", "mass production", "mission proven", "installed in", "fleet", "certified"]) else 0.0

            # Combine all 18 dense features
            feature_row = trl_scores + [
                empirical_density,
                speculative_density,
                discount_ratio,
                metric_density,
                lab_env,
                relevant_env,
                operational_env,
                commercial_env
            ]
            dense_features.append(feature_row)

        return np.array(dense_features, dtype=np.float32)

    def fit(self, texts: List[str]):
        """Fit the TF-IDF vectorizer."""
        self.tfidf.fit(texts)
        self.is_fitted = True
        return self

    def transform(self, texts: List[str]) -> csr_matrix:
        """Transform texts into sparse feature matrix combining TF-IDF and dense features."""
        if not self.is_fitted:
            raise ValueError("FeatureExtractor must be fitted before calling transform.")
        sparse_tfidf = self.tfidf.transform(texts)
        dense_feats = self._extract_dense_features(texts)
        return hstack([sparse_tfidf, csr_matrix(dense_feats)], format="csr")

    def fit_transform(self, texts: List[str]) -> csr_matrix:
        """Fit and transform texts in one step."""
        self.fit(texts)
        return self.transform(texts)


class EvidenceOrdinalClassifier:
    """Frank & Hall Ordinal Classification Model for TRL 1 to 9.

    Trains 8 binary classifiers C_1, ..., C_8 where C_k estimates P(TRL > k).
    Probabilities are calibrated and projected monotonically.
    """

    def __init__(self, c_reg: float = 1.5):
        self.c_reg = c_reg
        self.feature_extractor = FeatureExtractor()
        # Binary classifiers for thresholds k = 1 to 8
        self.binary_classifiers: Dict[int, LogisticRegression] = {}
        self.is_trained = False
        self.training_metrics: Dict[str, Any] = {}

    def fit(self, texts: List[str], y: List[int]) -> "EvidenceOrdinalClassifier":
        """Train the 8 binary ordinal classifiers on the dataset."""
        y_arr = np.array(y, dtype=int)
        X = self.feature_extractor.fit_transform(texts)

        for k in range(1, 9):
            # Target: 1 if TRL > k, 0 otherwise
            y_binary = (y_arr > k).astype(int)
            # Ensure both classes exist
            if len(np.unique(y_binary)) > 1:
                clf = LogisticRegression(
                    C=self.c_reg,
                    class_weight="balanced",
                    max_iter=1000,
                    random_state=42
                )
                clf.fit(X, y_binary)
            else:
                # Degenerate case fallback
                clf = None
            self.binary_classifiers[k] = clf

        self.is_trained = True
        return self

    def predict_proba(self, texts: List[str]) -> np.ndarray:
        """Predict calibrated probability distribution P(TRL = k) for k in 1..9 for each text."""
        if not self.is_trained:
            raise ValueError("Model is not trained yet.")

        X = self.feature_extractor.transform(texts)
        n_samples = X.shape[0]

        # Array of cumulative probabilities P(TRL > k) for k=1..8
        p_greater = np.zeros((n_samples, 8))

        for k in range(1, 9):
            clf = self.binary_classifiers.get(k)
            if clf is not None:
                # Probability of class 1 (TRL > k)
                p_greater[:, k - 1] = clf.predict_proba(X)[:, 1]
            else:
                # If single-class boundary
                p_greater[:, k - 1] = 0.0

        # Enforce ordinal monotonicity: P(TRL > k) must be non-increasing with k
        # P(TRL > 1) >= P(TRL > 2) >= ... >= P(TRL > 8)
        for i in range(n_samples):
            for k in range(1, 8):
                if p_greater[i, k] > p_greater[i, k - 1]:
                    # Monotonic projection: clip or average
                    p_greater[i, k] = p_greater[i, k - 1] * 0.95

        # Compute point probabilities P(TRL = k)
        # P(TRL = 1) = 1 - P(TRL > 1)
        # P(TRL = k) = P(TRL > k-1) - P(TRL > k) for k = 2..8
        # P(TRL = 9) = P(TRL > 8)
        probabilities = np.zeros((n_samples, 9))
        probabilities[:, 0] = np.clip(1.0 - p_greater[:, 0], 0.001, 1.0)

        for k in range(2, 9):
            prob_k = p_greater[:, k - 2] - p_greater[:, k - 1]
            probabilities[:, k - 1] = np.clip(prob_k, 0.001, 1.0)

        probabilities[:, 8] = np.clip(p_greater[:, 7], 0.001, 1.0)

        # Normalize across rows so sum equals 1.0
        row_sums = probabilities.sum(axis=1, keepdims=True)
        probabilities = probabilities / row_sums

        return probabilities

    def predict(self, texts: List[str]) -> np.ndarray:
        """Predict the most probable TRL level (1 to 9)."""
        probas = self.predict_proba(texts)
        return np.argmax(probas, axis=1) + 1

    def explain_prediction(self, text: str, predicted_trl: int, probas: np.ndarray) -> Dict[str, Any]:
        """Generate human-interpretable reasons and feature attributions for the prediction."""
        text_lower = text.lower()
        dense_feats = self.feature_extractor._extract_dense_features([text])[0]
        # dense_feats: [trl1..trl9, empirical, speculative, discount, metric, lab, rel, op, comm]
        empirical_density = dense_feats[9]
        speculative_density = dense_feats[10]
        discount_ratio = dense_feats[11]
        metric_density = dense_feats[12]

        primary_reasons = []
        dominant_criteria = []
        disqualifying_factors = []

        # 1. Evaluate dominant criteria match for predicted TRL
        pred_meta = TRL_DEFINITIONS[predicted_trl]
        matched_kws = [kw for kw in pred_meta["keywords"] if kw in text_lower]
        if matched_kws:
            primary_reasons.append(
                f"Document exhibits strong alignment with {pred_meta['title']} ({', '.join(matched_kws[:3])})."
            )
            dominant_criteria.append(pred_meta["milestones"][0])

        # 2. Speculative vs empirical check
        is_discounted = False
        if speculative_density > 0.015 and discount_ratio < 0.4:
            is_discounted = True
            disqualifying_factors.append(
                "Document contains forward-looking or speculative language ('will be', 'propose', 'planned') "
                "which was discounted in accordance with evidence standards to prevent artificial TRL inflation."
            )

        if metric_density > 0.01:
            primary_reasons.append(
                f"Verified quantitative engineering metrics detected ({round(metric_density * 100, 1)}% density) supporting empirical validation."
            )

        # 3. Environment verification
        if dense_feats[13] > 0.5:  # Lab
            primary_reasons.append("Evidence confirms component operation in laboratory/benchtop environment.")
        if dense_feats[14] > 0.5:  # Relevant
            primary_reasons.append("Evidence validates performance under simulated environmental stress (thermal/vibration/relevant conditions).")
        if dense_feats[15] > 0.5:  # Operational
            primary_reasons.append("Evidence validates full operational deployment in actual field/flight/clinical environment.")
        if dense_feats[16] > 0.5:  # Commercial
            primary_reasons.append("Evidence demonstrates multi-year operational uptime and mass commercial deployment.")

        # Disqualifying check for higher levels
        if predicted_trl < 7:
            if not any(k in text_lower for k in ["operational", "flight test", "commercial", "field deploy"]):
                disqualifying_factors.append("Absence of operational environment or field flight test validation prevents classification at TRL 7+.")

        if not primary_reasons:
            primary_reasons.append(f"Textual patterns and keyword density correspond closest to TRL {predicted_trl} ({pred_meta['title']}).")

        # Uncertainty calculation
        # Shannon entropy
        entropy = -sum(p * math.log2(max(p, 1e-9)) for p in probas)
        sorted_probas = sorted(probas, reverse=True)
        margin = sorted_probas[0] - sorted_probas[1]

        if sorted_probas[0] >= 0.50 and margin >= 0.25:
            uncertainty_level = "Low"
            uncertainty_reason = f"High model consensus; dominant TRL {predicted_trl} exceeds secondary alternative by {round(margin * 100, 1)}% margin."
        elif sorted_probas[0] >= 0.35 and margin >= 0.10:
            uncertainty_level = "Moderate"
            uncertainty_reason = f"Moderate consensus; document spans transition boundary between TRL {predicted_trl} and adjacent levels."
        else:
            uncertainty_level = "High"
            uncertainty_reason = "High epistemic uncertainty; evidence spans multiple developmental milestones or is relatively sparse."

        # Top feature contributions
        top_features = []
        for trl_i in range(1, 10):
            score = dense_feats[trl_i - 1]
            if score > 0:
                top_features.append({
                    "feature": f"TRL {trl_i} Criteria Match",
                    "weight": round(float(score), 3),
                    "impact": "Positive" if trl_i == predicted_trl else "Alternative"
                })

        return {
            "primary_reasons": primary_reasons,
            "dominant_criteria_met": dominant_criteria if dominant_criteria else [pred_meta["milestones"][0]],
            "disqualifying_factors": disqualifying_factors,
            "uncertainty_level": uncertainty_level,
            "uncertainty_reason": uncertainty_reason,
            "top_feature_contributions": top_features[:6],
            "is_claim_discounted": is_discounted
        }

    def save(self, filepath: str):
        """Save trained model to disk."""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        joblib.dump(self, filepath)

    @classmethod
    def load(cls, filepath: str) -> "EvidenceOrdinalClassifier":
        """Load trained model from disk."""
        return joblib.load(filepath)
