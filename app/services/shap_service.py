"""Airlytics SHAP Explainability Service.

Handles Tree SHAP calculation, categorical feature aggregation, and visualization.
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from phase6_feature_engineering import FEATURE_COLUMNS


def _group_transformed_columns(
    preprocessor, transformed_names: np.ndarray
) -> dict[str, list[int]]:
    """Map one-hot encoded and scaled feature column indices back to parent features."""
    groups = {column: [] for column in FEATURE_COLUMNS}
    candidates = sorted(FEATURE_COLUMNS, key=len, reverse=True)
    for position, name in enumerate(transformed_names):
        output_name = str(name).split("__", maxsplit=1)[-1]
        source = next(
            (c for c in candidates if output_name == c or output_name.startswith(f"{c}_")),
            None,
        )
        if source is None:
            raise ValueError(f"Cannot map transformed feature {name!r} to an input feature.")
        groups[source].append(position)
    if any(not positions for positions in groups.values()):
        missing = [n for n, p in groups.items() if not p]
        raise ValueError(f"Model preprocessing omitted expected input features: {missing}")
    return groups


def local_shap_contributions(pipeline, x: pd.DataFrame) -> pd.DataFrame:
    """Compute local Tree SHAP contributions aggregated back to the 25 input features."""
    try:
        import shap
    except ImportError as err:
        raise ImportError(
            "SHAP is required for explanations. Install requirements-modeling.txt."
        ) from err

    preprocessor = pipeline.named_steps["preprocessing"]
    regressor = pipeline.named_steps["regressor"]
    if not hasattr(regressor, "feature_importances_"):
        raise ValueError(
            "Explanations are only available for tree-based models (Random Forest/XGBoost)."
        )

    transformed = preprocessor.transform(x)
    if hasattr(transformed, "toarray"):
        transformed = transformed.toarray()
    transformed = np.asarray(transformed, dtype=np.float64)
    transformed_names = preprocessor.get_feature_names_out()
    grouped = _group_transformed_columns(preprocessor, transformed_names)

    try:
        explainer = shap.TreeExplainer(regressor, feature_perturbation="tree_path_dependent")
        explanation = explainer(transformed, check_additivity=True)
    except Exception as err:
        raise RuntimeError(f"SHAP could not explain the selected model: {err}") from err

    shap_values = np.asarray(explanation.values)
    base_values = np.asarray(explanation.base_values).reshape(-1)
    predictions = np.asarray(regressor.predict(transformed)).reshape(-1)
    if len(base_values) == 1:
        base_values = np.repeat(base_values, len(predictions))

    grouped_values = np.column_stack(
        [shap_values[:, grouped[col]].sum(axis=1) for col in FEATURE_COLUMNS]
    )
    row = pd.DataFrame(
        {
            "Feature": pd.Series(FEATURE_COLUMNS, dtype="string"),
            "Value": x.iloc[0][FEATURE_COLUMNS].astype("string").to_numpy(),
            "SHAP_Contribution": grouped_values[0],
            "Model_Baseline": float(base_values[0]),
            "Model_Prediction": float(predictions[0]),
        }
    )
    row["Absolute_SHAP_Contribution"] = row["SHAP_Contribution"].abs()
    return row.sort_values("Absolute_SHAP_Contribution", ascending=False, ignore_index=True)


def plot_contributions(contrib: pd.DataFrame, top_n: int = 10):
    """Generate a horizontal bar plot of feature SHAP contributions."""
    display_df = contrib.head(top_n).iloc[::-1]
    fig, ax = plt.subplots(figsize=(9, max(4, 0.45 * top_n)))
    colors = ["#28A745" if v >= 0 else "#D9534F" for v in display_df["SHAP_Contribution"]]
    ax.barh(display_df["Feature"], display_df["SHAP_Contribution"], color=colors)
    ax.axvline(0, color="#333333", linewidth=0.8)
    ax.set_xlabel("SHAP contribution (fare source units)")
    ax.set_title(f"Top {min(top_n, len(contrib))} features driving this prediction")
    fig.tight_layout()
    return fig
