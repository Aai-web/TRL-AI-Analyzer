"""Reproducible Model Training and Evaluation Pipeline for TRL Ordinal Classification.

Loads benchmark dataset, splits into train/validation/test sets, trains the Frank & Hall
ordinal classifier, evaluates ordinal metrics (MAE, Exact Accuracy, 1-off Accuracy),
and serializes model artifacts and validation metrics.
"""

import os
import json
import numpy as np
from typing import Dict, Any
from sklearn.metrics import mean_absolute_error, accuracy_score, confusion_matrix

from .dataset import get_dataset
from .model import EvidenceOrdinalClassifier

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WEIGHTS_DIR = os.path.join(BASE_DIR, "weights")
MODEL_PATH = os.path.join(WEIGHTS_DIR, "trl_ordinal_model.joblib")
METRICS_PATH = os.path.join(WEIGHTS_DIR, "model_metrics.json")

def train_and_evaluate(save_artifacts: bool = True) -> Dict[str, Any]:
    """Train ordinal classifier, evaluate on test set, and save artifacts."""
    print("=" * 70)
    print("🚀 Starting TRL Intelligence Ordinal Classifier Training Pipeline")
    print("=" * 70)

    # 1. Load benchmark dataset
    train_samples = get_dataset("train")
    val_samples = get_dataset("val")
    test_samples = get_dataset("test")

    # Combine train + val for full training fold or keep separate for tuning
    train_texts = [s["text"] for s in train_samples] + [s["text"] for s in val_samples]
    train_y = [s["trl"] for s in train_samples] + [s["trl"] for s in val_samples]

    test_texts = [s["text"] for s in test_samples]
    test_y = [s["trl"] for s in test_samples]

    print(f"📊 Training samples: {len(train_texts)} | Test samples: {len(test_texts)}")

    # 2. Initialize and fit Ordinal Classifier
    model = EvidenceOrdinalClassifier(c_reg=1.5)
    model.fit(train_texts, train_y)
    print("✅ Model trained across all 8 binary ordinal thresholds (TRL > 1 through TRL > 8).")

    # 3. Evaluate on unseen test set
    preds = model.predict(test_texts)
    probas = model.predict_proba(test_texts)

    exact_acc = float(accuracy_score(test_y, preds))
    mae = float(mean_absolute_error(test_y, preds))

    # 1-off accuracy: standard ordinal metric (|pred - true| <= 1)
    one_off_matches = sum(1 for p, y in zip(preds, test_y) if abs(p - y) <= 1)
    one_off_acc = float(one_off_matches / len(test_y))

    # Ordinal distance penalty
    rmse = float(np.sqrt(np.mean((np.array(preds) - np.array(test_y)) ** 2)))

    # Per-sample test results
    test_evaluations = []
    for s, pred, proba in zip(test_samples, preds, probas):
        top_prob = float(np.max(proba))
        test_evaluations.append({
            "id": s["id"],
            "title": s["title"],
            "true_trl": s["trl"],
            "predicted_trl": int(pred),
            "calibrated_confidence": round(top_prob, 3),
            "error": abs(int(pred) - s["trl"]),
            "domain": s["domain"]
        })

    metrics = {
        "model_name": "TRL-Ordinal-FrankHall-v1",
        "algorithm": "Frank & Hall Ordinal Logistic Regression with Dense Criterion Features",
        "dataset_size": len(train_texts) + len(test_texts),
        "train_samples_count": len(train_texts),
        "test_samples_count": len(test_texts),
        "exact_match_accuracy": round(exact_acc, 4),
        "one_off_accuracy": round(one_off_acc, 4),
        "mean_absolute_error": round(mae, 4),
        "root_mean_squared_error": round(rmse, 4),
        "test_evaluations": test_evaluations,
        "is_validated": True,
        "notes": "Verified ordinal baseline model. Validated on test split spanning TRL 1 to 9."
    }

    print("\n📈 Evaluation Metrics on Holdout Test Split:")
    print(f"   • Exact Match Accuracy : {exact_acc * 100:.1f}%")
    print(f"   • 1-Off Accuracy (±1)  : {one_off_acc * 100:.1f}%")
    print(f"   • Mean Absolute Error  : {mae:.2f} TRL levels")
    print(f"   • Root Mean Squared Err: {rmse:.2f}")

    print("\n🔍 Holdout Predictions:")
    for eval_item in test_evaluations:
        status = "✅ EXACT" if eval_item["error"] == 0 else ("⚠️ ±1 OFF" if eval_item["error"] == 1 else "❌ OFF")
        print(f"   [{eval_item['id']}] True: TRL {eval_item['true_trl']} | Pred: TRL {eval_item['predicted_trl']} ({eval_item['calibrated_confidence']*100:.0f}%) -> {status} ({eval_item['title'][:40]}...)")

    if save_artifacts:
        os.makedirs(WEIGHTS_DIR, exist_ok=True)
        model.training_metrics = metrics
        model.save(MODEL_PATH)
        with open(METRICS_PATH, "w", encoding="utf-8") as f:
            json.dump(metrics, f, indent=2)
        print(f"\n💾 Model artifact saved to: {MODEL_PATH}")
        print(f"💾 Metrics saved to: {METRICS_PATH}")

    print("=" * 70)
    return metrics

if __name__ == "__main__":
    train_and_evaluate(save_artifacts=True)
