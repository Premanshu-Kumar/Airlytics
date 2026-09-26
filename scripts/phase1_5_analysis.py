"""Run the reproducible Airlytics Phase 1-5 data analysis."""

from __future__ import annotations

import argparse
import calendar
import re
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy.stats import kruskal, spearmanr


EXPECTED_COLUMNS = {
    "Airline",
    "Date_of_Journey",
    "Source",
    "Destination",
    "Route",
    "Dep_Time",
    "Arrival_Time",
    "Duration",
    "Total_Stops",
    "Additional_Info",
    "Price",
}
REQUIRED_FIELDS = [
    "Airline",
    "Journey_Date",
    "Source",
    "Destination",
    "Route",
    "Duration_Minutes",
    "Stops",
    "Price",
]


def parse_duration(value: object) -> float:
    if pd.isna(value):
        return np.nan
    text = str(value).strip().lower()
    hours = re.search(r"(\d+)\s*h", text)
    minutes = re.search(r"(\d+)\s*m", text)
    if not hours and not minutes:
        return np.nan
    total_minutes = int(hours.group(1)) * 60 if hours else 0
    return total_minutes + (int(minutes.group(1)) if minutes else 0)


def parse_stops(value: object) -> float:
    if pd.isna(value):
        return np.nan
    text = str(value).strip().lower()
    if text in {"non-stop", "non stop", "nonstop"}:
        return 0
    match = re.search(r"\d+", text)
    return float(match.group()) if match else np.nan


def parse_hour(value: object) -> float:
    if pd.isna(value):
        return np.nan
    match = re.search(r"\b(\d{1,2}):(\d{2})\b", str(value))
    if not match:
        return np.nan
    hour, minute = map(int, match.groups())
    if hour > 23 or minute > 59:
        return np.nan
    return hour + minute / 60


def format_number(value: float) -> str:
    return f"{value:,.2f}"


def save_figures(data: pd.DataFrame, output_dir: Path) -> None:
    sns.set_theme(style="whitegrid")

    def save(name: str) -> None:
        plt.tight_layout()
        plt.savefig(output_dir / name, dpi=160, bbox_inches="tight")
        plt.close()

    plt.figure(figsize=(9, 5))
    sns.histplot(data["Price"], bins=50, kde=True, color="#2878B5")
    plt.axvline(data["Price"].median(), color="#D9534F", linestyle="--", label="Median")
    plt.title("Observed airfare distribution")
    plt.xlabel("Fare (source units)")
    plt.ylabel("Flight records")
    plt.legend()
    save("price_distribution.png")

    airline_order = data.groupby("Airline")["Price"].median().sort_values().index
    plt.figure(figsize=(12, 6))
    sns.boxplot(data=data, x="Airline", y="Price", order=airline_order, color="#8FC1A9")
    plt.title("Airfare distribution by airline")
    plt.xlabel("Airline")
    plt.ylabel("Fare (source units)")
    plt.xticks(rotation=35, ha="right")
    save("price_by_airline.png")

    common_routes = data["Route"].value_counts().head(15).index
    route_data = data[data["Route"].isin(common_routes)]
    route_order = route_data.groupby("Route")["Price"].median().sort_values().index
    plt.figure(figsize=(12, 7))
    sns.boxplot(data=route_data, y="Route", x="Price", order=route_order, color="#F2C14E")
    plt.title("Airfare distribution on the 15 most frequent routes")
    plt.xlabel("Fare (source units)")
    plt.ylabel("Route")
    save("price_by_route.png")

    monthly = data.groupby("Journey_Month")["Price"].agg(["mean", "median"])
    plt.figure(figsize=(9, 5))
    monthly[["mean", "median"]].plot(
        kind="bar", ax=plt.gca(), color=["#2878B5", "#F2C14E"]
    )
    plt.title("Observed airfare by journey month")
    plt.xlabel("Journey month (2019)")
    plt.ylabel("Fare (source units)")
    plt.xticks(rotation=0)
    plt.legend(["Mean", "Median"])
    save("price_by_month.png")

    stops_order = sorted(data["Stops"].dropna().unique())
    plt.figure(figsize=(9, 5))
    sns.boxplot(data=data, x="Stops", y="Price", order=stops_order, color="#A8DADC")
    plt.title("Airfare distribution by number of stops")
    plt.xlabel("Number of stops")
    plt.ylabel("Fare (source units)")
    save("price_by_stops.png")

    numeric = data[
        [
            "Price",
            "Duration_Minutes",
            "Stops",
            "Departure_Hour",
            "Arrival_Hour",
            "Journey_Month",
            "Journey_DayOfWeek",
        ]
    ].corr()
    plt.figure(figsize=(9, 7))
    sns.heatmap(numeric, annot=True, fmt=".2f", cmap="vlag", center=0, square=True)
    plt.title("Correlation among numeric flight features")
    save("numeric_correlation.png")

    plt.figure(figsize=(9, 5))
    sns.scatterplot(
        data=data.sample(min(len(data), 2500), random_state=42),
        x="Duration_Minutes",
        y="Price",
        hue="Stops",
        palette="viridis",
        alpha=0.65,
    )
    plt.title("Fare, duration, and stops")
    plt.xlabel("Duration (minutes)")
    plt.ylabel("Fare (source units)")
    plt.legend(title="Stops")
    save("fare_duration_stops.png")

    airline_stop = (
        data.groupby(["Airline", "Stops"], observed=True)["Price"]
        .median()
        .unstack()
    )
    plt.figure(figsize=(11, 6))
    sns.heatmap(airline_stop, annot=True, fmt=".0f", cmap="YlGnBu")
    plt.title("Median fare by airline and number of stops")
    plt.xlabel("Number of stops")
    plt.ylabel("Airline")
    save("airline_stops_median_fare.png")
