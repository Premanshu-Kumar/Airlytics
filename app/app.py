"""Airlytics Phase 10 — Interactive Airfare Estimator.

Run with:
    streamlit run app/app.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import joblib
from phase6_feature_engineering import FEATURE_COLUMNS, TARGET_COLUMN, _period, _season

st.set_page_config(page_title="Airlytics — Airfare Estimator", page_icon="✈️", layout="wide")

DEFAULT_MODEL_PATH = PROJECT_ROOT / "outputs" / "phase8" / "models" / "selected_model.joblib"
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


@st.cache_resource(show_spinner=False)
def load_artifact(model_path: Path):
    if not model_path.is_file():
        raise FileNotFoundError(
            f"Selected model not found at {model_path}. Run Phase 8 first "
            f"(`python scripts/phase8_model_evaluation.py`)."
        )
    return joblib.load(model_path)


@st.cache_data(show_spinner=False)
def load_reference_routes() -> list[str]:
    if not CLEANED_DATA_PATH.is_file():
        return []
    df = pd.read_csv(CLEANED_DATA_PATH)
    if "Route" not in df.columns:
        raise ValueError(f"Cleaned fare data at {CLEANED_DATA_PATH} has no `Route` column.")
    return sorted(df["Route"].dropna().unique().tolist())


@st.cache_data(show_spinner=False)
def load_reference_categories(column: str, fallback: tuple[str, ...]) -> list[str]:
    if not CLEANED_DATA_PATH.is_file():
        return sorted(set(fallback))
    df = pd.read_csv(CLEANED_DATA_PATH)
    if column not in df.columns:
        raise ValueError(f"Cleaned fare data at {CLEANED_DATA_PATH} has no `{column}` column.")
    observed = (
        df[column]
        .dropna()
        .astype("string")
        .str.strip()
        .loc[lambda values: values.ne("")]
        .tolist()
    )
    return sorted(set(fallback) | set(observed))


def suggest_route(source: str, destination: str, reference_routes: list[str]) -> str:
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
    parts = [part.strip() for part in route.split("→")]
    if len(parts) < 2:
        return False
    source_code = SOURCE_TO_CODE.get(source, source[:3].upper())
    destination_code = DESTINATION_TO_CODE.get(destination, destination[:3].upper())
    return parts[0] == source_code and parts[-1] == destination_code


def routes_for_city_pair(
    source: str, destination: str, reference_routes: list[str]
) -> list[str]:
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


def _group_transformed_columns(preprocessor, transformed_names: np.ndarray) -> dict[str, list[int]]:
    groups = {column: [] for column in FEATURE_COLUMNS}
    candidates = sorted(FEATURE_COLUMNS, key=len, reverse=True)
    for position, name in enumerate(transformed_names):
        output_name = str(name).split("__", maxsplit=1)[-1]
        source = next(
            (c for c in candidates if output_name == c or output_name.startswith(f"{c}_")),
            None,
        )
        if source is None:
            raise ValueError(f"Cannot map transformed feature {name!r} to an input feature.")
        groups[source].append(position)
    if any(not positions for positions in groups.values()):
        missing = [n for n, p in groups.items() if not p]
        raise ValueError(f"Model preprocessing omitted expected input features: {missing}")
    return groups


def local_shap_contributions(pipeline, x: pd.DataFrame) -> pd.DataFrame:
    try:
        import shap
    except ImportError as err:
        raise ImportError(
            "SHAP is required for explanations. Install requirements-modeling.txt."
        ) from err

    preprocessor = pipeline.named_steps["preprocessing"]
    regressor = pipeline.named_steps["regressor"]
    if not hasattr(regressor, "feature_importances_"):
        raise ValueError("Explanations are only available for tree-based models (Random Forest/XGBoost).")

    transformed = preprocessor.transform(x)
    if hasattr(transformed, "toarray"):
        transformed = transformed.toarray()
    transformed = np.asarray(transformed, dtype=np.float64)
    transformed_names = preprocessor.get_feature_names_out()
    grouped = _group_transformed_columns(preprocessor, transformed_names)

    try:
        explainer = shap.TreeExplainer(regressor, feature_perturbation="tree_path_dependent")
        explanation = explainer(transformed, check_additivity=True)
    except Exception as err:
        raise RuntimeError(f"SHAP could not explain the selected model: {err}") from err

    shap_values = np.asarray(explanation.values)
    base_values = np.asarray(explanation.base_values).reshape(-1)
    predictions = np.asarray(regressor.predict(transformed)).reshape(-1)
    if len(base_values) == 1:
        base_values = np.repeat(base_values, len(predictions))

    grouped_values = np.column_stack(
        [shap_values[:, grouped[col]].sum(axis=1) for col in FEATURE_COLUMNS]
    )
    row = pd.DataFrame(
        {
            "Feature": pd.Series(FEATURE_COLUMNS, dtype="string"),
            "Value": x.iloc[0][FEATURE_COLUMNS].astype("string").to_numpy(),
            "SHAP_Contribution": grouped_values[0],
            "Model_Baseline": float(base_values[0]),
            "Model_Prediction": float(predictions[0]),
        }
    )
    row["Absolute_SHAP_Contribution"] = row["SHAP_Contribution"].abs()
    return row.sort_values("Absolute_SHAP_Contribution", ascending=False, ignore_index=True)


def plot_contributions(contrib: pd.DataFrame, top_n: int = 10):
    display_df = contrib.head(top_n).iloc[::-1]
    fig, ax = plt.subplots(figsize=(9, max(4, 0.45 * top_n)))
    colors = ["#28A745" if v >= 0 else "#D9534F" for v in display_df["SHAP_Contribution"]]
    ax.barh(display_df["Feature"], display_df["SHAP_Contribution"], color=colors)
    ax.axvline(0, color="#333333", linewidth=0.8)
    ax.set_xlabel("SHAP contribution (fare source units)")
    ax.set_title(f"Top {min(top_n, len(contrib))} features driving this prediction")
    fig.tight_layout()
    return fig


def validate_stops_match_route(
    number_of_stops: int,
    route: str,
    source: str | None = None,
    destination: str | None = None,
) -> str | None:
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


def main() -> None:
    st.title("✈️ Airlytics — Intelligent Airfare Estimator")
    st.caption(
        "Phase 10 interactive estimator built on the Phase 8 Random Forest. "
        "Fares are reported in the dataset's source units (historical 2019 observations)."
    )

    try:
        artifact = load_artifact(DEFAULT_MODEL_PATH)
    except Exception as err:
        st.error(str(err))
        st.stop()

    pipeline = artifact["pipeline"]
    model_name = artifact.get("model_name", "Selected model")
    training_rows = artifact.get("training_rows", "—")
    reference_routes = load_reference_routes()
    additional_info_options = load_reference_categories(
        "Additional_Info", tuple(ADDITIONAL_INFO_OPTIONS)
    )

    with st.sidebar:
        st.header("Flight details")

        airline = st.selectbox("Airline", options=AIRLINES, index=AIRLINES.index("IndiGo"))
        col1, col2 = st.columns(2)
        with col1:
            source = st.selectbox("Source city", options=SOURCES, index=SOURCES.index("Bangalore"))
        with col2:
            destination = st.selectbox(
                "Destination city",
                options=[d for d in DESTINATIONS if d != source] or DESTINATIONS,
                index=0,
            )
        default_route = suggest_route(source, destination, reference_routes)
        route_options = routes_for_city_pair(source, destination, reference_routes)
        try:
            default_route_idx = route_options.index(default_route)
        except ValueError:
            default_route_idx = 0
        route = st.selectbox(
            "Route (airport codes with layovers)",
            options=route_options,
            index=default_route_idx,
            help="Airport codes separated by → matching the training data.",
        )

        journey_date = st.date_input(
            "Journey date",
            value=pd.Timestamp("2019-06-15"),
            min_value=pd.Timestamp("2019-01-01"),
            max_value=pd.Timestamp("2019-12-31"),
            help="The training data covers 2019 calendar observations.",
        )

        tcol1, tcol2 = st.columns(2)
        with tcol1:
            dep_time = st.time_input("Departure time", value=pd.Timestamp("09:00").time())
        with tcol2:
            arr_time = st.time_input("Arrival time", value=pd.Timestamp("11:30").time())

        def to_hour(t) -> float:
            return t.hour + t.minute / 60.0 + t.second / 3600.0

        dep_hour = to_hour(dep_time)
        arr_hour = to_hour(arr_time)
        raw_duration_hours = (arr_hour - dep_hour) % 24
        if raw_duration_hours == 0:
            raw_duration_hours = 24.0
        suggested_duration = max(30, int(round(raw_duration_hours * 60)))

        duration_minutes = st.slider(
            "Flight duration (minutes)",
            min_value=15,
            max_value=2400,
            value=suggested_duration,
            step=5,
        )

        default_stops = max(0, route.count("→") - 1) if route else 0
        default_stops = min(default_stops, max(STOP_OPTIONS))
        number_of_stops = st.selectbox(
            "Number of stops",
            options=STOP_OPTIONS,
            index=STOP_OPTIONS.index(default_stops),
        )

        default_info_idx = ADDITIONAL_INFO_OPTIONS.index("No info")
        additional_info = st.selectbox(
            "Additional info",
            options=additional_info_options,
            index=additional_info_options.index("No info")
            if "No info" in additional_info_options
            else default_info_idx,
        )

        st.divider()
        estimate_clicked = st.button("✈ Estimate fare", type="primary", use_container_width=True)
        st.caption(
            f"Model: **{model_name}** · Trained on **{training_rows:,}** rows"
        )

    mismatch = validate_stops_match_route(number_of_stops, route, source, destination)
    if mismatch:
        st.warning(mismatch)
        if estimate_clicked:
            st.error("Correct the route and stop count before estimating the fare.")
            return

    if not estimate_clicked:
        st.info("Configure your flight on the left and click **✈ Estimate fare**.")
        with st.expander("About this estimator"):
            st.markdown(
                """
