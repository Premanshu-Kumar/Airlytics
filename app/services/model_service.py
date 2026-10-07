"""Airlytics Model Service.

Handles artifact loading, input validation, user feature engineering, and inference.
"""

from __future__ import annotations

import sys
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from phase6_feature_engineering import FEATURE_COLUMNS, TARGET_COLUMN, _period, _season
from app.services.data_service import DESTINATION_TO_CODE, SOURCE_TO_CODE

DEFAULT_MODEL_PATH = PROJECT_ROOT / "outputs" / "phase8" / "models" / "selected_model.joblib"


@st.cache_resource(show_spinner=False)
def load_artifact(model_path: Path = DEFAULT_MODEL_PATH) -> dict:
    """Load the serialized scikit-learn model artifact dictionary."""
    if not model_path.is_file():
        raise FileNotFoundError(
            f"Selected model not found at {model_path}. Run Phase 8 first "
            f"(`python scripts/phase8_model_evaluation.py`)."
        )
    return joblib.load(model_path)


def suggest_route(source: str, destination: str, reference_routes: list[str]) -> str:
    """Find the best matching route code representation for a given city pair."""
    src_code = SOURCE_TO_CODE.get(source, source[:3].upper())
    dst_code = DESTINATION_TO_CODE.get(destination, destination[:3].upper())
    nonstop = f"{src_code} → {dst_code}"
    if nonstop in reference_routes:
        return nonstop
    for route in reference_routes:
        parts = [p.strip() for p in route.split("→")]
        if parts and parts[0] == src_code and parts[-1] == dst_code:
            return route
    return nonstop


def route_matches_cities(route: str, source: str, destination: str) -> bool:
    """Validate that a route's starting and ending airport codes correspond to the cities."""
    parts = [part.strip() for part in route.split("→")]
    if len(parts) < 2:
        return False
    source_code = SOURCE_TO_CODE.get(source, source[:3].upper())
    destination_code = DESTINATION_TO_CODE.get(destination, destination[:3].upper())
    return parts[0] == source_code and parts[-1] == destination_code


def routes_for_city_pair(
    source: str, destination: str, reference_routes: list[str]
) -> list[str]:
    """Return all known historical routes operating between the given city pair."""
    matching = sorted(
        route
        for route in reference_routes
        if route_matches_cities(route, source, destination)
    )
    if matching:
        return matching
    return [suggest_route(source, destination, reference_routes)]