def analyze(input_path: Path, output_dir: Path) -> None:
    raw = pd.read_excel(input_path)
    missing_columns = EXPECTED_COLUMNS.difference(raw.columns)
    if missing_columns:
        raise ValueError(f"Dataset is missing expected columns: {sorted(missing_columns)}")

    raw_missing = raw.isna().sum()
    exact_duplicates = int(raw.duplicated().sum())
    data = raw.drop_duplicates().copy()

    for column in ["Airline", "Source", "Destination", "Route", "Additional_Info"]:
        data[column] = data[column].astype("string").str.strip()
        data[column] = data[column].replace({"": pd.NA, "nan": pd.NA})

    data["Source"] = data["Source"].replace({"Banglore": "Bangalore"})
    data["Destination"] = data["Destination"].replace({"Banglore": "Bangalore"})
    data["Journey_Date"] = pd.to_datetime(
        data["Date_of_Journey"], format="%d/%m/%Y", errors="coerce"
    )
    data["Duration_Minutes"] = data["Duration"].map(parse_duration)
    data["Stops"] = data["Total_Stops"].map(parse_stops)
    data["Departure_Hour"] = data["Dep_Time"].map(parse_hour)
    data["Arrival_Hour"] = data["Arrival_Time"].map(parse_hour)
    data["Price"] = pd.to_numeric(data["Price"], errors="coerce")
    data["Journey_Month"] = data["Journey_Date"].dt.month
    data["Journey_DayOfWeek"] = data["Journey_Date"].dt.dayofweek

    missing_required = data[REQUIRED_FIELDS].isna().any(axis=1)
    invalid_price = data["Price"].le(0) | data["Price"].isna()
    invalid_duration = data["Duration_Minutes"].le(0) | data["Duration_Minutes"].isna()
    invalid_stops = data["Stops"].lt(0) | data["Stops"].isna()
    invalid_date = data["Journey_Date"].isna()
    invalid_records = (
        missing_required | invalid_price | invalid_duration | invalid_stops | invalid_date
    )
    data = data.loc[~invalid_records].copy()

    lower = data["Price"].quantile(0.25)
    upper = data["Price"].quantile(0.75)
    iqr = upper - lower
    outlier_low = lower - 1.5 * iqr
    outlier_high = upper + 1.5 * iqr
    data["Fare_Outlier_IQR"] = data["Price"].lt(outlier_low) | data["Price"].gt(outlier_high)

    output_dir.mkdir(parents=True, exist_ok=True)
    cleaned_columns = [
        "Airline",
        "Journey_Date",
        "Source",
        "Destination",
        "Route",
        "Dep_Time",
        "Departure_Hour",
        "Arrival_Time",
        "Arrival_Hour",
        "Duration_Minutes",
        "Stops",
        "Additional_Info",
        "Price",
        "Journey_Month",
        "Journey_DayOfWeek",
        "Fare_Outlier_IQR",
    ]
    cleaned = data[cleaned_columns].rename(
        columns={"Price": "Fare_Source_Units", "Stops": "Number_of_Stops"}
    )
    cleaned.to_csv(output_dir / "cleaned_fares.csv", index=False, date_format="%Y-%m-%d")

    save_figures(data, output_dir)
    descriptive = data["Price"].describe()
    airline_medians = (
        data.groupby("Airline")["Price"].agg(["count", "median"]).sort_values("median")
    )
    route_medians = (
        data.groupby("Route")["Price"]
        .agg(["count", "median"])
        .query("count >= 25")
        .sort_values("median")
    )
    duration_corr, duration_p = spearmanr(data["Duration_Minutes"], data["Price"])
    airline_groups = [
        group["Price"].to_numpy()
        for _, group in data.groupby("Airline")
        if len(group) >= 2
    ]
    airline_test = kruskal(*airline_groups) if len(airline_groups) >= 2 else None
    airline_h = airline_test.statistic if airline_test else np.nan
    airline_p = airline_test.pvalue if airline_test else np.nan
    airline_p_text = (
        "underflowed to 0.0"
        if airline_test and airline_test.pvalue == 0
        else f"{airline_p:.3g}"
    )
    duration_p_text = "underflowed to 0.0" if duration_p == 0 else f"{duration_p:.3g}"
    monthly_medians = data.groupby("Journey_Month")["Price"].median()

    lower_outliers = int(data["Price"].lt(outlier_low).sum())
    upper_outliers = int(data["Price"].gt(outlier_high).sum())
    normalized_banglore = int(
        raw["Source"].eq("Banglore").sum() + raw["Destination"].eq("Banglore").sum()
    )
    missing_lines = "\n".join(
        f"| `{name}` | {count} |" for name, count in raw_missing.items() if count > 0
    ) or "| None | 0 |"
    airline_low = airline_medians.index[0]
    airline_high = airline_medians.index[-1]
    route_low = route_medians.index[0] if not route_medians.empty else "Not enough repeated routes"
    route_high = route_medians.index[-1] if not route_medians.empty else "Not enough repeated routes"
    month_low = calendar.month_name[int(monthly_medians.idxmin())]
    month_high = calendar.month_name[int(monthly_medians.idxmax())]

    report = f"""# Airlytics Phases 1–5 Analysis

Generated by `python scripts/phase1_5_analysis.py` from the versioned source workbook.

## Phase 1 — Problem definition

**Problem.** Airfare varies with airline, route, journey date, flight duration, and stops. Travelers lack a simple historical reference for comparing fares.

**Objective.** Describe historical airfare patterns and their associations with the available flight attributes. The work is exploratory and does not claim to forecast current or future prices.

**Scope.** This phase uses the labeled India-market training workbook only. It analyzes prices, route, airline, journey date, duration, and stops. The companion test workbook has no price target and is not included in fare analysis. Booking date is absent, so booking-window analysis is out of scope. Currency is not specified in the publisher's dataset metadata; all fare values are therefore reported in source units.

## Phase 2 — Dataset selection and collection

- **Dataset:** Flight Price Prediction DataSet, version 1 (`Data_Train.xlsx` and `Test_set.xlsx`)
- **Publisher/source:** Jillani SofTech; the dataset description says it was obtained from the EaseMyTrip website
- **Source:** [Kaggle dataset page](https://www.kaggle.com/datasets/jillanisofttech/flight-price-prediction-dataset)
- **License listed by publisher:** CC0: Public Domain
- **Labeled workbook:** {len(raw):,} rows × {len(raw.columns)} columns
- **Unlabeled companion workbook:** 2,671 rows × 10 columns
- **Target:** `Price` (source units)
- **Schema and limitations:** See [`data/README.md`](../data/README.md).

The observations are historical snapshots, not a representative sample of every airline or market. The publisher does not document the collection methodology, currency, taxes/fees, fare class, or booking timestamp. The data is from 2019 and should not be interpreted as current market pricing.

## Phase 3 — Data cleaning

| Check | Result |
|---|---:|
| Raw labeled rows | {len(raw):,} |
| Exact duplicate rows removed | {exact_duplicates:,} |
| Rows remaining after validation | {len(data):,} |
| Rows excluded for one or more invalid/missing required fields | {int(invalid_records.sum()):,} |
| Source spelling values normalized (`Banglore` → `Bangalore`) | {normalized_banglore:,} |
| Fare outliers flagged and retained (below / above 1.5×IQR fences) | {lower_outliers:,} / {upper_outliers:,} ({int(data['Fare_Outlier_IQR'].sum()):,} total) |

Missing values in the raw labeled workbook:

| Column | Missing |
|---|---:|
{missing_lines}

Cleaning parses journey dates, duration into minutes, stops into a numeric count, and departure/arrival clock times into decimal hours. Rows missing required analysis fields, with invalid dates, non-positive fares/durations, or invalid stop counts are excluded. Exact duplicates are removed. Outliers are flagged, not dropped, because unusually high fares may be valid observations.

## Phase 4 — Exploratory data analysis

The charts below cover fare distribution, airline and route comparisons, monthly price patterns, stops, numeric correlations, and the interaction of duration and stops with fare.

![Fare distribution](price_distribution.png)
![Fare by airline](price_by_airline.png)
![Fare by route](price_by_route.png)
![Fare by journey month](price_by_month.png)
![Fare by stops](price_by_stops.png)
![Numeric correlations](numeric_correlation.png)
![Duration and stops](fare_duration_stops.png)
![Airline and stops](airline_stops_median_fare.png)

In the cleaned sample, the airline with the lowest/highest median fare is **{airline_low}** / **{airline_high}**. Among routes with at least 25 observations, the lowest/highest median fare is on **{route_low}** / **{route_high}**. The lowest/highest journey-month median is in **{month_low}** / **{month_high}**. These are descriptive sample comparisons, not causal effects or live price guidance.

## Phase 5 — Statistical analysis

| Statistic | Result |
|---|---:|
| Valid observations | {int(descriptive['count']):,} |
| Mean fare | {format_number(descriptive['mean'])} |
| Standard deviation | {format_number(descriptive['std'])} |
| Median fare | {format_number(descriptive['50%'])} |
| Interquartile range | {format_number(descriptive['75%'] - descriptive['25%'])} |
| Minimum / maximum | {format_number(descriptive['min'])} / {format_number(descriptive['max'])} |
| Spearman ρ (duration vs fare) | {duration_corr:.3f} |
| Spearman p-value | {duration_p_text} |
| Kruskal–Wallis H (fare by airline) | {airline_h:.2f} |
| Kruskal–Wallis p-value | {airline_p_text} |

The positive Spearman coefficient indicates that longer flights tended to be associated with higher fares in this sample. The Kruskal–Wallis result indicates fare distributions vary across at least some airline groups; it does not identify which pairs differ. SciPy's reported zero p-values reflect floating-point underflow, not probabilities that are literally zero. Both tests are observational, sensitive to sample size and confounding, and do not establish causality. The airline test was run on groups with at least two observations.

## Reproducibility

Install `requirements-analysis.txt`, then run:

```powershell
python scripts/phase1_5_analysis.py
```

The script writes `cleaned_fares.csv`, this report, and the PNG figures into `outputs/phase1_5/`.
"""
    (output_dir / "phase1_5_report.md").write_text(report, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("data/raw/Data_Train.xlsx"),
        help="Path to the labeled source workbook.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("outputs/phase1_5"),
        help="Directory for cleaned data, report, and figures.",
    )
    args = parser.parse_args()
    if not args.input.is_file():
        raise FileNotFoundError(f"Source workbook not found: {args.input}")
    analyze(args.input, args.output_dir)
    print(f"Phase 1-5 analysis written to {args.output_dir}")


if __name__ == "__main__":
    main()
