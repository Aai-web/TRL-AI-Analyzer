"""Pydantic schemas for TRL Intelligence API and ML components."""

from typing import List, Dict, Optional, Any, Literal
from pydantic import BaseModel, Field
from datetime import datetime, timezone

class EvidenceStrength(str):
    STRONG = "Strong"
    MODERATE = "Moderate"
    WEAK = "Weak"

class DocumentChunk(BaseModel):
    chunk_id: str
    page_number: int = Field(..., description="1-indexed page number in the original document")
    text: str
    start_char: int = 0
    end_char: int = 0
    is_heading: bool = False

class EvidenceItem(BaseModel):
    evidence_id: str
    trl_level: int = Field(..., ge=1, le=9, description="TRL level this evidence supports")
    criterion_name: str = Field(..., description="The specific TRL milestone or criterion matched")
    quote: str = Field(..., description="Exact verbatim statement extracted from the document")
    page_number: int = Field(..., description="Exact page reference (1-indexed)")
    strength: Literal["Strong", "Moderate", "Weak"]
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    verification_status: Literal["Verified Result", "Empirical Observation", "Preliminary Validation", "Unverified Claim"]
    reasoning: str = Field(..., description="Explanation of why this statement constitutes evidence")

class TRLAlternative(BaseModel):
    trl: int = Field(..., ge=1, le=9)
    probability: float = Field(..., ge=0.0, le=1.0)
    description: str

class ModelExplanation(BaseModel):
    primary_reasons: List[str]
    dominant_criteria_met: List[str]
    disqualifying_factors: List[str]
    uncertainty_level: Literal["Low", "Moderate", "High"]
    uncertainty_reason: str
    top_feature_contributions: List[Dict[str, Any]]
    is_claim_discounted: bool = Field(False, description="True if speculative claims were discounted")

class GapRequirement(BaseModel):
    requirement_id: str
    target_trl: int = Field(..., ge=1, le=9)
    category: str
    title: str
    description: str
    status: Literal["Met", "Partially Met", "Missing"]
    gap_severity: Literal["Critical", "Major", "Minor"]
    impediment_explanation: str
    recommended_action: str
    recommended_tests: List[str]

class RoadmapPhase(BaseModel):
    phase_id: str
    phase_name: str
    target_trl: int
    timeline_estimate: str
    priority: Literal["High", "Medium", "Low"]
    milestones: List[str]
    validation_protocol: str
    deliverables: List[str]

class TRLPredictionResult(BaseModel):
    predicted_trl: int = Field(..., ge=1, le=9)
    trl_title: str
    trl_definition: str
    calibrated_confidence: float = Field(..., ge=0.0, le=1.0)
    confidence_tier: Literal["High", "Moderate", "Preliminary"]
    probability_distribution: Dict[int, float] = Field(..., description="Calibrated probabilities for TRL 1 to 9")
    alternatives: List[TRLAlternative]
    evidence_items: List[EvidenceItem]
    evidence_counts_by_trl: Dict[int, int]
    gap_analysis: List[GapRequirement]
    missing_criteria_count: int
    next_trl_barriers: List[str]
    roadmap: List[RoadmapPhase]
    model_explanation: ModelExplanation
    meta: Dict[str, Any] = Field(default_factory=dict)

class DocumentAnalysisResponse(BaseModel):
    document_id: str
    filename: str
    file_type: str
    page_count: int
    word_count: int
    char_count: int
    processed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    prediction: TRLPredictionResult
    summary: str
    technical_domain: str

class TextAnalysisRequest(BaseModel):
    title: Optional[str] = "Pasted Technical Text"
    text: str = Field(..., min_length=20, description="Raw technical document text to analyze")

class ModelInfoResponse(BaseModel):
    model_name: str
    model_type: str
    training_dataset_size: int
    metrics: Dict[str, Any]
    trl_definitions: Dict[int, Dict[str, str]]
    feature_extraction_pipeline: List[str]
    reproducibility_version: str

class SampleDocumentInfo(BaseModel):
    sample_id: str
    title: str
    expected_trl: int
    domain: str
    description: str
    file_path: str

class UserProfile(BaseModel):
    id: str
    name: str
    email: str
    organization: str
    role: str

class LoginRequest(BaseModel):
    email: str
    password: str

class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str
    organization: Optional[str] = "Independent Research Lab"
    role: Optional[str] = "Technology Evaluator"

class AuthResponse(BaseModel):
    token: str
    user: UserProfile
    message: str

