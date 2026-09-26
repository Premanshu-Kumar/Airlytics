"""Train reproducible Phase 7 airfare regression model candidates."""

from __future__ import annotations

import argparse
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

if __package__:
    from .phase6_feature_engineering import FEATURE_COLUMNS, TARGET_COLUMN
else:
    from phase6_feature_engineering import FEATURE_COLUMNS, TARGET_COLUMN


RANDOM_STATE = 42
CATEGORICAL_FEATURES = [
    "Airline",
    "Source",
    "Destination",
    "Route",
    "Additional_Info",
    "Season",
    "Departure_Period",
    "Arrival_Period",
    "Stop_Category",
]
NUMERIC_FEATURES = [name for name in FEATURE_COLUMNS if name not in CATEGORICAL_FEATURES]


def make_pipeline(estimator: object) -> Pipeline:
    preprocessing = ColumnTransformer(
        transformers=[
            ("numeric", StandardScaler(), NUMERIC_FEATURES),
            (
                "categorical",
                OneHotEncoder(handle_unknown="ignore", min_frequency=2),
                CATEGORICAL_FEATURES,
            ),
        ],
        remainder="drop",
    )
    return Pipeline([("preprocessing", preprocessing), ("regressor", estimator)])


def model_candidates() -> dict[str, Pipeline]:
    try:
        from xgboost import XGBRegressor
    except ImportError as error:
        raise ImportError(
            "XGBoost is required for Phase 7. Install it with "
            "`python -m pip install -r requirements-modeling.txt`."
        ) from error

    return {
        "Linear Regression": make_pipeline(LinearRegression()),
        "Random Forest": make_pipeline(
            RandomForestRegressor(
                n_estimators=180,
                max_depth=24,
                min_samples_leaf=2,
                max_features=0.8,
                n_jobs=-1,
                random_state=RANDOM_STATE,
            )
        ),
        "XGBoost": make_pipeline(
            XGBRegressor(
                n_estimators=350,
                max_depth=6,
                learning_rate=0.05,
                subsample=0.8,
                colsample_bytree=0.8,
                reg_lambda=1.0,
                objective="reg:squarederror",
                eval_metric="rmse",
                tree_method="hist",
                n_jobs=-1,
                random_state=RANDOM_STATE,
            )
        ),
    }


def train_models(
    data: pd.DataFrame,
    output_dir: Path,
    test_size: float = 0.2,
    random_state: int = RANDOM_STATE,
) -> pd.DataFrame:
    missing = sorted(set(FEATURE_COLUMNS + [TARGET_COLUMN]).difference(data.columns))
    if missing:
        raise ValueError(f"Engineered fare data is missing required columns: {missing}")
    if len(data) < 20:
        raise ValueError("At least 20 valid observations are required for a train/validation split.")
    if not 0 < test_size < 1:
        raise ValueError("--test-size must be greater than 0 and less than 1.")

    x = data[FEATURE_COLUMNS]
    y = pd.to_numeric(data[TARGET_COLUMN], errors="coerce")
    if y.isna().any() or not np.isfinite(y.to_numpy()).all() or y.le(0).any():
        raise ValueError(f"`{TARGET_COLUMN}` must contain only finite, positive fares.")

    x_train, x_validation, y_train, y_validation = train_test_split(
        x, y, test_size=test_size, random_state=random_state
    )
    model_dir = output_dir / "models"
    model_dir.mkdir(parents=True, exist_ok=True)
    rows = []

    for name, pipeline in model_candidates().items():
        pipeline.fit(x_train, y_train)
        predictions = pipeline.predict(x_validation)
        rows.append(
            {
                "Model": name,
                "MAE": mean_absolute_error(y_validation, predictions),
                "RMSE": np.sqrt(mean_squared_error(y_validation, predictions)),
                "R2": r2_score(y_validation, predictions),
            }
        )
        slug = name.lower().replace(" ", "_")
        joblib.dump(
            {
                "model_name": name,
                "pipeline": pipeline,
                "feature_columns": FEATURE_COLUMNS,
                "target_column": TARGET_COLUMN,
                "random_state": random_state,
                "validation_fraction": test_size,
            },
            model_dir / f"{slug}.joblib",
            compress=3,
        )

    results = pd.DataFrame(rows).sort_values("MAE").reset_index(drop=True)
    output_dir.mkdir(parents=True, exist_ok=True)
    results.to_csv(output_dir / "validation_metrics.csv", index=False, float_format="%.6f")
    report_rows = "\n".join(
        f"| {row.Model} | {row.MAE:,.2f} | {row.RMSE:,.2f} | {row.R2:.4f} |"
        for row in results.itertuples(index=False)
    )
    (output_dir / "phase7_report.md").write_text(
        f"""# Airlytics Phase 7 — Model Development

Generated by `python scripts/phase7_model_development.py`.

Three regression candidates were trained on the engineered Phase 6 features.
A reproducible random split (random state {random_state}) reserved
{test_size:.0%} of {len(data):,} observations for a development validation
set. Categorical encoding and numeric scaling are fitted inside each training
pipeline, so validation rows do not influence preprocessing. Unseen validation
categories are handled by the fitted one-hot encoder.

## Development validation results

| Model | MAE (source units) | RMSE (source units) | R² |
|---|---:|---:|---:|
{report_rows}

These scores are preliminary development results, not a final unbiased
performance claim or a current-fare guarantee. All three trained pipelines
are retained in `models/`; final model selection and broader evaluation belong
to Phase 8.
""",
        encoding="utf-8",
    )
    return results


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
        default=Path("outputs/phase7"),
        help="Directory for model artifacts and validation results.",
    )
    parser.add_argument(
        "--test-size",
        type=float,
        default=0.2,
        help="Fraction of observations reserved for development validation.",
    )
    parser.add_argument("--random-state", type=int, default=RANDOM_STATE)
    args = parser.parse_args()
    if not args.input.is_file():
        raise FileNotFoundError(
            f"Engineered fare CSV not found: {args.input}. Run Phase 6 first."
        )

    results = train_models(
        pd.read_csv(args.input),
        args.output_dir,
        test_size=args.test_size,
        random_state=args.random_state,
    )
    print(results.to_string(index=False))
    print(f"Phase 7 models and results written to {args.output_dir}")


if __name__ == "__main__":
    main()
