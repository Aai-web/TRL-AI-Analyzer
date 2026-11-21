"""Main FastAPI Application Entrypoint for TRL Intelligence.

Techfest IIT Bombay 2nd APCTT Hackathon 2026.
"""

import os
import io
import json
from typing import List, Optional
from datetime import datetime, timezone
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response, JSONResponse

from .config import settings
from .models.schemas import (
    DocumentAnalysisResponse,
    TextAnalysisRequest,
    ModelInfoResponse,
    SampleDocumentInfo,
    UserProfile,
    LoginRequest,
    RegisterRequest,
    AuthResponse
)
from .document_parser import DocumentParser, DocumentParsingError
from .services.analysis_service import AnalysisService
from .services.report_service import ReportService
from .ml.trl_criteria import TRL_DEFINITIONS
from .ml.train import METRICS_PATH, WEIGHTS_DIR

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-Powered Technology Readiness Level (TRL 1-9) Prediction, Evidence Extraction & Gap Analysis"
)

# Enable CORS for local dev and web frontends
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize core services
document_parser = DocumentParser(chunk_size_chars=1200, chunk_overlap_chars=200)
analysis_service = AnalysisService()

# Sample documents directory
SAMPLE_DOCS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "sample_documents"))

@app.get("/api/health")
def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "model_loaded": analysis_service.classifier is not None,
        "cached_history_count": len(analysis_service.get_history())
    }

# Pre-populated in-memory user database
USERS_DB = {
    "evaluator@iitb.ac.in": {
        "password": "hackathon2026",
        "user": UserProfile(
            id="usr-evaluator-01",
            name="Prof. Rajesh Sharma",
            email="evaluator@iitb.ac.in",
            organization="IIT Bombay Techfest APCTT Cell",
            role="Lead Technology Assessor"
        )
    },
    "researcher@isro.gov.in": {
        "password": "space2026",
        "user": UserProfile(
            id="usr-researcher-02",
            name="Dr. Ananya Roy",
            email="researcher@isro.gov.in",
            organization="ISRO Propulsion Directorate",
            role="Senior Propulsion Scientist"
        )
    }
}

@app.post("/api/auth/login", response_model=AuthResponse)
def login_user(payload: LoginRequest):
    """Authenticate existing user or evaluate demo login."""
    email_clean = payload.email.strip().lower()
    user_record = USERS_DB.get(email_clean)

    if not user_record or user_record["password"] != payload.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password. You can also use the Instant Demo Login button."
        )

    # Simple session token
    token = f"trl-token-{user_record['user'].id}-{int(datetime.now(timezone.utc).timestamp())}"
    return AuthResponse(
        token=token,
        user=user_record["user"],
        message="Authentication successful."
    )

@app.post("/api/auth/register", response_model=AuthResponse)
def register_user(payload: RegisterRequest):
    """Register a new technology assessor or researcher."""
    email_clean = payload.email.strip().lower()
    if email_clean in USERS_DB:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email address already exists. Please sign in."
        )

    if len(payload.password) < 4:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 4 characters long."
        )

    new_user = UserProfile(
        id=f"usr-{len(USERS_DB)+1:03d}-{int(datetime.now(timezone.utc).timestamp())%10000}",
        name=payload.name.strip(),
        email=email_clean,
        organization=payload.organization.strip() if payload.organization else "Research & Development Lab",
        role=payload.role.strip() if payload.role else "Technology Evaluator"
    )

    USERS_DB[email_clean] = {
        "password": payload.password,
        "user": new_user
    }

    token = f"trl-token-{new_user.id}-{int(datetime.now(timezone.utc).timestamp())}"
    return AuthResponse(
        token=token,
        user=new_user,
        message="Registration successful."
    )

@app.get("/api/auth/demo", response_model=AuthResponse)
def get_demo_account():
    """Quick one-click demo login for hackathon judges and evaluators."""
    demo_record = USERS_DB["evaluator@iitb.ac.in"]
    token = f"trl-token-{demo_record['user'].id}-{int(datetime.now(timezone.utc).timestamp())}"
    return AuthResponse(
        token=token,
        user=demo_record["user"],
        message="Demo evaluator session active."
    )

