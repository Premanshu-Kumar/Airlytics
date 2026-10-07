"""Airlytics Data Service.

Provides reference data loading, category options, and airport/city mappings.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
CLEANED_DATA_PATH = PROJECT_ROOT / "outputs" / "phase1_5" / "cleaned_fares.csv"
ENGINEERED_DATA_PATH = PROJECT_ROOT / "outputs" / "phase6" / "engineered_fares.csv"

AIRLINES = sorted([
    "Air Asia", "Air India", "GoAir", "IndiGo", "Jet Airways", "Jet Airways Business",
    "Multiple carriers", "Multiple carriers Premium economy", "SpiceJet", "Trujet",
    "Vistara", "Vistara Premium economy",
])
SOURCES = sorted(["Bangalore", "Chennai", "Delhi", "Kolkata", "Mumbai"])
DESTINATIONS = sorted(["Bangalore", "Cochin", "Delhi", "Hyderabad", "Kolkata", "New Delhi"])
ADDITIONAL_INFO_OPTIONS = sorted([
    "1 Long layover", "1 Short layover", "2 Long layover", "Business class",
    "Change airports", "In-flight meal not included", "No Info", "No info",
    "No check-in baggage included", "Red-eye flight",
])
STOP_OPTIONS = [0, 1, 2, 3, 4]

SOURCE_TO_CODE = {
    "Bangalore": "BLR", "Chennai": "MAA", "Delhi": "DEL",
    "Kolkata": "CCU", "Mumbai": "BOM",
}
DESTINATION_TO_CODE = {
    "Bangalore": "BLR", "Cochin": "COK", "Delhi": "DEL",
    "Hyderabad": "HYD", "Kolkata": "CCU", "New Delhi": "DEL",
}


@st.cache_data(show_spinner=False)
def load_reference_routes(cleaned_data_path: Path = CLEANED_DATA_PATH) -> list[str]:
    """Load unique historical flight routes observed in the cleaned training data."""
    if not cleaned_data_path.is_file():
        return []
    df = pd.read_csv(cleaned_data_path)
    if "Route" not in df.columns:
        raise ValueError(f"Cleaned fare data at {cleaned_data_path} has no `Route` column.")
    return sorted(df["Route"].dropna().unique().tolist())


@st.cache_data(show_spinner=False)
def load_reference_categories(
    column: str,
    fallback: tuple[str, ...],
    cleaned_data_path: Path = CLEANED_DATA_PATH,
) -> list[str]:
    """Load observed unique categories for a column, merging with fallback defaults."""
    if not cleaned_data_path.is_file():
        return sorted(set(fallback))
    df = pd.read_csv(cleaned_data_path)
    if column not in df.columns:
        raise ValueError(f"Cleaned fare data at {cleaned_data_path} has no `{column}` column.")
    observed = (
        df[column]
        .dropna()
        .astype("string")
        .str.strip()
        .loc[lambda values: values.ne("")]
        .tolist()
    )
    return sorted(set(fallback) | set(observed))
