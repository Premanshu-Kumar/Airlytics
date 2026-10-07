"""Dashboard View for Airlytics."""

from __future__ import annotations

import streamlit as st


def render_dashboard_view() -> None:
    """Render the executive dashboard view."""
    st.title("Airlytics Dashboard")
    st.caption("Intelligent airfare price estimation and flight analytics.")

    st.markdown(
        """
        <div class="airlytics-empty-state">
            <div style="font-size: 2rem; margin-bottom: 12px;">📊</div>
            <div class="airlytics-empty-title">Dashboard modules will be implemented in Stage 4.</div>
            <div class="airlytics-empty-subtitle">
                High-level market telemetry, ground-truth platform KPIs, and key empirical flight dataset insights will be featured here.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
