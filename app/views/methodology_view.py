"""About / Methodology View for Airlytics."""

from __future__ import annotations

import streamlit as st


def render_methodology_view() -> None:
    """Render the project methodology, limitations, and ethics view."""
    st.title("About Airlytics")
    st.caption("Project methodology, dataset, machine learning, and explainability.")

    st.markdown(
        """
        <div class="airlytics-empty-state">
            <div style="font-size: 2rem; margin-bottom: 12px;">📖</div>
            <div class="airlytics-empty-title">Methodology content will be implemented later.</div>
            <div class="airlytics-empty-subtitle">
                Academic alignment (LPU INT234 Predictive Analytics), dataset attribution (EaseMyTrip CC0), 11-phase reproducible workflow, Tree SHAP mathematical foundations, and critical limitations (lack of booking date field) will be fully documented here.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
