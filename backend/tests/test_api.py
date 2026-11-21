"""Direct integration tests for FastAPI endpoint functions."""

import unittest
from backend.app.main import (
    health_check,
    get_model_information,
    list_sample_documents,
    analyze_sample_document,
    download_pdf_report,
    analyze_raw_text
)
from backend.app.models.schemas import TextAnalysisRequest

class TestAPIEndpoints(unittest.TestCase):

    def test_health_check(self):
        data = health_check()
        self.assertEqual(data["status"], "healthy")
        self.assertTrue(data["model_loaded"])

    def test_model_info(self):
        data = get_model_information()
        self.assertIn("TRL", data.model_name)
        self.assertEqual(len(data.trl_definitions), 9)

    def test_sample_documents(self):
        samples = list_sample_documents()
        self.assertEqual(len(samples), 5)

    def test_analyze_sample_document(self):
        result = analyze_sample_document("SAMPLE-TRL1")
        self.assertIsNotNone(result)
        self.assertEqual(result.prediction.predicted_trl, 1)
        self.assertGreater(len(result.prediction.evidence_items), 0)
        self.assertGreater(len(result.prediction.gap_analysis), 0)
        self.assertEqual(len(result.prediction.roadmap), 3)

        # Download report
        doc_id = result.document_id
        report_resp = download_pdf_report(doc_id)
        self.assertEqual(report_resp.status_code, 200)
        self.assertEqual(report_resp.media_type, "application/pdf")
        self.assertGreater(len(report_resp.body), 500)

    def test_analyze_raw_text(self):
        req = TextAnalysisRequest(
            title="Quantum Sheath Study",
            text="Using the Boltzmann transport equations, we observe and calculate theoretical plasma sheath dissipation coefficients. No physical hardware has been built."
        )
        result = analyze_raw_text(req)
        self.assertEqual(result.prediction.predicted_trl, 1)
        self.assertGreater(len(result.prediction.evidence_items), 0)

if __name__ == "__main__":
    unittest.main()
