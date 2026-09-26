"""Build reproducible, prediction-time airfare features for Phase 6."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd


TARGET_COLUMN = "Fare_Source_Units"
FEATURE_COLUMNS = [
    "Airline",
    "Source",
    "Destination",
    "Route",
    "Additional_Info",
    "Journey_Year",
    "Journey_Month",
    "Journey_Day",
    "Journey_DayOfWeek",
    "Is_Weekend",
    "Season",
    "Month_Sin",
    "Month_Cos",
    "Departure_Hour",
    "Departure_Hour_Sin",
    "Departure_Hour_Cos",
    "Departure_Period",
    "Arrival_Hour",
    "Arrival_Hour_Sin",
    "Arrival_Hour_Cos",
    "Arrival_Period",
    "Duration_Minutes",
    "Number_of_Stops",
    "Stop_Category",
    "Route_Leg_Count",
]

REQUIRED_COLUMNS = {
    "Airline",
    "Journey_Date",
    "Source",
    "Destination",
    "Route",
    "Departure_Hour",
    "Arrival_Hour",
    "Duration_Minutes",
    "Number_of_Stops",
    "Additional_Info",
    TARGET_COLUMN,
}


def _period(hour: float) -> str:
    if hour < 5 or hour >= 21:
        return "Night"
    if hour < 12:
        return "Morning"
    if hour < 17:
        return "Afternoon"
    return "Evening"


def _season(month: int) -> str:
    if month in {12, 1, 2}:
        return "Winter"
    if month in {3, 4, 5, 6}:
        return "Summer"
    if month in {7, 8, 9}:
        return "Monsoon"
    return "Post-Monsoon"


def engineer_features(data: pd.DataFrame) -> pd.DataFrame:
    """Create model features and retain the fare only as a separate target."""
    missing = sorted(REQUIRED_COLUMNS.difference(data.columns))
    if missing:
        raise ValueError(f"Cleaned fare data is missing required columns: {missing}")

    dates = pd.to_datetime(data["Journey_Date"], errors="coerce")
    numeric_columns = [
        "Departure_Hour",
        "Arrival_Hour",
        "Duration_Minutes",
        "Number_of_Stops",
        TARGET_COLUMN,
    ]
    numeric = data[numeric_columns].apply(pd.to_numeric, errors="coerce")
    invalid = dates.isna() | numeric.isna().any(axis=1)
    invalid |= numeric["Duration_Minutes"].le(0)
    invalid |= numeric["Number_of_Stops"].lt(0)
    invalid |= numeric["Number_of_Stops"].mod(1).ne(0)
    invalid |= numeric[TARGET_COLUMN].le(0)
    invalid |= numeric["Departure_Hour"].lt(0) | numeric["Departure_Hour"].ge(24)
    invalid |= numeric["Arrival_Hour"].lt(0) | numeric["Arrival_Hour"].ge(24)
    invalid |= ~numeric[
        ["Departure_Hour", "Arrival_Hour", "Duration_Minutes", "Number_of_Stops", TARGET_COLUMN]
    ].apply(np.isfinite).all(axis=1)
    for column in ["Airline", "Source", "Destination", "Route"]:
        invalid |= data[column].isna() | data[column].astype("string").str.strip().eq("")

    if invalid.any():
        rows = (np.flatnonzero(invalid.to_numpy()) + 2).tolist()
        preview = ", ".join(map(str, rows[:10]))
        suffix = " ..." if len(rows) > 10 else ""
        raise ValueError(
            f"Cleaned fare data contains {len(rows)} invalid row(s) at CSV row(s) "
            f"{preview}{suffix}; correct the input before feature engineering."
        )

    month = dates.dt.month
    departure_hour = numeric["Departure_Hour"]
    arrival_hour = numeric["Arrival_Hour"]
    route = data["Route"].astype("string").str.strip()
    stops = numeric["Number_of_Stops"]
    route_legs = route.str.count("→").clip(lower=1).astype("int64")

    features = pd.DataFrame(index=data.index)
    for column in ["Airline", "Source", "Destination", "Route"]:
        features[column] = data[column].astype("string").str.strip()
    features["Additional_Info"] = (
        data["Additional_Info"].astype("string").str.strip().replace("", pd.NA).fillna("Unknown")
    )
    features["Journey_Year"] = dates.dt.year
    features["Journey_Month"] = month
    features["Journey_Day"] = dates.dt.day
    features["Journey_DayOfWeek"] = dates.dt.dayofweek
    features["Is_Weekend"] = dates.dt.dayofweek.ge(5).astype("int8")
    features["Season"] = month.map(_season)
    features["Month_Sin"] = np.sin(2 * np.pi * (month - 1) / 12)
    features["Month_Cos"] = np.cos(2 * np.pi * (month - 1) / 12)
    features["Departure_Hour"] = departure_hour
    features["Departure_Hour_Sin"] = np.sin(2 * np.pi * departure_hour / 24)
    features["Departure_Hour_Cos"] = np.cos(2 * np.pi * departure_hour / 24)
    features["Departure_Period"] = departure_hour.map(_period)
    features["Arrival_Hour"] = arrival_hour
    features["Arrival_Hour_Sin"] = np.sin(2 * np.pi * arrival_hour / 24)
    features["Arrival_Hour_Cos"] = np.cos(2 * np.pi * arrival_hour / 24)
    features["Arrival_Period"] = arrival_hour.map(_period)
    features["Duration_Minutes"] = numeric["Duration_Minutes"]
    features["Number_of_Stops"] = stops
    features["Stop_Category"] = pd.cut(
        stops,
        bins=[-np.inf, 0, 1, np.inf],
        labels=["Nonstop", "One stop", "Two or more stops"],
        include_lowest=True,
    ).astype("string")
    features["Route_Leg_Count"] = route_legs
    features[TARGET_COLUMN] = numeric[TARGET_COLUMN]
    return features[FEATURE_COLUMNS + [TARGET_COLUMN]].reset_index(drop=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("outputs/phase1_5/cleaned_fares.csv"),
        help="Path to the cleaned fare CSV from Phase 1-5.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("outputs/phase6"),
        help="Directory for the engineered feature CSV and report.",
    )
    args = parser.parse_args()
    if not args.input.is_file():
        raise FileNotFoundError(f"Cleaned fare CSV not found: {args.input}")

    engineered = engineer_features(pd.read_csv(args.input))
    args.output_dir.mkdir(parents=True, exist_ok=True)
    engineered.to_csv(args.output_dir / "engineered_fares.csv", index=False)
    (args.output_dir / "phase6_report.md").write_text(
        f"""# Airlytics Phase 6 — Feature Engineering

Generated by `python scripts/phase6_feature_engineering.py`.

- Valid observations: {len(engineered):,}
- Model input features: {len(FEATURE_COLUMNS)}
- Target: `{TARGET_COLUMN}` (source units)
- Target and target-derived `Fare_Outlier_IQR` are excluded from model inputs.
- Booking window is omitted: the source contains no booking date.

## Engineered features

The input retains airline, origin, destination, route, and additional listing
information. Journey date is expanded into year, month, day, weekday, weekend,
and season; month and clock times also receive sine/cosine encodings to preserve
their cyclical nature. Departure and arrival periods, flight duration, stop
count/category, and route leg count are included.

The output `engineered_fares.csv` contains these features plus the target as a
separate final column. Model preprocessing is fitted only on the training split
in Phase 7.
""",
        encoding="utf-8",
    )
    print(f"Phase 6 features written to {args.output_dir}")


if __name__ == "__main__":
    main()
