/**
 * Airlytics API Contract Types
 */

export interface MetadataResponse {
  airlines: string[];
  sources: string[];
  destinations: string[];
  stop_options: number[];
  additional_info_options: string[];
  routes_count: number;
  model_name: string;
  holdout_mae: number;
  holdout_rmse: number;
  holdout_r2: number;
}

export interface AvailableRoutesResponse {
  source: string;
  destination: string;
  matching_routes: string[];
  suggested_route: string;
}

export interface PredictRequest {
  airline: string;
  source: string;
  destination: string;
  route: string;
  journey_date: string;
  departure_time: string;
  arrival_time: string;
  duration_minutes: number;
  number_of_stops: number;
  additional_info?: string;
}

export interface PredictResponse {
  predicted_fare: number;
  confidence_interval: [number, number];
  model_name: string;
  holdout_mae: number;
  holdout_r2: number;
  inputs_summary: {
    airline: string;
    route: string;
    journey_date: string;
    duration_minutes: number;
    stops: number;
    stop_category: string;
    season: string;
    departure_period: string;
  };
}

export interface ShapContribution {
  feature: string;
  value: string;
  contribution: number;
  absolute_contribution: number;
  impact_level: "High Impact" | "Medium Impact" | "Moderate Impact";
  direction: "surcharge" | "discount";
  plain_english: string;
}

export interface ExplainResponse {
  predicted_fare: number;
  model_baseline: number;
  net_shap_adjustment: number;
  additivity_verified: boolean;
  top_contributors: ShapContribution[];
  all_contributors: ShapContribution[];
  summary_sentence: string;
}

export interface AirlineStat {
  airline: string;
  median_fare: number;
  count: number;
}

export interface StopStat {
  stops: number;
  median_fare: number;
  count: number;
}

export interface AnalyticsOverviewResponse {
  total_records: number;
  median_fare: number;
  mean_fare: number;
  min_fare: number;
  max_fare: number;
  airlines: AirlineStat[];
  stops: StopStat[];
}

export interface ModelEvalItem {
  rank: number;
  model_name: string;
  cv_mae_mean: number;
  cv_mae_std: number;
  holdout_mae: number;
  holdout_rmse: number;
  holdout_r2: number;
  is_selected: boolean;
}

export interface ModelEvaluationResponse {
  evaluation_protocol: string;
  selected_model: string;
  models: ModelEvalItem[];
}