- Inputs follow the Phase 6 feature engineering specification exactly: date/time
  features, cyclical sine/cosine encodings, stop category, route leg count, and
  departure/arrival periods.
- Preprocessing (standard scaling + one-hot encoding with rare-category grouping)
  is applied by the fitted Phase 8 pipeline.
- Fare predictions come from the selected **Random Forest** refitted on all
  labeled observations after holdout evaluation.
- Individual explanations use grouped **Tree SHAP** contributions aggregated
  back to the original input feature names.
"""
            )
        return

    try:
        user_features = build_user_row(
            airline=airline,
            source=source,
            destination=destination,
            route=route,
            additional_info=additional_info,
            journey_date=pd.Timestamp(journey_date),
            departure_hour=dep_hour,
            arrival_hour=arr_hour,
            duration_minutes=float(duration_minutes),
            number_of_stops=number_of_stops,
        )
    except ValueError as err:
        st.error(f"Could not compute fare estimate: {err}")
        return

    try:
        prediction = float(pipeline.predict(user_features[FEATURE_COLUMNS])[0])
    except Exception as err:
        st.error(f"Prediction failed: {err}")
        return

    predicted_display = f"{prediction:,.2f}"

    kpi_col, info_col = st.columns([1.2, 1.2])
    with kpi_col:
        st.metric(
            label="Estimated fare (source units)",
            value=predicted_display,
            delta=f"{model_name}",
            delta_color="off",
        )
        st.caption(
            "This is a data-driven estimate based on historical 2019 patterns; "
            "it is not a guarantee of current market prices."
        )
    with info_col:
        info_df = pd.DataFrame(
            {
                "Field": pd.Series(
                    [
                        "Airline", "Route", "Journey date", "Departure",
                        "Arrival", "Duration", "Stops", "Additional info",
                    ],
                    dtype="string",
                ),
                "Value": pd.Series(
                    [
                        str(airline),
                        str(route),
                        pd.Timestamp(journey_date).strftime("%A, %d %B %Y"),
                        f"{dep_time.strftime('%H:%M')} ({_period(dep_hour)})",
                        f"{arr_time.strftime('%H:%M')} ({_period(arr_hour)})",
                        f"{duration_minutes} minutes",
                        f"{number_of_stops} stop(s) · {user_features['Stop_Category'].iloc[0]}",
                        str(additional_info),
                    ],
                    dtype="string",
                ),
            }
        )
        st.dataframe(info_df, use_container_width=True, hide_index=True)

    st.subheader("📖 Why this estimate?")

    try:
        contrib = local_shap_contributions(pipeline, user_features[FEATURE_COLUMNS])
    except Exception as err:
        st.warning(f"Explanations are unavailable for this configuration: {err}")
        contrib = None

    if contrib is not None:
        baseline = float(contrib["Model_Baseline"].iloc[0])
        model_predicted = float(contrib["Model_Prediction"].iloc[0])
        total_contrib = float(contrib["SHAP_Contribution"].sum())
        sum_check = baseline + total_contrib

        expl_col1, expl_col2 = st.columns([1.2, 1])
        with expl_col1:
            st.pyplot(plot_contributions(contrib, top_n=10), clear_figure=True)
            st.caption(
                "Green bars push the estimate above the model baseline; "
                "red bars pull it below."
            )
        with expl_col2:
            st.markdown(
                f"""
