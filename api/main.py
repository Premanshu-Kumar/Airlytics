"""Airlytics FastAPI Backend Service.

Exposes REST API endpoints for the Next.js frontend, directly consuming
the existing Python ML pipeline and services without duplicating logic.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
if str(PROJECT_ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

from phase6_feature_engineering import FEATURE_COLUMNS, _period, _season
from app.services.data_service import (
    ADDITIONAL_INFO_OPTIONS,
    AIRLINES,
    CLEANED_DATA_PATH,
    DESTINATIONS,
    SOURCES,
    STOP_OPTIONS,
    load_reference_categories,
    load_reference_routes,
)
from app.services.model_service import (
    DEFAULT_MODEL_PATH,
    build_user_row,
    load_artifact,
    predict_fare,
    routes_for_city_pair,
    suggest_route,
    validate_stops_match_route,
)
from app.services.shap_service import local_shap_contributions

app = FastAPI(
    title="Airlytics API",
    description="Intelligent Airfare Price Estimation & Explainable Flight Analytics API",
    version="1.0.0",
)

# Enable CORS for Next.js frontend (default port 3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global lazy load artifact
_artifact_cache: dict[str, Any] | None = None


def get_artifact() -> dict[str, Any]:
    global _artifact_cache
    if _artifact_cache is None:
        _artifact_cache = load_artifact(DEFAULT_MODEL_PATH)
    return _artifact_cache


# ---------------------------------------------------------------------------
# Request & Response Schemas
# ---------------------------------------------------------------------------


class PredictRequest(BaseModel):
    airline: str = Field(..., example="IndiGo")
    source: str = Field(..., example="Bangalore")
    destination: str = Field(..., example="Delhi")
    route: str = Field(..., example="BLR → DEL")
    journey_date: str = Field(..., example="2019-06-15")
    departure_time: str = Field(..., example="09:00")
    arrival_time: str = Field(..., example="11:30")
    duration_minutes: float = Field(..., example=150.0)
    number_of_stops: int = Field(..., example=0)
    additional_info: str = Field(default="No info", example="No info")


class PredictResponse(BaseModel):
    predicted_fare: float
    confidence_interval: list[float]
    model_name: str
    holdout_mae: float
    holdout_r2: float
    inputs_summary: dict[str, Any]


class ShapFeatureContribution(BaseModel):
    feature: str
    value: str
    contribution: float
    absolute_contribution: float
    impact_level: str
    direction: str
    plain_english: str


class ExplainResponse(BaseModel):
    predicted_fare: float
    model_baseline: float
    net_shap_adjustment: float
    additivity_verified: bool
    top_contributors: list[ShapFeatureContribution]
    all_contributors: list[ShapFeatureContribution]
    summary_sentence: str


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@app.get("/api/health")
def health():
    art = get_artifact()
    return {
        "status": "healthy",
        "model_name": art.get("model_name"),
        "training_rows": art.get("training_rows"),
    }


@app.get("/api/metadata")
def metadata():
    routes = load_reference_routes()
    return {
        "airlines": AIRLINES,
        "sources": SOURCES,
        "destinations": DESTINATIONS,
        "stop_options": STOP_OPTIONS,
        "additional_info_options": load_reference_categories(
            "Additional_Info", tuple(ADDITIONAL_INFO_OPTIONS)
        ),
        "routes_count": len(routes),
        "model_name": "Random Forest Regressor",
        "holdout_mae": 640.33,
        "holdout_rmse": 1430.08,
        "holdout_r2": 0.9019,
    }


@app.get("/api/routes/available")
def get_routes(source: str, destination: str):
    routes = load_reference_routes()
    matching = routes_for_city_pair(source, destination, routes)
    default_route = suggest_route(source, destination, routes)
    return {
        "source": source,
        "destination": destination,
        "matching_routes": matching,
        "suggested_route": default_route,
    }


@app.post("/api/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    # 1. Route-stop validation
    mismatch = validate_stops_match_route(
        req.number_of_stops, req.route, req.source, req.destination
    )
    if mismatch:
        raise HTTPException(status_code=400, detail=mismatch)

    # 2. Parse times to decimal hours
    try:
        dep_parts = list(map(int, req.departure_time.split(":")))
        arr_parts = list(map(int, req.arrival_time.split(":")))
        dep_hour = dep_parts[0] + dep_parts[1] / 60.0
        arr_hour = arr_parts[0] + arr_parts[1] / 60.0
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid time format. Expected HH:MM.")

    # 3. Build user features via model_service
    try:
        user_row = build_user_row(
            airline=req.airline,
            source=req.source,
            destination=req.destination,
            route=req.route,
            additional_info=req.additional_info,
            journey_date=pd.Timestamp(req.journey_date),
            departure_hour=dep_hour,
            arrival_hour=arr_hour,
            duration_minutes=req.duration_minutes,
            number_of_stops=req.number_of_stops,
        )
    except ValueError as err:
        raise HTTPException(status_code=400, detail=str(err))

    # 4. Predict
    art = get_artifact()
    pipeline = art["pipeline"]
    fare = predict_fare(pipeline, user_row)
    mae = 640.33
    ci = [max(0.0, round(fare - mae, 2)), round(fare + mae, 2)]

    return PredictResponse(
        predicted_fare=round(fare, 2),
        confidence_interval=ci,
        model_name=art.get("model_name", "Random Forest"),
        holdout_mae=mae,
        holdout_r2=0.9019,
        inputs_summary={
            "airline": req.airline,
            "route": req.route,
            "journey_date": req.journey_date,
            "duration_minutes": req.duration_minutes,
            "stops": req.number_of_stops,
            "stop_category": str(user_row["Stop_Category"].iloc[0]),
            "season": str(user_row["Season"].iloc[0]),
            "departure_period": str(user_row["Departure_Period"].iloc[0]),
        },
    )


@app.post("/api/explain", response_model=ExplainResponse)
def explain(req: PredictRequest):
    # Reuse predict logic to generate user_row
    dep_parts = list(map(int, req.departure_time.split(":")))
    arr_parts = list(map(int, req.arrival_time.split(":")))
    dep_hour = dep_parts[0] + dep_parts[1] / 60.0
    arr_hour = arr_parts[0] + arr_parts[1] / 60.0

    user_row = build_user_row(
        airline=req.airline,
        source=req.source,
        destination=req.destination,
        route=req.route,
        additional_info=req.additional_info,
        journey_date=pd.Timestamp(req.journey_date),
        departure_hour=dep_hour,
        arrival_hour=arr_hour,
        duration_minutes=req.duration_minutes,
        number_of_stops=req.number_of_stops,
    )

    art = get_artifact()
    pipeline = art["pipeline"]
    fare = predict_fare(pipeline, user_row)
    contrib = local_shap_contributions(pipeline, user_row[FEATURE_COLUMNS])

    baseline = float(contrib["Model_Baseline"].iloc[0])
    total_shap = float(contrib["SHAP_Contribution"].sum())
    additivity = abs((baseline + total_shap) - fare) < 0.1

    all_items: list[ShapFeatureContribution] = []
    max_abs = float(contrib["Absolute_SHAP_Contribution"].max()) or 1.0

    for _, row in contrib.iterrows():
        feat = str(row["Feature"])
        val = str(row["Value"])
        shap_val = float(row["SHAP_Contribution"])
        abs_val = float(row["Absolute_SHAP_Contribution"])
        ratio = abs_val / max_abs

        if ratio >= 0.5:
            impact = "High Impact"
        elif ratio >= 0.2:
            impact = "Medium Impact"
        else:
            impact = "Moderate Impact"

        direction = "surcharge" if shap_val >= 0 else "discount"

        # Plain english business translation
        if feat == "Duration_Minutes":
            pe = f"Flight length of {val} mins ({direction} of {abs_val:,.1f} units)"
        elif feat == "Airline":
            pe = f"Carrier pricing baseline for {val} ({direction} of {abs_val:,.1f} units)"
        elif feat == "Number_of_Stops":
            pe = f"Layover handling effect for {val} stops ({direction} of {abs_val:,.1f} units)"
        elif feat == "Route":
            pe = f"Sector operating density for route {val} ({direction} of {abs_val:,.1f} units)"
        elif feat == "Destination":
            pe = f"Demand premium for destination {val} ({direction} of {abs_val:,.1f} units)"
        else:
            pe = f"{feat} configured as {val} contributes {shap_val:+,.1f} units"

        all_items.append(
            ShapFeatureContribution(
                feature=feat,
                value=val,
                contribution=round(shap_val, 2),
                absolute_contribution=round(abs_val, 2),
                impact_level=impact,
                direction=direction,
                plain_english=pe,
            )
        )

    top_feature = all_items[0].feature.replace("_", " ").lower()
    summary = (
        f"{all_items[0].feature.replace('_', ' ')} is the primary factor driving this fare estimate, "
        f"adjusting the baseline by {all_items[0].contribution:+,.1f} source units."
    )

    return ExplainResponse(
        predicted_fare=round(fare, 2),
        model_baseline=round(baseline, 2),
        net_shap_adjustment=round(total_shap, 2),
        additivity_verified=additivity,
        top_contributors=all_items[:10],
        all_contributors=all_items,
        summary_sentence=summary,
    )


@app.get("/api/analytics/overview")
def analytics_overview():
    if not CLEANED_DATA_PATH.is_file():
        raise HTTPException(status_code=404, detail="Cleaned fares data not found")

    df = pd.read_csv(CLEANED_DATA_PATH)

    # 1. Airline median prices
    airline_stats = (
        df.groupby("Airline")["Price"]
        .agg(["median", "count"])
        .reset_index()
        .sort_values("median", ascending=False)
    )
    airline_data = [
        {"airline": row["Airline"], "median_fare": round(float(row["median"]), 2), "count": int(row["count"])}
        for _, row in airline_stats.iterrows()
    ]

    # 2. Stops median prices
    stops_stats = (
        df.groupby("Stops")["Price"]
        .agg(["median", "count"])
        .reset_index()
        .sort_values("Stops")
    )
    stops_data = [
        {"stops": int(row["Stops"]), "median_fare": round(float(row["median"]), 2), "count": int(row["count"])}
        for _, row in stops_stats.iterrows()
    ]

    # 3. Overall distribution stats
    return {
        "total_records": len(df),
        "median_fare": round(float(df["Price"].median()), 2),
        "mean_fare": round(float(df["Price"].mean()), 2),
        "min_fare": round(float(df["Price"].min()), 2),
        "max_fare": round(float(df["Price"].max()), 2),
        "airlines": airline_data,
        "stops": stops_data,
    }


@app.get("/api/models/evaluation")
def model_evaluation():
    eval_csv = PROJECT_ROOT / "outputs" / "phase8" / "evaluation_metrics.csv"
    if not eval_csv.is_file():
        raise HTTPException(status_code=404, detail="Evaluation metrics not found")

    df = pd.read_csv(eval_csv)
    models = []
    for _, row in df.iterrows():
        models.append({
            "rank": int(row["CV_Rank"]),
            "model_name": str(row["Model"]),
            "cv_mae_mean": round(float(row["CV_MAE_Mean"]), 2),
            "cv_mae_std": round(float(row["CV_MAE_Std"]), 2),
            "holdout_mae": round(float(row["Holdout_MAE"]), 2),
            "holdout_rmse": round(float(row["Holdout_RMSE"]), 2),
            "holdout_r2": round(float(row["Holdout_R2"]), 4),
            "is_selected": str(row["Model"]) == "Random Forest",
        })

    return {
        "evaluation_protocol": "5-Fold Cross-Validation on 80% training partition + 20% held-out test set",
        "selected_model": "Random Forest Regressor",
        "models": models,
    }
