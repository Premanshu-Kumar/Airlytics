"""AI Explanation View for Airlytics."""

from __future__ import annotations

import streamlit as st


def render_explanation_view(contrib_df=None) -> None:
    """Render the AI explainability view."""
    st.title("AI Explanation")
    st.caption("Understand why the model produced a particular fare estimate.")

    st.markdown(
        """
        <div class="airlytics-empty-state">
            <div style="font-size: 2rem; margin-bottom: 12px;">🧠</div>
            <div class="airlytics-empty-title">SHAP explanation interface will be implemented later.</div>
            <div class="airlytics-empty-subtitle">
                Interactive Tree SHAP waterfalls, force diagrams, positive vs. negative cost drivers, and consumer-friendly plain-English feature interpretations will be displayed here.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
