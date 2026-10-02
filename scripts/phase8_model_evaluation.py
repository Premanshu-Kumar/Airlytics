"""Evaluate Phase 7 regression candidates with cross-validation and a holdout."""

from __future__ import annotations

import argparse
from pathlib import Path

import joblib
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import KFold, cross_val_score, train_test_split

if __package__:
    from .phase6_feature_engineering import FEATURE_COLUMNS, TARGET_COLUMN
    from .phase7_model_development import RANDOM_STATE, model_candidates
else:
    from phase6_feature_engineering import FEATURE_COLUMNS, TARGET_COLUMN
    from phase7_model_development import RANDOM_STATE, model_candidates


def evaluate_models(
    data: pd.DataFrame,
    output_dir: Path,
    test_size: float = 0.2,
    cv_folds: int = 5,
    random_state: int = RANDOM_STATE,
    candidates: dict | None = None,
) -> pd.DataFrame:
    """Select using training-only CV, evaluate the holdout, and save artifacts."""
    missing = sorted(set(FEATURE_COLUMNS + [TARGET_COLUMN]).difference(data.columns))
    if missing:
        raise ValueError(f"Engineered fare data is missing required columns: {missing}")
    if len(data) < 20:
        raise ValueError("At least 20 valid observations are required for evaluation.")
    if not 0 < test_size < 1:
        raise ValueError("--test-size must be greater than 0 and less than 1.")
    if cv_folds < 2:
        raise ValueError("--cv-folds must be at least 2.")

    x = data[FEATURE_COLUMNS]
    y = pd.to_numeric(data[TARGET_COLUMN], errors="coerce")
    if y.isna().any() or not np.isfinite(y.to_numpy()).all() or y.le(0).any():
        raise ValueError(f"`{TARGET_COLUMN}` must contain only finite, positive fares.")

    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=test_size, random_state=random_state
    )
    if cv_folds > len(x_train):
        raise ValueError(
            f"--cv-folds ({cv_folds}) cannot exceed training observations ({len(x_train)})."
        )

    models = candidates if candidates is not None else model_candidates()
    if not models:
        raise ValueError("At least one model candidate is required.")

    cv = KFold(n_splits=cv_folds, shuffle=True, random_state=random_state)
    rows = []
    predictions_by_model = {}
    for name, pipeline in models.items():
        cv_scores = -cross_val_score(
            pipeline,
            x_train,
            y_train,
            scoring="neg_mean_absolute_error",
            cv=cv,
            n_jobs=1,
            error_score="raise",
        )
        pipeline.fit(x_train, y_train)
        predictions = pipeline.predict(x_test)
        predictions_by_model[name] = predictions
        rows.append(
            {
                "Model": name,
                "CV_MAE_Mean": float(cv_scores.mean()),
                "CV_MAE_Std": float(cv_scores.std(ddof=1)) if len(cv_scores) > 1 else 0.0,
                "Holdout_MAE": mean_absolute_error(y_test, predictions),
                "Holdout_RMSE": np.sqrt(mean_squared_error(y_test, predictions)),
                "Holdout_R2": r2_score(y_test, predictions),
            }
        )

    results = pd.DataFrame(rows).sort_values("CV_MAE_Mean").reset_index(drop=True)
    selected_name = str(results.iloc[0]["Model"])
    selected_model = models[selected_name]
    selected_model.fit(x, y)
    selected_predictions = predictions_by_model[selected_name]
    residuals = y_test.to_numpy() - selected_predictions

    output_dir.mkdir(parents=True, exist_ok=True)
    model_dir = output_dir / "models"
    model_dir.mkdir(parents=True, exist_ok=True)
    results.insert(0, "CV_Rank", np.arange(1, len(results) + 1))
    results.to_csv(output_dir / "evaluation_metrics.csv", index=False, float_format="%.6f")
    pd.DataFrame(
        {
            "Actual_Fare_Source_Units": y_test.to_numpy(),
            "Predicted_Fare_Source_Units": selected_predictions,
            "Residual_Source_Units": residuals,
        }
    ).to_csv(output_dir / "selected_model_holdout_predictions.csv", index=False)
    joblib.dump(
        {
            "model_name": selected_name,
            "pipeline": selected_model,
            "feature_columns": FEATURE_COLUMNS,
            "target_column": TARGET_COLUMN,
            "random_state": random_state,
            "training_rows": len(data),
            "selection_metric": "mean cross-validated MAE on the training partition",
        },
        model_dir / "selected_model.joblib",
        compress=3,
    )

    _save_diagnostics(results, y_test, selected_predictions, residuals, output_dir)
    report_rows = "\n".join(
        (
            f"| {row.Model} | {row.CV_MAE_Mean:,.2f} ± {row.CV_MAE_Std:,.2f} "
            f"| {row.Holdout_MAE:,.2f} | {row.Holdout_RMSE:,.2f} "
            f"| {row.Holdout_R2:.4f} |"
        )
        for row in results.itertuples(index=False)
    )
    (output_dir / "phase8_report.md").write_text(
        f"""# Airlytics Phase 8 — Model Evaluation

Generated by `python scripts/phase8_model_evaluation.py`.

## Evaluation protocol

The {len(data):,} engineered observations were divided into an {1 - test_size:.0%}
training partition and a {test_size:.0%} held-out test partition using random
state {random_state}. Candidate pipelines were ranked only by the mean
absolute error from {cv_folds}-fold shuffled cross-validation on the training
partition. Each fold fits its own preprocessing pipeline. The held-out test
partition was not used to select the model.

After evaluation, the selected candidate (**{selected_name}**) was refitted on
all {len(data):,} labeled observations and saved as
`models/selected_model.joblib` for subsequent project phases. Holdout scores
below describe the pre-refit model and remain an unbiased final estimate for
this experiment.

## Candidate comparison

Errors are in dataset fare source units; the source does not specify currency.

| Model (ranked by CV MAE) | CV MAE (mean ± SD) | Holdout MAE | Holdout RMSE | Holdout R² |
|---|---:|---:|---:|---:|
{report_rows}

## Diagnostics

The prediction-level holdout results are in
`selected_model_holdout_predictions.csv`. The selected model's diagnostic
figures are `actual_vs_predicted.png`, `residual_distribution.png`, and
`residuals_vs_predicted.png`. Residual is actual fare minus predicted fare.

## Limitations

This is a random holdout evaluation of historical 2019 data, not a temporal
forecasting test or a guarantee of current market prices. The source does not
include booking dates or currency metadata. Future work should consider a
time-aware evaluation if representative collection dates become available.
""",
        encoding="utf-8",
    )
    return results


