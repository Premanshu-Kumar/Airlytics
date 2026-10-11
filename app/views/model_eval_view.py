"""Model Performance View for Airlytics."""

from __future__ import annotations

from pathlib import Path
import pandas as pd
import streamlit as st


def render_model_eval_view() -> None:
    """Render the model performance and evaluation view."""
    st.title("Model Performance Benchmark")
    st.caption("5-Model regression benchmark evaluated via 5-Fold Cross Validation and held-out test data.")

    eval_path = Path("outputs/phase8/evaluation_metrics.csv")
    if eval_path.is_file():
        df = pd.read_csv(eval_path)
        st.subheader("Leaderboard")
        st.dataframe(
            df.style.highlight_min(subset=["Holdout_MAE", "Holdout_RMSE"], color="#1e3a5f")
            .highlight_max(subset=["Holdout_R2"], color="#1e3a5f"),
            use_container_width=True,
        )

        col1, col2 = st.columns(2)
        error_comp = Path("outputs/phase8/model_error_comparison.png")
        if error_comp.is_file():
            col1.image(str(error_comp), caption="Error Comparison (MAE vs RMSE)")

        act_pred = Path("outputs/phase8/actual_vs_predicted.png")
        if act_pred.is_file():
            col2.image(str(act_pred), caption="Actual vs. Predicted Fares (Selected Model)")
    else:
        st.info("Run `python scripts/phase8_model_evaluation.py` to populate benchmark results.")
