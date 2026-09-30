"""Generate global feature importance and SHAP explanations for Phase 8."""

from __future__ import annotations

import argparse
from pathlib import Path

import joblib
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

if __package__:
    from .phase6_feature_engineering import FEATURE_COLUMNS, TARGET_COLUMN
else:
    from phase6_feature_engineering import FEATURE_COLUMNS, TARGET_COLUMN


MAX_GLOBAL_SAMPLES = 500
RANDOM_STATE = 42


def _group_transformed_columns(preprocessor, transformed_names: np.ndarray) -> dict[str, list[int]]:
    groups = {column: [] for column in FEATURE_COLUMNS}
    candidates = sorted(FEATURE_COLUMNS, key=len, reverse=True)

    for position, name in enumerate(transformed_names):
        output_name = str(name).split("__", maxsplit=1)[-1]
        source = next(
            (
                column
                for column in candidates
                if output_name == column or output_name.startswith(f"{column}_")
            ),
            None,
        )
        if source is None:
            raise ValueError(f"Cannot map transformed feature {name!r} to an input feature.")
        groups[source].append(position)

    if any(not positions for positions in groups.values()):
        missing = [name for name, positions in groups.items() if not positions]
        raise ValueError(f"Model preprocessing omitted expected input features: {missing}")
    return groups