| Item | Value (source units) |
|---|---:|
| Model baseline | {baseline:,.2f} |
| Sum of feature contributions | {total_contrib:+,.2f} |
| Predicted fare (baseline + contributions) | {sum_check:,.2f} |
"""
            )
            st.caption(
                "Baseline plus SHAP contributions equals the predicted fare "
                "(Tree SHAP additivity)."
            )
            with st.expander("All feature contributions (sorted)"):
                display_cols = [
                    "Feature", "Value", "SHAP_Contribution", "Absolute_SHAP_Contribution",
                ]
                st.dataframe(
                    contrib[display_cols].rename(
                        columns={
                            "SHAP_Contribution": "Contribution",
                            "Absolute_SHAP_Contribution": "|Contribution|",
                        }
                    ),
                    use_container_width=True,
                    hide_index=True,
                )

    with st.expander("🔬 Global feature reference (training data)"):
        global_importance_path = (
            PROJECT_ROOT / "outputs" / "phase9" / "global_feature_importance.csv"
        )
        if global_importance_path.is_file():
            gi = pd.read_csv(global_importance_path).head(15)
            gcol1, gcol2 = st.columns([1.2, 1])
            with gcol1:
                disp = gi.sort_values("Mean_Absolute_SHAP")
                fig2, ax2 = plt.subplots(figsize=(9, 6))
                ax2.barh(disp["Feature"], disp["Mean_Absolute_SHAP"], color="#2878B5")
                ax2.set_xlabel("Mean absolute grouped SHAP (source units)")
                ax2.set_title("Global feature importance from training")
                fig2.tight_layout()
                st.pyplot(fig2, clear_figure=True)
            with gcol2:
                st.dataframe(
                    gi[["Feature", "Mean_Absolute_SHAP", "Mean_SHAP"]].rename(
                        columns={
                            "Mean_Absolute_SHAP": "Mean |SHAP|",
                            "Mean_SHAP": "Mean SHAP",
                        }
                    ),
                    use_container_width=True,
                    hide_index=True,
                )
            st.caption(
                "Global associations learned by the Random Forest over the training "
                "sample; these describe model behavior and are not causal effects."
            )
        else:
            st.info("Run Phase 9 to populate the global feature reference.")


if __name__ == "__main__":
    main()
