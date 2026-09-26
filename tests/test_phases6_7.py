import unittest

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

from scripts.phase6_feature_engineering import FEATURE_COLUMNS, TARGET_COLUMN, engineer_features
from scripts.phase7_model_development import make_pipeline


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


if __name__ == "__main__":
    unittest.main()