def explain_model(
    data: pd.DataFrame,
    model_path: Path,
    output_dir: Path,
    row_index: int = 0,
    max_samples: int = MAX_GLOBAL_SAMPLES,
) -> pd.DataFrame:
    """Explain the Phase 8 fitted tree pipeline and write explainability artifacts."""
    try:
        import shap
    except ImportError as error:
        raise ImportError(
            "SHAP is required for Phase 9. Install it with "
            "`python -m pip install -r requirements-modeling.txt`."
        ) from error

    missing = sorted(set(FEATURE_COLUMNS + [TARGET_COLUMN]).difference(data.columns))
    if missing:
        raise ValueError(f"Engineered fare data is missing required columns: {missing}")
    if not 0 <= row_index < len(data):
        raise ValueError(f"--row-index must be between 0 and {len(data) - 1}.")
    if max_samples < 1:
        raise ValueError("--max-samples must be at least 1.")
    if not model_path.is_file():
        raise FileNotFoundError(f"Selected Phase 8 model not found: {model_path}")

    artifact = joblib.load(model_path)
    if artifact.get("target_column") != TARGET_COLUMN:
        raise ValueError(f"Model artifact does not target `{TARGET_COLUMN}`.")
    if artifact.get("feature_columns") != FEATURE_COLUMNS:
        raise ValueError("Model artifact feature schema does not match Phase 6.")

    pipeline = artifact["pipeline"]
    preprocessor = pipeline.named_steps["preprocessing"]
    regressor = pipeline.named_steps["regressor"]
    if not hasattr(regressor, "feature_importances_"):
        raise ValueError(
            "Phase 9 currently requires a tree model with feature_importances_; "
            f"the selected model is {artifact.get('model_name')!r}."
        )

    x = data[FEATURE_COLUMNS].reset_index(drop=True)
    target = pd.to_numeric(data[TARGET_COLUMN], errors="coerce")
    if target.isna().any() or not np.isfinite(target.to_numpy()).all():
        raise ValueError(f"`{TARGET_COLUMN}` must contain finite values.")

    selected_positions = np.arange(len(data))
    if len(selected_positions) > max_samples:
        selected_positions = np.sort(
            np.random.default_rng(RANDOM_STATE).choice(
                selected_positions, size=max_samples, replace=False
            )
        )
    if row_index not in selected_positions:
        selected_positions = np.sort(np.append(selected_positions, row_index))

    transformed = preprocessor.transform(x.iloc[selected_positions])
    if hasattr(transformed, "toarray"):
        transformed = transformed.toarray()
    transformed = np.asarray(transformed, dtype=np.float64)
    transformed_names = preprocessor.get_feature_names_out()
    if transformed.shape[1] != len(transformed_names):
        raise ValueError("Transformed feature matrix and feature names have different widths.")
    grouped_columns = _group_transformed_columns(preprocessor, transformed_names)

    try:
        explainer = shap.TreeExplainer(regressor, feature_perturbation="tree_path_dependent")
        explanation = explainer(transformed, check_additivity=True)
    except Exception as error:
        raise RuntimeError(f"SHAP could not explain the selected tree model: {error}") from error

    shap_values = np.asarray(explanation.values)
    if shap_values.ndim != 2 or shap_values.shape != transformed.shape:
        raise ValueError(
            f"Unexpected SHAP output shape {shap_values.shape}; expected {transformed.shape}."
        )
    base_values = np.asarray(explanation.base_values).reshape(-1)
    predictions = np.asarray(regressor.predict(transformed)).reshape(-1)
    if len(base_values) == 1:
        base_values = np.repeat(base_values, len(predictions))
    if not np.allclose(
        base_values + shap_values.sum(axis=1),
        predictions,
        rtol=1e-4,
        atol=1e-2,
    ):
        raise RuntimeError("SHAP values failed the model additivity check.")

    grouped_values = np.column_stack(
        [shap_values[:, grouped_columns[column]].sum(axis=1) for column in FEATURE_COLUMNS]
    )
    global_indices = np.flatnonzero(selected_positions != row_index)
    if not len(global_indices):
        global_indices = np.arange(len(selected_positions))
    global_importance = np.mean(np.abs(grouped_values[global_indices]), axis=0)
    mean_signed_contribution = np.mean(grouped_values[global_indices], axis=0)

    impurity_values = np.asarray(regressor.feature_importances_)
    impurity_importance = np.array(
        [impurity_values[grouped_columns[column]].sum() for column in FEATURE_COLUMNS]
    )
    results = pd.DataFrame(
        {
            "Feature": FEATURE_COLUMNS,
            "Mean_Absolute_SHAP": global_importance,
            "Mean_SHAP": mean_signed_contribution,
            "Random_Forest_Impurity_Importance": impurity_importance,
        }
    ).sort_values("Mean_Absolute_SHAP", ascending=False, ignore_index=True)

    row_position = int(np.flatnonzero(selected_positions == row_index)[0])
    local_values = grouped_values[row_position]
    local_prediction = float(predictions[row_position])
    local_base_value = float(base_values[row_position])
    local_rows = pd.DataFrame(
        {
            "Feature": FEATURE_COLUMNS,
            "Value": x.iloc[row_index][FEATURE_COLUMNS].to_numpy(),
            "SHAP_Contribution": local_values,
            "Model_Baseline": local_base_value,
            "Model_Prediction": local_prediction,
        }
    )
    local_rows["Absolute_SHAP_Contribution"] = local_rows["SHAP_Contribution"].abs()
    local_rows = local_rows.sort_values(
        "Absolute_SHAP_Contribution", ascending=False, ignore_index=True
    )

    output_dir.mkdir(parents=True, exist_ok=True)
    results.to_csv(output_dir / "global_feature_importance.csv", index=False, float_format="%.8f")
    local_rows.to_csv(output_dir / "individual_shap_values.csv", index=False, float_format="%.8f")

    _save_global_plot(results, output_dir / "global_feature_importance.png")
    global_explanation = shap.Explanation(
        values=grouped_values[global_indices],
        base_values=base_values[global_indices],
        feature_names=FEATURE_COLUMNS,
    )
    plt.figure(figsize=(11, 7))
    shap.plots.bar(global_explanation, max_display=15, show=False)
    plt.tight_layout()
    plt.savefig(output_dir / "shap_global_summary.png", dpi=160, bbox_inches="tight")
    plt.close()

    local_explanation = shap.Explanation(
        values=local_values,
        base_values=local_base_value,
        data=x.iloc[row_index][FEATURE_COLUMNS].to_numpy(),
        feature_names=FEATURE_COLUMNS,
    )
    plt.figure(figsize=(11, 7))
    shap.plots.waterfall(local_explanation, max_display=15, show=False)
    plt.tight_layout()
    plt.savefig(output_dir / "shap_individual_prediction.png", dpi=160, bbox_inches="tight")
    plt.close()

    top_global = "\n".join(
        f"| {row.Feature} | {row.Mean_Absolute_SHAP:.2f} | {row.Mean_SHAP:.2f} |"
        for row in results.head(10).itertuples(index=False)
    )
    top_local = "\n".join(
        f"| `{row.Feature}` | {row.Value} | {row.SHAP_Contribution:+.2f} |"
        for row in local_rows.head(10).itertuples(index=False)
    )
    (output_dir / "phase9_report.md").write_text(
        f"""# Airlytics Phase 9 — Explainable AI

Generated by `python scripts/phase9_explainability.py`.

## Method

The selected Phase 8 model is **{artifact['model_name']}**, fitted on
{artifact['training_rows']:,} labeled observations. Tree SHAP values are
calculated on the fitted Random Forest using the transformed Phase 6 features.
Encoded columns (including one-hot categories) are grouped back to their
original input feature by summing their SHAP contributions per observation.
The global summary uses up to {len(global_indices):,} reproducibly selected
observations; the explained example is engineered dataset row {row_index}
(zero-based). The additivity check confirms each row's base value plus
contributions equals the model output.

## Global feature contributions

Mean absolute grouped SHAP is the average magnitude of a feature's contribution
over the global sample; mean SHAP preserves its average direction. These are
associations learned by the fitted model, not causal effects.

| Feature | Mean absolute SHAP | Mean SHAP |
|---|---:|---:|
{top_global}

See `global_feature_importance.csv` for all features and aggregated Random
Forest impurity importance, `global_feature_importance.png` for the comparison,
and `shap_global_summary.png` for the global mean-absolute SHAP summary.

## Individual prediction

| Item | Value |
|---|---:|
| Dataset row (zero-based) | {row_index} |
| Observed fare (source units) | {target.iloc[row_index]:,.2f} |
| Model prediction (source units) | {local_prediction:,.2f} |
| SHAP base value (source units) | {local_base_value:,.2f} |
| Sum of grouped SHAP contributions | {local_values.sum():,.2f} |

| Feature | Value | SHAP contribution (source units) |
|---|---|---:|
{top_local}

The local explanation is shown in `shap_individual_prediction.png`; all
feature-level contributions are in `individual_shap_values.csv`. Positive
contributions move this prediction above the model baseline; negative values
move it below.

## Limitations

The selected model was refitted on the complete labeled dataset after Phase 8
evaluation, so the example row is part of the model's training data; its
individual explanation is illustrative, not an independent test explanation.
The dataset contains historical 2019 fares, omits booking dates, and does not
specify currency. SHAP explains this model's learned associations and does not
establish causation or guarantee current prices.
""",
        encoding="utf-8",
    )
    return results


