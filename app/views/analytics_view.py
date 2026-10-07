"""Price Analytics View for Airlytics."""

from __future__ import annotations

import streamlit as st


def render_analytics_view() -> None:
    """Render the exploratory price analytics view."""
    st.title("Price Analytics")
    st.caption("Explore airfare patterns across airlines, routes, stops, and duration.")

    st.markdown(
        """
        <div class="airlytics-empty-state">
            <div style="font-size: 2rem; margin-bottom: 12px;">📈</div>
            <div class="airlytics-empty-title">Analytics modules will be implemented later.</div>
            <div class="airlytics-empty-subtitle">
                Interactive distribution histograms, carrier price hierarchy boxplots, stop escalation violins, and duration elasticity scatter plots will be featured here.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
