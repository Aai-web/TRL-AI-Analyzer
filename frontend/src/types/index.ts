/** Type definitions for TRL Intelligence frontend. */

export interface UserProfile {
  id: string;
  name: string;
  email: string;
  organization: string;
  role: string;
}

export interface AuthResponse {
  token: string;
  user: UserProfile;
  message: string;
}

export type EvidenceStrength = 'Strong' | 'Moderate' | 'Weak';

export type VerificationStatus = 
  | 'Verified Result' 
  | 'Empirical Observation' 
  | 'Preliminary Validation' 
  | 'Unverified Claim';

export interface EvidenceItem {
  evidence_id: string;
  trl_level: number;
  criterion_name: string;
  quote: string;
  page_number: number;
  strength: EvidenceStrength;
  confidence_score: number;
  verification_status: VerificationStatus;
  reasoning: string;
}

export interface TRLAlternative {
  trl: number;
  probability: number;
  description: string;
}

export interface FeatureContribution {
  feature: string;
  weight: number;
  impact: 'Positive' | 'Alternative';
}

export interface ModelExplanation {
  primary_reasons: string[];
  dominant_criteria_met: string[];
  disqualifying_factors: string[];
  uncertainty_level: 'Low' | 'Moderate' | 'High';
  uncertainty_reason: string;
  top_feature_contributions: FeatureContribution[];
  is_claim_discounted: boolean;
}

export interface GapRequirement {
  requirement_id: string;
  target_trl: number;
  category: string;
  title: string;
  description: string;
  status: 'Met' | 'Partially Met' | 'Missing';
  gap_severity: 'Critical' | 'Major' | 'Minor';
  impediment_explanation: string;
  recommended_action: string;
  recommended_tests: string[];
}

export interface RoadmapPhase {
  phase_id: string;
  phase_name: string;
  target_trl: number;
  timeline_estimate: string;
  priority: 'High' | 'Medium' | 'Low';
  milestones: string[];
  validation_protocol: string;
  deliverables: string[];
}

export interface TRLPredictionResult {
  predicted_trl: number;
  trl_title: string;
  trl_definition: string;
  calibrated_confidence: number;
  confidence_tier: 'High' | 'Moderate' | 'Preliminary';
  probability_distribution: Record<number, number>;
  alternatives: TRLAlternative[];
  evidence_items: EvidenceItem[];
  evidence_counts_by_trl: Record<number, number>;
  gap_analysis: GapRequirement[];
  missing_criteria_count: number;
  next_trl_barriers: string[];
  roadmap: RoadmapPhase[];
  model_explanation: ModelExplanation;
  meta: Record<string, any>;
}

export interface DocumentAnalysisResponse {
  document_id: string;
  filename: string;
  file_type: string;
  page_count: number;
  word_count: number;
  char_count: number;
  processed_at: string;
  prediction: TRLPredictionResult;
  summary: string;
  technical_domain: string;
}

export interface SampleDocumentInfo {
  sample_id: string;
  title: string;
  expected_trl: number;
  domain: string;
  description: string;
  file_path: string;
}

export interface ModelInfoResponse {
  model_name: string;
  model_type: string;
  training_dataset_size: number;
  metrics: {
    exact_match_accuracy?: number;
    one_off_accuracy?: number;
    mean_absolute_error?: number;
    root_mean_squared_error?: number;
    dataset_size?: number;
    [key: string]: any;
  };
  trl_definitions: Record<number, {
    title: string;
    category: string;
    definition: string;
  }>;
  feature_extraction_pipeline: string[];
  reproducibility_version: string;
}