def _save_global_plot(results: pd.DataFrame, path: Path) -> None:
    displayed = results.head(15).sort_values("Mean_Absolute_SHAP")
    plt.figure(figsize=(10, 7))
    plt.barh(displayed["Feature"], displayed["Mean_Absolute_SHAP"], color="#2878B5")
    plt.xlabel("Mean absolute grouped SHAP value (fare source units)")
    plt.title("Global feature importance from SHAP")
    plt.tight_layout()
    plt.savefig(path, dpi=160, bbox_inches="tight")
    plt.close()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("outputs/phase6/engineered_fares.csv"),
        help="Path to the engineered fare CSV from Phase 6.",
    )
    parser.add_argument(
        "--model",
        type=Path,
        default=Path("outputs/phase8/models/selected_model.joblib"),
        help="Selected fitted model artifact from Phase 8.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("outputs/phase9"),
        help="Directory for global and individual explanation artifacts.",
    )
    parser.add_argument(
        "--row-index",
        type=int,
        default=0,
        help="Zero-based engineered dataset row to explain individually.",
    )
    parser.add_argument(
        "--max-samples",
        type=int,
        default=MAX_GLOBAL_SAMPLES,
        help="Maximum number of rows used for the global SHAP summary.",
    )
    args = parser.parse_args()
    if not args.input.is_file():
        raise FileNotFoundError(f"Engineered fare CSV not found: {args.input}. Run Phase 6 first.")

    results = explain_model(
        pd.read_csv(args.input),
        model_path=args.model,
        output_dir=args.output_dir,
        row_index=args.row_index,
        max_samples=args.max_samples,
    )
    print(results.head(10).to_string(index=False))
    print(f"Phase 9 explanations written to {args.output_dir}")


if __name__ == "__main__":
    main()
