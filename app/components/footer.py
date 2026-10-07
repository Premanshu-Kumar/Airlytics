"""Airlytics Footer Component."""

from __future__ import annotations

import streamlit as st


def render_footer() -> None:
    """Render the standard application footer."""
    st.markdown(
        """
        <div class="airlytics-footer">
            <strong>AIRLYTICS</strong> — Intelligent Airfare Price Estimation & Explainable Flight Analytics<br/>
            <span>Machine Learning • Explainability • Flight Analytics | LPU INT234 Academic Project</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