def _save_diagnostics(
    results: pd.DataFrame,
    actual: pd.Series,
    predictions: np.ndarray,
    residuals: np.ndarray,
    output_dir: Path,
) -> None:
    results_plot = results.sort_values("Holdout_MAE")
    positions = np.arange(len(results_plot))
    plt.figure(figsize=(9, 5))
    plt.bar(positions - 0.18, results_plot["Holdout_MAE"], width=0.36, label="MAE")
    plt.bar(positions + 0.18, results_plot["Holdout_RMSE"], width=0.36, label="RMSE")
    plt.xticks(positions, results_plot["Model"], rotation=20, ha="right")
    plt.ylabel("Error (fare source units)")
    plt.title("Holdout error by model")
    plt.legend()
    _save_current_figure(output_dir / "model_error_comparison.png")

    actual_values = actual.to_numpy()
    low = min(actual_values.min(), predictions.min())
    high = max(actual_values.max(), predictions.max())
    plt.figure(figsize=(7, 7))
    plt.scatter(actual_values, predictions, alpha=0.55, s=18)
    plt.plot([low, high], [low, high], linestyle="--", color="#D9534F")
    plt.xlabel("Actual fare (source units)")
    plt.ylabel("Predicted fare (source units)")
    plt.title("Selected model: actual vs predicted holdout fares")
    _save_current_figure(output_dir / "actual_vs_predicted.png")

    plt.figure(figsize=(8, 5))
    plt.hist(residuals, bins=40, color="#2878B5", edgecolor="white")
    plt.axvline(0, color="#D9534F", linestyle="--")
    plt.xlabel("Residual: actual − predicted (source units)")
    plt.ylabel("Flights")
    plt.title("Selected model: holdout residual distribution")
    _save_current_figure(output_dir / "residual_distribution.png")

    plt.figure(figsize=(8, 5))
    plt.scatter(predictions, residuals, alpha=0.55, s=18)
    plt.axhline(0, color="#D9534F", linestyle="--")
    plt.xlabel("Predicted fare (source units)")
    plt.ylabel("Residual: actual − predicted (source units)")
    plt.title("Selected model: residuals vs predicted fares")
    _save_current_figure(output_dir / "residuals_vs_predicted.png")


def _save_current_figure(path: Path) -> None:
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
        "--output-dir",
        type=Path,
        default=Path("outputs/phase8"),
        help="Directory for evaluation reports, diagnostics, and selected model.",
    )
    parser.add_argument(
        "--test-size",
        type=float,
        default=0.2,
        help="Fraction of observations reserved for the final holdout.",
    )
    parser.add_argument(
        "--cv-folds",
        type=int,
        default=5,
        help="Number of shuffled cross-validation folds within the training set.",
    )
    parser.add_argument("--random-state", type=int, default=RANDOM_STATE)
    args = parser.parse_args()
    if not args.input.is_file():
        raise FileNotFoundError(
            f"Engineered fare CSV not found: {args.input}. Run Phase 6 first."
        )

    results = evaluate_models(
        pd.read_csv(args.input),
        args.output_dir,
        test_size=args.test_size,
        cv_folds=args.cv_folds,
        random_state=args.random_state,
    )
    print(results.to_string(index=False))
    print(f"Selected model: {results.iloc[0]['Model']}")
    print(f"Phase 8 evaluation written to {args.output_dir}")


if __name__ == "__main__":
    main()
