"""Model Performance View for Airlytics."""

from __future__ import annotations

import streamlit as st


def render_model_eval_view() -> None:
    """Render the model performance and evaluation view."""
    st.title("Model Performance")
    st.caption("Evaluate and compare the machine-learning models.")

    st.markdown(
        """
        <div class="airlytics-empty-state">
            <div style="font-size: 2rem; margin-bottom: 12px;">🏆</div>
            <div class="airlytics-empty-title">Model evaluation dashboard will be implemented later.</div>
            <div class="airlytics-empty-subtitle">
                3-model benchmark leaderboard (Random Forest vs XGBoost vs Linear Regression), 5-fold cross-validation metrics, actual vs. predicted diagnostics, and residual distribution plots will be showcased here.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
