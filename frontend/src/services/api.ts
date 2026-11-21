/** API Client Service for TRL Intelligence. */

import {
  DocumentAnalysisResponse,
  SampleDocumentInfo,
  ModelInfoResponse,
  UserProfile,
  AuthResponse
} from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

class ApiError extends Error {
  status: number;
  constructor(message: string, status: number) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
  }
}

async function handleResponse<T>(res: Response): Promise<T> {
  if (!res.ok) {
    let errorDetail = `Request failed with status ${res.status}`;
    try {
      const errorJson = await res.json();
      if (errorJson.detail) {
        errorDetail = errorJson.detail;
      }
    } catch {
      // Fallback to text status
    }
    throw new ApiError(errorDetail, res.status);
  }
  return res.json() as Promise<T>;
}

export const api = {
  /** Upload and analyze a PDF or TXT document. */
  async uploadDocument(file: File): Promise<DocumentAnalysisResponse> {
    const formData = new FormData();
    formData.append('file', file);

    const res = await fetch(`${API_BASE_URL}/analyze`, {
      method: 'POST',
      body: formData,
    });
    return handleResponse<DocumentAnalysisResponse>(res);
  },

  /** Analyze pasted technical text. */
  async analyzeText(text: string, title?: string): Promise<DocumentAnalysisResponse> {
    const res = await fetch(`${API_BASE_URL}/analyze-text`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text, title }),
    });
    return handleResponse<DocumentAnalysisResponse>(res);
  },

  /** List available preloaded sample documents. */
  async getSampleDocuments(): Promise<SampleDocumentInfo[]> {
    const res = await fetch(`${API_BASE_URL}/sample-documents`);
    return handleResponse<SampleDocumentInfo[]>(res);
  },

  /** Analyze a specific sample document by ID. */
  async analyzeSample(sampleId: string): Promise<DocumentAnalysisResponse> {
    const res = await fetch(`${API_BASE_URL}/sample-documents/analyze/${sampleId}`, {
      method: 'POST',
    });
    return handleResponse<DocumentAnalysisResponse>(res);
  },

  /** Get analysis history from current backend session. */
  async getHistory(): Promise<DocumentAnalysisResponse[]> {
    const res = await fetch(`${API_BASE_URL}/history`);
    return handleResponse<DocumentAnalysisResponse[]>(res);
  },

  /** Get model architecture and validation metrics. */
  async getModelInfo(): Promise<ModelInfoResponse> {
    const res = await fetch(`${API_BASE_URL}/model-info`);
    return handleResponse<ModelInfoResponse>(res);
  },

  /** Get direct download URL for PDF assessment report. */
  getReportDownloadUrl(documentId: string): string {
    return `${API_BASE_URL}/report/${documentId}`;
  },

  /** Check backend health status. */
  async checkHealth(): Promise<{ status: string; model_loaded: boolean }> {
    const res = await fetch(`${API_BASE_URL}/health`);
    return handleResponse<{ status: string; model_loaded: boolean }>(res);
  },

  /** Sign in with email and password. */
  async login(email: string, password: string): Promise<AuthResponse> {
    const res = await fetch(`${API_BASE_URL}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    });
    return handleResponse<AuthResponse>(res);
  },

  /** Register new account. */
  async register(data: { name: string; email: string; password: string; organization?: string; role?: string }): Promise<AuthResponse> {
    const res = await fetch(`${API_BASE_URL}/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    return handleResponse<AuthResponse>(res);
  },

  /** Get instant demo evaluator account. */
  async getDemoAccount(): Promise<AuthResponse> {
    const res = await fetch(`${API_BASE_URL}/auth/demo`);
    return handleResponse<AuthResponse>(res);
  }
};
