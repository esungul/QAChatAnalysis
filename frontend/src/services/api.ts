import { AnalysisResult, AnalysisRequest, DashboardStats, AnalysisSummary } from '../types';

const API_BASE = 'http://localhost:8000';

class APIError extends Error {
  constructor(message: string, public status?: number) {
    super(message);
    this.name = 'APIError';
  }
}

const handleResponse = async (response: Response) => {
  if (!response.ok) {
    const errorText = await response.text();
    throw new APIError(`API error (${response.status}): ${errorText}`, response.status);
  }
  return response.json();
};

export const analysisAPI = {
  analyzeTranscript: async (request: AnalysisRequest): Promise<{ analysis_id: number; result: AnalysisResult }> => {
    const response = await fetch(`${API_BASE}/api/analyze`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(request),
    });
    return handleResponse(response);
  },

  getAnalyses: async (limit: number = 50, offset: number = 0): Promise<{ analyses: AnalysisSummary[] }> => {
    const response = await fetch(`${API_BASE}/api/analyses?limit=${limit}&offset=${offset}`);
    return handleResponse(response);
  },

  getAnalysisDetail: async (analysisId: number): Promise<AnalysisResult> => {
    const response = await fetch(`${API_BASE}/api/analyses/${analysisId}`);
    return handleResponse(response);
  },

  getDashboardStats: async (): Promise<DashboardStats> => {
    const response = await fetch(`${API_BASE}/api/dashboard/stats`);
    return handleResponse(response);
  },

  // Health check endpoint
  healthCheck: async (): Promise<{ message: string; version: string }> => {
    const response = await fetch(`${API_BASE}/`);
    return handleResponse(response);
  },
};