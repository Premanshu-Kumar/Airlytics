import unittest
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

from scripts.phase6_feature_engineering import FEATURE_COLUMNS, TARGET_COLUMN, engineer_features
from scripts.phase7_model_development import make_pipeline
from scripts.phase8_model_evaluation import evaluate_models


def cleaned_rows():
    return pd.DataFrame(
        {
            "Airline": ["Air A", "Air B", "Air A"],
            "Journey_Date": ["2019-01-01", "2019-07-06", "2019-12-31"],
            "Source": ["Delhi", "Mumbai", "Delhi"],
            "Destination": ["Kolkata", "Pune", "Kolkata"],
            "Route": ["DEL → CCU", "BOM → PNQ", "DEL → IXR → CCU"],
            "Departure_Hour": [0.0, 12.5, 23.5],
            "Arrival_Hour": [4.0, 15.0, 2.0],
            "Duration_Minutes": [240, 150, 300],
            "Number_of_Stops": [0, 1, 2],
            "Additional_Info": ["No info", None, "Meal included"],
            "Fare_Source_Units": [5000, 6000, 7000],
        }
    )


class Phase6FeatureEngineeringTests(unittest.TestCase):
    def test_builds_date_time_route_and_stop_features_without_target_leakage(self):
        result = engineer_features(cleaned_rows())

        self.assertEqual(list(result.columns), FEATURE_COLUMNS + [TARGET_COLUMN])
        self.assertEqual(result["Season"].tolist(), ["Winter", "Monsoon", "Winter"])
        self.assertEqual(result["Is_Weekend"].tolist(), [0, 1, 0])
        self.assertEqual(result["Departure_Period"].tolist(), ["Night", "Afternoon", "Night"])
        self.assertEqual(result["Route_Leg_Count"].tolist(), [1, 1, 2])
        self.assertEqual(result["Stop_Category"].tolist(), ["Nonstop", "One stop", "Two or more stops"])
        self.assertEqual(result.loc[1, "Additional_Info"], "Unknown")
        self.assertNotIn("Fare_Source_Units", FEATURE_COLUMNS)
        self.assertTrue(np.isclose(result.loc[0, "Month_Sin"], 0))

    def test_invalid_required_data_is_rejected_with_csv_row(self):
        data = cleaned_rows()
        data.loc[1, "Departure_Hour"] = np.nan
        with self.assertRaisesRegex(ValueError, "CSV row\\(s\\) 3"):
            engineer_features(data)

    def test_model_pipeline_accepts_unseen_validation_categories(self):
        features = engineer_features(cleaned_rows())
        pipeline = make_pipeline(LinearRegression())
        pipeline.fit(features[FEATURE_COLUMNS].iloc[:2], features[TARGET_COLUMN].iloc[:2])
        prediction = pipeline.predict(features[FEATURE_COLUMNS].iloc[2:])

        self.assertEqual(len(prediction), 1)
        self.assertTrue(np.isfinite(prediction).all())

    def test_phase8_writes_holdout_metrics_diagnostics_and_full_data_model(self):
        base = cleaned_rows()
        data = engineer_features(pd.concat([base] * 8, ignore_index=True))
        data[TARGET_COLUMN] += np.arange(len(data)) * 13
        with tempfile.TemporaryDirectory() as temporary_dir:
            output_dir = Path(temporary_dir)
            results = evaluate_models(
                data,
                output_dir,
                test_size=0.25,
                cv_folds=2,
                candidates={"Linear Regression": make_pipeline(LinearRegression())},
            )

            self.assertEqual(results.loc[0, "Model"], "Linear Regression")
            self.assertGreater(results.loc[0, "CV_MAE_Mean"], 0)
            self.assertTrue((output_dir / "evaluation_metrics.csv").is_file())
            self.assertTrue((output_dir / "selected_model_holdout_predictions.csv").is_file())
            self.assertTrue((output_dir / "models" / "selected_model.joblib").is_file())
            self.assertTrue((output_dir / "actual_vs_predicted.png").is_file())
            self.assertTrue((output_dir / "residual_distribution.png").is_file())
            self.assertTrue((output_dir / "residuals_vs_predicted.png").is_file())

    def test_phase8_rejects_invalid_fold_count(self):
        data = engineer_features(pd.concat([cleaned_rows()] * 8, ignore_index=True))
        with self.assertRaisesRegex(ValueError, "--cv-folds must be at least 2"):
            evaluate_models(data, Path("unused"), cv_folds=1)


if __name__ == "__main__":
    unittest.main()
