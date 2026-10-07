"""Fare Predictor View for Airlytics."""

from __future__ import annotations

import pandas as pd
import streamlit as st


def render_predictor_view(
    prediction_result: dict | None = None,
    user_features: pd.DataFrame | None = None,
    contrib_df: pd.DataFrame | None = None,
    model_name: str = "Random Forest",
    error_message: str | None = None,
) -> None:
    """Render the fare predictor view and results."""
    st.title("Fare Predictor")
    st.caption("Estimate airfare using the trained machine-learning model.")

    if error_message:
        st.error(error_message)

    if prediction_result is None:
        st.markdown(
            """
            <div class="airlytics-empty-state">
                <div style="font-size: 2rem; margin-bottom: 12px;">✈️</div>
                <div class="airlytics-empty-title">Prediction interface will be implemented in the next stage.</div>
                <div class="airlytics-empty-subtitle">
                    Configure flight details in the left sidebar and click <strong>✈ Estimate fare</strong> to run live inference on the trained Random Forest model.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        with st.expander("About this estimator"):
            st.markdown(
                """
- Inputs follow the Phase 6 feature engineering specification: cyclical time encodings, stop categories, and route legs.
- Preprocessing (StandardScaler + OneHotEncoder) is applied by the fitted Phase 8 pipeline.
- Predictions come from the selected **Random Forest** refitted on all labeled observations.
- Explanations use grouped **Tree SHAP** contributions aggregated to parent features.
"""
            )
        return

    # Render Active Prediction Output
    prediction = prediction_result["prediction"]
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
        flight_info = prediction_result.get("info_df")
        if flight_info is not None:
            st.dataframe(flight_info, use_container_width=True, hide_index=True)

    if contrib_df is not None:
        st.subheader("📖 Why this estimate?")
        plot_fig = prediction_result.get("plot_fig")
        baseline = float(contrib_df["Model_Baseline"].iloc[0])
        total_contrib = float(contrib_df["SHAP_Contribution"].sum())
        sum_check = baseline + total_contrib

        expl_col1, expl_col2 = st.columns([1.2, 1])
        with expl_col1:
            if plot_fig is not None:
                st.pyplot(plot_fig, clear_figure=True)
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
            st.caption("Baseline plus SHAP contributions equals the predicted fare (Tree SHAP additivity).")
            with st.expander("All feature contributions (sorted)"):
                display_cols = ["Feature", "Value", "SHAP_Contribution", "Absolute_SHAP_Contribution"]
                st.dataframe(
                    contrib_df[display_cols].rename(
                        columns={
                            "SHAP_Contribution": "Contribution",
                            "Absolute_SHAP_Contribution": "|Contribution|",
                        }
                    ),
                    use_container_width=True,
                    hide_index=True,
                )