def build_user_row(
    airline: str,
    source: str,
    destination: str,
    route: str,
    additional_info: str,
    journey_date: pd.Timestamp,
    departure_hour: float,
    arrival_hour: float,
    duration_minutes: float,
    number_of_stops: int,
) -> pd.DataFrame:
    """Construct a validated single-row DataFrame matching the 25-feature schema."""
    raw = pd.DataFrame(
        {
            "Airline": [airline],
            "Journey_Date": [journey_date.strftime("%Y-%m-%d")],
            "Source": [source],
            "Destination": [destination],
            "Route": [route],
            "Departure_Hour": [departure_hour],
            "Arrival_Hour": [arrival_hour],
            "Duration_Minutes": [duration_minutes],
            "Number_of_Stops": [float(number_of_stops)],
            "Additional_Info": [additional_info if additional_info else "Unknown"],
            TARGET_COLUMN: [1.0],
        }
    )
    dates = pd.to_datetime(raw["Journey_Date"], errors="coerce")
    numeric_cols = [
        "Departure_Hour", "Arrival_Hour", "Duration_Minutes",
        "Number_of_Stops", TARGET_COLUMN,
    ]
    numeric = raw[numeric_cols].apply(pd.to_numeric, errors="coerce")

    invalid_parts = []
    if dates.isna().any():
        invalid_parts.append("Journey date is invalid.")
    if numeric.isna().any(axis=None) or not np.isfinite(numeric.to_numpy()).all():
        invalid_parts.append("Numeric fields must contain finite values.")
    if numeric["Duration_Minutes"].iloc[0] <= 0:
        invalid_parts.append("Duration must be greater than zero.")
    if numeric["Number_of_Stops"].iloc[0] < 0 or numeric["Number_of_Stops"].iloc[0] % 1 != 0:
        invalid_parts.append("Number of stops must be a non-negative integer.")
    if numeric[TARGET_COLUMN].iloc[0] <= 0:
        invalid_parts.append("Target placeholder is invalid.")
    if numeric["Departure_Hour"].iloc[0] < 0 or numeric["Departure_Hour"].iloc[0] >= 24:
        invalid_parts.append("Departure hour must be between 0 (inclusive) and 24 (exclusive).")
    if numeric["Arrival_Hour"].iloc[0] < 0 or numeric["Arrival_Hour"].iloc[0] >= 24:
        invalid_parts.append("Arrival hour must be between 0 (inclusive) and 24 (exclusive).")
    for col in ["Airline", "Source", "Destination", "Route"]:
        val = raw[col].iloc[0]
        if pd.isna(val) or str(val).strip() == "":
            invalid_parts.append(f"{col} cannot be empty.")
    if invalid_parts:
        raise ValueError(" ".join(invalid_parts))

    month = dates.dt.month.iloc[0]
    dep_hour = numeric["Departure_Hour"].iloc[0]
    arr_hour = numeric["Arrival_Hour"].iloc[0]
    route_str = str(raw["Route"].iloc[0]).strip()
    stops = numeric["Number_of_Stops"].iloc[0]
    route_legs = max(1, route_str.count("→"))

    features = pd.DataFrame(index=raw.index)
    for col in ["Airline", "Source", "Destination", "Route"]:
        features[col] = [str(raw[col].iloc[0]).strip()]
    info_raw = str(raw["Additional_Info"].iloc[0]).strip()
    features["Additional_Info"] = [info_raw if info_raw else "Unknown"]
    features["Journey_Year"] = int(dates.dt.year.iloc[0])
    features["Journey_Month"] = int(month)
    features["Journey_Day"] = int(dates.dt.day.iloc[0])
    features["Journey_DayOfWeek"] = int(dates.dt.dayofweek.iloc[0])
    features["Is_Weekend"] = np.int8(1 if dates.dt.dayofweek.iloc[0] >= 5 else 0)
    features["Season"] = _season(int(month))
    features["Month_Sin"] = np.sin(2 * np.pi * (month - 1) / 12)
    features["Month_Cos"] = np.cos(2 * np.pi * (month - 1) / 12)
    features["Departure_Hour"] = float(dep_hour)
    features["Departure_Hour_Sin"] = np.sin(2 * np.pi * dep_hour / 24)
    features["Departure_Hour_Cos"] = np.cos(2 * np.pi * dep_hour / 24)
    features["Departure_Period"] = _period(float(dep_hour))
    features["Arrival_Hour"] = float(arr_hour)
    features["Arrival_Hour_Sin"] = np.sin(2 * np.pi * arr_hour / 24)
    features["Arrival_Hour_Cos"] = np.cos(2 * np.pi * arr_hour / 24)
    features["Arrival_Period"] = _period(float(arr_hour))
    features["Duration_Minutes"] = float(numeric["Duration_Minutes"].iloc[0])
    features["Number_of_Stops"] = float(stops)
    stop_cat = pd.cut(
        [stops],
        bins=[-np.inf, 0, 1, np.inf],
        labels=["Nonstop", "One stop", "Two or more stops"],
        include_lowest=True,
    )[0]
    features["Stop_Category"] = str(stop_cat) if pd.notna(stop_cat) else "Nonstop"
    features["Route_Leg_Count"] = int(route_legs)
    features[TARGET_COLUMN] = numeric[TARGET_COLUMN].iloc[0]
    return features[FEATURE_COLUMNS + [TARGET_COLUMN]]


def validate_stops_match_route(
    number_of_stops: int,
    route: str,
    source: str | None = None,
    destination: str | None = None,
) -> str | None:
    """Validate consistency between selected stop count and route airport leg codes."""
    if not route:
        return None
    route_airports = [part.strip() for part in route.split("→")]
    if len(route_airports) < 2 or any(not airport for airport in route_airports):
        return f"Route `{route}` must contain at least two airport codes separated by →."
    if source and destination and not route_matches_cities(route, source, destination):
        source_code = SOURCE_TO_CODE.get(source, source[:3].upper())
        destination_code = DESTINATION_TO_CODE.get(destination, destination[:3].upper())
        return (
            f"Route `{route}` must start at `{source_code}` and end at "
            f"`{destination_code}` for the selected cities."
        )
    expected_stops = len(route_airports) - 2
    if number_of_stops != expected_stops:
        return (
            f"Route `{route}` has {len(route_airports) - 1} leg(s), which implies "
            f"{expected_stops} stop(s). You selected {number_of_stops} stop(s)."
        )
    return None


def predict_fare(pipeline, user_features: pd.DataFrame) -> float:
    """Execute prediction on the fitted pipeline for user features."""
    return float(pipeline.predict(user_features[FEATURE_COLUMNS])[0])
