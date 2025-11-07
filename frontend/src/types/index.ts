export interface AnalysisResult {
  overall_scores: {
    total_score: number;
    max_possible_score: number;
    percentage_score: number;
  };
  first_response_analysis: any;
  security_verification_analysis: any;
  customer_needs_analysis: any;
  interaction_analysis: any;
  time_respect_analysis: any;
  needs_identification_analysis: any;
  transfer_analysis: any;
  [key: string]: any;
}

export interface AnalysisRequest {
  transcript: string;
  model: string;
}

export interface DashboardStats {
  total_analyses: number;
  average_score: number;
  recent_analyses: number;
  score_distribution: {
    excellent: number;
    good: number;
    average: number;
    poor: number;
  };
}

export interface AnalysisSummary {
  id: number;
  transcript_preview: string;
  model_used: string;
  overall_score: number;
  max_score: number;
  percentage_score: number;
  created_at: string;
}