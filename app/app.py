"""Airlytics — Intelligent Airfare Price Estimation & Flight Analytics.

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
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from phase6_feature_engineering import FEATURE_COLUMNS, TARGET_COLUMN, _period, _season

# Modular services layer re-exports for backward compatibility & test continuity
from app.services.data_service import (
    ADDITIONAL_INFO_OPTIONS,
    AIRLINES,
    CLEANED_DATA_PATH,
    DESTINATION_TO_CODE,
    DESTINATIONS,
    ENGINEERED_DATA_PATH,
    SOURCE_TO_CODE,
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
    route_matches_cities,
    routes_for_city_pair,
    suggest_route,
    validate_stops_match_route,
)
from app.services.shap_service import (
    _group_transformed_columns,
    local_shap_contributions,
    plot_contributions,
)

# Shared UI components and views
from app.components.header import render_header
from app.components.footer import render_footer
from app.views.dashboard_view import render_dashboard_view
from app.views.predictor_view import render_predictor_view
from app.views.analytics_view import render_analytics_view
from app.views.explanation_view import render_explanation_view
from app.views.model_eval_view import render_model_eval_view
from app.views.route_view import render_route_view
from app.views.methodology_view import render_methodology_view

st.set_page_config(page_title="Airlytics — Airfare Estimator", page_icon="✈️", layout="wide")


def load_css() -> None:
    """Inject the global Airlytics CSS design system into the app."""
    css_path = PROJECT_ROOT / "app" / "assets" / "style.css"
    if css_path.is_file():
        css_content = css_path.read_text(encoding="utf-8")
        st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)


def main() -> None:
    # 1. Apply global styling
    load_css()

    # 2. Load model artifact & metadata
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

    # 3. Render Top Telemetry Header
    render_header(model_name=str(model_name), r2_score="0.9019")

    # 4. Sidebar: Navigation & Flight Parameters
    with st.sidebar:
        st.markdown(
            """
            <div class="airlytics-nav-container">
                <div class="airlytics-nav-label">Navigation Console</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        nav_options = [
            "Dashboard",
            "Fare Predictor",
            "Price Analytics",
            "AI Explanation",
            "Model Performance",
            "Route Insights",
            "About / Methodology",
        ]
        active_view = st.radio(
            "Navigation",
            options=nav_options,
            index=0,
            label_visibility="collapsed",
        )

        st.divider()
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

    # 5. Route consistency validation
    mismatch = validate_stops_match_route(number_of_stops, route, source, destination)
    if mismatch:
        st.warning(mismatch)
        if estimate_clicked:
            st.error("Correct the route and stop count before estimating the fare.")
            return

    # 6. Execute prediction & SHAP if triggered
    prediction_result = None
    user_features = None
    contrib_df = None

    if estimate_clicked:
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
            prediction = predict_fare(pipeline, user_features)
            
            # Flight summary dataframe
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

            # Local SHAP calculation
            try:
                contrib_df = local_shap_contributions(pipeline, user_features[FEATURE_COLUMNS])
                plot_fig = plot_contributions(contrib_df, top_n=10)
            except Exception:
                contrib_df = None
                plot_fig = None

            prediction_result = {
                "prediction": prediction,
                "info_df": info_df,
                "plot_fig": plot_fig,
            }
        except ValueError as err:
            st.error(f"Could not compute fare estimate: {err}")
            return
        except Exception as err:
            st.error(f"Prediction failed: {err}")
            return

    # 7. Render Active Page View
    if estimate_clicked and prediction_result is not None:
        render_predictor_view(
            prediction_result=prediction_result,
            user_features=user_features,
            contrib_df=contrib_df,
            model_name=str(model_name),
        )
    elif active_view == "Dashboard":
        render_dashboard_view()
    elif active_view == "Fare Predictor":
        render_predictor_view(
            prediction_result=prediction_result,
            user_features=user_features,
            contrib_df=contrib_df,
            model_name=str(model_name),
        )
    elif active_view == "Price Analytics":
        render_analytics_view()
    elif active_view == "AI Explanation":
        render_explanation_view(contrib_df=contrib_df)
    elif active_view == "Model Performance":
        render_model_eval_view()
    elif active_view == "Route Insights":
        render_route_view()
    elif active_view == "About / Methodology":
        render_methodology_view()

    # 8. Render Application Footer
    render_footer()


if __name__ == "__main__":
    main()