@app.post("/api/analyze", response_model=DocumentAnalysisResponse)
def analyze_uploaded_document(file: UploadFile = File(...)):
    """Upload and analyze a PDF or TXT technical paper or report."""
    filename = file.filename or "uploaded_document"
    ext = os.path.splitext(filename)[1].lower()

    if ext not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file format '{ext}'. Allowed formats are: {', '.join(settings.ALLOWED_EXTENSIONS)}"
        )

    try:
        content = file.file.read()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to read uploaded file: {str(e)}"
        )

    # Max size check
    max_bytes = settings.UPLOAD_MAX_SIZE_MB * 1024 * 1024
    if len(content) > max_bytes:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File exceeds maximum allowed size of {settings.UPLOAD_MAX_SIZE_MB}MB."
        )

    # Parse document with page preservation
    try:
        if ext == ".pdf":
            chunks, page_count, word_count = document_parser.parse_pdf_bytes(content, filename=filename)
        else:
            text = content.decode("utf-8", errors="replace")
            chunks, page_count, word_count = document_parser.parse_txt_file(text, is_raw_text=True)
    except DocumentParsingError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error parsing document structure: {str(e)}"
        )

    # Execute complete TRL assessment
    try:
        result = analysis_service.analyze_document(
            chunks=chunks,
            filename=filename,
            file_type="PDF" if ext == ".pdf" else "TXT",
            page_count=page_count,
            word_count=word_count
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error during ML assessment pipeline: {str(e)}"
        )

@app.post("/api/analyze-text", response_model=DocumentAnalysisResponse)
def analyze_raw_text(payload: TextAnalysisRequest):
    """Analyze raw technical text, abstract, or pasted report excerpt."""
    if len(payload.text.strip()) < 50:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Provided text is too short to extract meaningful TRL evidence (minimum 50 characters required)."
        )

    try:
        chunks, page_count, word_count = document_parser.parse_txt_file(payload.text, is_raw_text=True)
        result = analysis_service.analyze_document(
            chunks=chunks,
            filename=payload.title or "Pasted Technical Document",
            file_type="TXT",
            page_count=page_count,
            word_count=word_count
        )
        return result
    except DocumentParsingError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error evaluating text content: {str(e)}"
        )

@app.get("/api/history", response_model=List[DocumentAnalysisResponse])
def get_document_history():
    """Retrieve history of analyzed documents in the current session."""
    return analysis_service.get_history()

@app.get("/api/history/{document_id}", response_model=DocumentAnalysisResponse)
def get_document_by_id(document_id: str):
    """Retrieve a specific analysis by its document ID."""
    doc = analysis_service.get_analysis_by_id(document_id)
    if not doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document assessment '{document_id}' not found."
        )
    return doc

@app.get("/api/report/{document_id}")
def download_pdf_report(document_id: str):
    """Download publication-ready PDF assessment report."""
    doc = analysis_service.get_analysis_by_id(document_id)
    if not doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document assessment '{document_id}' not found."
        )

    try:
        pdf_bytes = ReportService.generate_pdf_report(doc)
        safe_filename = f"TRL_Report_{doc.filename.replace(' ', '_').replace('.pdf', '')}_{doc.document_id}.pdf"
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": f'attachment; filename="{safe_filename}"'}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate PDF report: {str(e)}"
        )

@app.get("/api/sample-documents", response_model=List[SampleDocumentInfo])
def list_sample_documents():
    """List preloaded technical sample papers across the TRL 1-9 spectrum."""
    samples = [
        SampleDocumentInfo(
            sample_id="SAMPLE-TRL1",
            title="Quantum Sheath Transport in Hypersonic Boundary Layers",
            expected_trl=1,
            domain="Aerospace & Defence",
            description="Theoretical formulation using Boltzmann transport and first-principles calculations. No physical hardware built.",
            file_path="trl1_basic_principles_quantum_transport.txt"
        ),
        SampleDocumentInfo(
            sample_id="SAMPLE-TRL3",
            title="Silicon-Carbon Nanocomposite Anodes for Lithium Batteries",
            expected_trl=3,
            domain="Energy & Clean Tech",
            description="Laboratory coin cell electrochemical testing demonstrating 1,420 mAh/g reversible capacity across 50 cycles.",
            file_path="trl3_analytical_proof_battery_anodes.txt"
        ),
        SampleDocumentInfo(
            sample_id="SAMPLE-TRL5",
            title="Thermal Vacuum Chamber Testing of CubeSat Transceiver Brassboard",
            expected_trl=5,
            domain="Aerospace & Defence",
            description="High-fidelity brassboard unit tested across 12 thermal cycles in TVAC chamber at 1e-6 Torr with 5W RF power.",
            file_path="trl5_lab_validated_cubesat_transceiver.txt"
        ),
        SampleDocumentInfo(
            sample_id="SAMPLE-TRL7",
            title="Operational Sea Trials of Autonomous Offshore Wind Submersible",
            expected_trl=7,
            domain="Robotics & Autonomous Systems",
            description="Operational prototype hybrid AUV deployed from support vessel in Dogger Bank North Sea under Sea State 4.",
            file_path="trl7_prototype_offshore_submersible.txt"
        ),
        SampleDocumentInfo(
            sample_id="SAMPLE-TRL9",
            title="Autonomous Star Tracker Mission Operations: 5 Years On-Orbit",
            expected_trl=9,
            domain="Aerospace & Defence",
            description="Flight-proven units across 48 commercial satellites with over 5.2 million cumulative operating hours and 99.999% uptime.",
            file_path="trl9_mission_proven_star_tracker.txt"
        )
    ]
    return samples

