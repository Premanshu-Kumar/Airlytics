import {
  AnalyticsOverviewResponse,
  AvailableRoutesResponse,
  ExplainResponse,
  MetadataResponse,
  ModelEvaluationResponse,
  PredictRequest,
  PredictResponse,
} from "@/types/api";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

async function fetchJson<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;
  const response = await fetch(url, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(options?.headers || {}),
    },
  });

  if (!response.ok) {
    const errorBody = await response.text();
    let message = `API Error ${response.status}: ${response.statusText}`;
    try {
      const parsed = JSON.parse(errorBody);
      if (parsed.detail) message = parsed.detail;
    } catch {
      if (errorBody) message = errorBody;
    }
    throw new Error(message);
  }

  return response.json();
}

export const apiService = {
  getHealth: () => fetchJson<{ status: string; model_name: string; training_rows: number }>("/api/health"),
  getMetadata: () => fetchJson<MetadataResponse>("/api/metadata"),
  getRoutes: (source: string, destination: string) =>
    fetchJson<AvailableRoutesResponse>(
      `/api/routes/available?source=${encodeURIComponent(source)}&destination=${encodeURIComponent(destination)}`
    ),
  predictFare: (data: PredictRequest) =>
    fetchJson<PredictResponse>("/api/predict", {
      method: "POST",
      body: JSON.stringify(data),
    }),
  explainPrediction: (data: PredictRequest) =>
    fetchJson<ExplainResponse>("/api/explain", {
      method: "POST",
      body: JSON.stringify(data),
    }),
  getAnalyticsOverview: () => fetchJson<AnalyticsOverviewResponse>("/api/analytics/overview"),
  getModelEvaluation: () => fetchJson<ModelEvaluationResponse>("/api/models/evaluation"),
};
