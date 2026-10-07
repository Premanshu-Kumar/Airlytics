"""Airlytics Header Component."""

from __future__ import annotations

import streamlit as st


def render_header(model_name: str = "Random Forest", r2_score: str = "0.9019") -> None:
    """Render the top application telemetry and branding header."""
    st.markdown(
        f"""
        <div class="airlytics-header">
            <div class="airlytics-brand">
                <span style="font-size: 1.5rem;">✈️</span>
                <div>
                    <div class="airlytics-brand-title">AIRLYTICS</div>
                    <div class="airlytics-brand-tagline">Intelligent Airfare Price Intelligence & Explainability</div>
                </div>
            </div>
            <div class="airlytics-status-badge">
                <div class="airlytics-status-dot"></div>
                <span>Active Model: {model_name} (R² {r2_score})</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