@app.post("/api/sample-documents/analyze/{sample_id}", response_model=DocumentAnalysisResponse)
def analyze_sample_document(sample_id: str):
    """Analyze one of the preloaded sample documents."""
    sample_files = {
        "SAMPLE-TRL1": ("Quantum Sheath Transport in Hypersonic Boundary Layers.txt", "trl1_basic_principles_quantum_transport.txt"),
        "SAMPLE-TRL3": ("Silicon-Carbon Nanocomposite Anodes for Lithium Batteries.txt", "trl3_analytical_proof_battery_anodes.txt"),
        "SAMPLE-TRL5": ("Thermal Vacuum Chamber Testing of CubeSat Transceiver.txt", "trl5_lab_validated_cubesat_transceiver.txt"),
        "SAMPLE-TRL7": ("Operational Sea Trials of Autonomous Offshore Wind Submersible.txt", "trl7_prototype_offshore_submersible.txt"),
        "SAMPLE-TRL9": ("Autonomous Star Tracker Mission Operations - 5 Years On-Orbit.txt", "trl9_mission_proven_star_tracker.txt")
    }

    if sample_id not in sample_files:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sample document '{sample_id}' not found."
        )

    title, filename = sample_files[sample_id]
    filepath = os.path.join(SAMPLE_DOCS_DIR, filename)

    if not os.path.exists(filepath):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sample document file missing on disk: {filepath}"
        )

    chunks, page_count, word_count = document_parser.parse_txt_file(filepath, is_raw_text=False)
    result = analysis_service.analyze_document(
        chunks=chunks,
        filename=title,
        file_type="TXT",
        page_count=page_count,
        word_count=word_count
    )
    return result

@app.get("/api/model-info", response_model=ModelInfoResponse)
def get_model_information():
    """Retrieve detailed information about the trained Frank & Hall Ordinal ML model."""
    metrics_data = {}
    if os.path.exists(METRICS_PATH):
        try:
            with open(METRICS_PATH, "r", encoding="utf-8") as f:
                metrics_data = json.load(f)
        except Exception:
            metrics_data = {}

    trl_info = {
        trl: {
            "title": data["title"],
            "category": data["category"],
            "definition": data["definition"]
        }
        for trl, data in TRL_DEFINITIONS.items()
    }

    return ModelInfoResponse(
        model_name="TRL Intelligence Frank & Hall Ordinal Classifier",
        model_type="Evidence-Based Ordinal Logistic Ensemble with Isotonic Monotonicity Projection",
        training_dataset_size=metrics_data.get("dataset_size", 32),
        metrics=metrics_data,
        trl_definitions=trl_info,
        feature_extraction_pipeline=[
            "Sublinear TF-IDF (1-2 N-grams, max_features=1500)",
            "TRL 1-9 Normative Criterion Match Vectors",
            "Empirical Action Verbs Density Extraction",
            "Speculative Modal Marker Density Extraction",
            "Verified-to-Speculative Discount Ratio",
            "Quantitative Engineering Metrics Density",
            "Environmental Operational Setting Classification (Lab vs Relevant vs Operational vs Commercial)"
        ],
        reproducibility_version="1.0.0-hackathon2026"
    )
