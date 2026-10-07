"""Route Insights View for Airlytics."""

from __future__ import annotations

import streamlit as st


def render_route_view() -> None:
    """Render the route insights and sector analysis view."""
    st.title("Route Insights")
    st.caption("Explore fare patterns across flight routes.")

    st.markdown(
        """
        <div class="airlytics-empty-state">
            <div style="font-size: 2rem; margin-bottom: 12px;">🗺️</div>
            <div class="airlytics-empty-title">Route analytics will be implemented later.</div>
            <div class="airlytics-empty-subtitle">
                City-pair sector comparisons, direct vs. layover fare deltas, carrier route dominance, and leaderboards of most economical/expensive routes across India will be provided here.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
