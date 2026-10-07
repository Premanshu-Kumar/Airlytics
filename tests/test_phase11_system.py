"""Airlytics Phase 11 - System & Integration Tests.

Covers:
  - Valid inputs: well-formed flight configurations produce a finite positive fare.
  - Missing / blank inputs: empty required strings raise ValueError.
  - Unknown categories: airline / route / additional-info values unseen during
    training are handled gracefully (no crash, finite prediction).
  - Boundary values: extremes of numerical inputs (duration, stops, hours, dates).
  - Different routes: nonstop, one-stop and multi-stop routes each produce a fare.
  - Different booking windows: Journey_Month variation drives Month_Sin/Cos change.

Run with:
    python -m pytest tests/test_phase11_system.py -v
or
    python -m unittest tests.test_phase11_system
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT / "scripts"))
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.phase6_feature_engineering import FEATURE_COLUMNS, TARGET_COLUMN, engineer_features
from scripts.phase7_model_development import make_pipeline


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------

def _cleaned_rows() -> pd.DataFrame:
    """Minimal cleaned-fare table covering all seasons and stop categories."""
    return pd.DataFrame(
        {
            "Airline": [
                "IndiGo", "Air India", "SpiceJet", "Vistara", "GoAir",
                "IndiGo", "Air India", "SpiceJet",
            ],
            "Journey_Date": [
                "2019-01-15",
                "2019-04-10",
                "2019-07-20",
                "2019-10-05",
                "2019-12-31",
                "2019-03-01",
                "2019-09-01",
                "2019-11-01",
            ],
            "Source": [
                "Delhi", "Mumbai", "Bangalore", "Chennai", "Kolkata",
                "Delhi", "Mumbai", "Bangalore",
            ],
            "Destination": [
                "Kolkata", "Delhi", "Delhi", "Delhi", "Delhi",
                "Kolkata", "Delhi", "Delhi",
            ],
            "Route": [
                "DEL → CCU",
                "BOM → DEL",
                "BLR → DEL",
                "MAA → DEL",
                "CCU → DEL",
                "DEL → CCU",
                "BOM → PNQ → DEL",
                "BLR → BOM → DEL",
            ],
            "Departure_Hour": [6.0, 10.0, 14.0, 18.0, 22.0, 0.0, 8.5, 16.0],
            "Arrival_Hour": [8.5, 12.0, 16.5, 21.0, 23.5, 4.0, 13.5, 20.0],
            "Duration_Minutes": [150, 120, 150, 180, 90, 240, 300, 240],
            "Number_of_Stops": [0, 0, 0, 0, 0, 0, 1, 1],
            "Additional_Info": [
                "No info", "No Info", "In-flight meal not included",
                "No info", "No Info", "No info", "1 Short layover", "1 Long layover",
            ],
            TARGET_COLUMN: [5000, 7500, 6200, 8000, 4800, 5200, 9000, 8500],
        }
    )


def _trained_pipeline(n_rows: int = 80) -> object:
    """Return a pipeline fitted on synthetic expanded data for unit-testing."""
    base = _cleaned_rows()
    # Use arrow symbol consistent with the app
    data = engineer_features(
        pd.concat([base] * (n_rows // len(base) + 1), ignore_index=True)
        .assign(Route=lambda df: df["Route"].str.replace("->", "->", regex=False))
    )
    data = data.iloc[:n_rows].copy()
    data[TARGET_COLUMN] = data[TARGET_COLUMN] + np.arange(len(data)) * 50
    pipeline = make_pipeline(
        RandomForestRegressor(n_estimators=20, max_depth=5, random_state=42)
    )
    pipeline.fit(data[FEATURE_COLUMNS], data[TARGET_COLUMN])
    return pipeline


def _build_user_row(**kwargs):
    """Thin wrapper around app.build_user_row with sensible defaults."""
    import importlib.util, sys as _sys
    from app.app import build_user_row
    defaults = dict(
        airline="IndiGo",
        source="Delhi",
        destination="Kolkata",
        route="DEL → CCU",
        additional_info="No info",
        journey_date=pd.Timestamp("2019-06-15"),
        departure_hour=9.0,
        arrival_hour=11.5,
        duration_minutes=150.0,
        number_of_stops=0,
    )
    defaults.update(kwargs)
    return build_user_row(**defaults)


# ---------------------------------------------------------------------------
# 1. Valid inputs
# ---------------------------------------------------------------------------

class ValidInputTests(unittest.TestCase):
    """Well-formed inputs must produce a finite, positive predicted fare."""

    @classmethod
    def setUpClass(cls):
        cls.pipeline = _trained_pipeline()

    def _predict(self, **overrides) -> float:
        row = _build_user_row(**overrides)
        return float(self.pipeline.predict(row[FEATURE_COLUMNS])[0])

    def test_standard_nonstop_indigo_returns_finite_positive_fare(self):
        fare = self._predict()
        self.assertTrue(np.isfinite(fare))
        self.assertGreater(fare, 0)

    def test_air_india_one_stop_returns_finite_positive_fare(self):
        fare = self._predict(
            airline="Air India",
            route="BOM → PNQ → DEL",
            source="Mumbai",
            destination="Delhi",
            number_of_stops=1,
            duration_minutes=300,
        )
        self.assertTrue(np.isfinite(fare))
        self.assertGreater(fare, 0)

    def test_spicejet_route_returns_finite_positive_fare(self):
        fare = self._predict(
            airline="SpiceJet",
            source="Bangalore",
            destination="Delhi",
            route="BLR → DEL",
        )
        self.assertTrue(np.isfinite(fare))
        self.assertGreater(fare, 0)

    def test_prediction_is_scalar_float(self):
        fare = self._predict()
        self.assertIsInstance(fare, float)

    def test_journey_in_all_four_seasons_produces_finite_fare(self):
        for date in ["2019-01-15", "2019-04-15", "2019-08-01", "2019-10-15"]:
            with self.subTest(date=date):
                fare = self._predict(journey_date=pd.Timestamp(date))
                self.assertTrue(np.isfinite(fare))
                self.assertGreater(fare, 0)

    def test_vistara_premium_economy_returns_finite_fare(self):
        fare = self._predict(airline="Vistara Premium economy")
        self.assertTrue(np.isfinite(fare))

    def test_no_info_additional_info_returns_finite_fare(self):
        fare = self._predict(additional_info="No Info")
        self.assertTrue(np.isfinite(fare))


# ---------------------------------------------------------------------------
# 2. Missing / blank inputs
# ---------------------------------------------------------------------------

class MissingInputTests(unittest.TestCase):
    """Missing or blank required fields must raise ValueError."""

    def test_blank_airline_raises_value_error(self):
        with self.assertRaises(ValueError):
            _build_user_row(airline="")

    def test_blank_source_raises_value_error(self):
        with self.assertRaises(ValueError):
            _build_user_row(source="")

    def test_blank_destination_raises_value_error(self):
        with self.assertRaises(ValueError):
            _build_user_row(destination="")

    def test_blank_route_raises_value_error(self):
        with self.assertRaises(ValueError):
            _build_user_row(route="")

    def test_zero_duration_raises_value_error(self):
        with self.assertRaises(ValueError):
            _build_user_row(duration_minutes=0.0)

    def test_negative_duration_raises_value_error(self):
        with self.assertRaises(ValueError):
            _build_user_row(duration_minutes=-60.0)

    def test_negative_stops_raises_value_error(self):
        with self.assertRaises(ValueError):
            _build_user_row(number_of_stops=-1)

    def test_departure_hour_24_raises_value_error(self):
        with self.assertRaises(ValueError):
            _build_user_row(departure_hour=24.0)

    def test_arrival_hour_24_raises_value_error(self):
        with self.assertRaises(ValueError):
            _build_user_row(arrival_hour=24.0)

    def test_departure_hour_negative_raises_value_error(self):
        with self.assertRaises(ValueError):
            _build_user_row(departure_hour=-1.0)

    def test_arrival_hour_negative_raises_value_error(self):
        with self.assertRaises(ValueError):
            _build_user_row(arrival_hour=-0.1)


# ---------------------------------------------------------------------------
# 3. Unknown categories
# ---------------------------------------------------------------------------

class UnknownCategoryTests(unittest.TestCase):
    """Values unseen during training must not crash the pipeline."""

    @classmethod
    def setUpClass(cls):
        cls.pipeline = _trained_pipeline()

    def _predict_with_unknown(self, **overrides) -> float:
        row = _build_user_row(**overrides)
        return float(self.pipeline.predict(row[FEATURE_COLUMNS])[0])

    def test_unseen_airline_produces_finite_fare(self):
        fare = self._predict_with_unknown(airline="NewAir Express")
        self.assertTrue(np.isfinite(fare))

    def test_unseen_route_produces_finite_fare(self):
        fare = self._predict_with_unknown(
            source="Delhi",
            destination="Kolkata",
            route="DEL → VNS → CCU",
            number_of_stops=1,
        )
        self.assertTrue(np.isfinite(fare))

    def test_unseen_additional_info_produces_finite_fare(self):
        fare = self._predict_with_unknown(additional_info="Priority boarding included")
        self.assertTrue(np.isfinite(fare))

    def test_unseen_source_city_produces_finite_fare(self):
        fare = self._predict_with_unknown(
            source="Ahmedabad",
            route="AMD → CCU",
        )
        self.assertTrue(np.isfinite(fare))

    def test_unseen_destination_city_produces_finite_fare(self):
        fare = self._predict_with_unknown(
            destination="Goa",
            route="DEL → GOI",
        )
        self.assertTrue(np.isfinite(fare))


# ---------------------------------------------------------------------------
# 4. Boundary values
# ---------------------------------------------------------------------------

class BoundaryValueTests(unittest.TestCase):
    """Extreme but valid inputs at numeric boundaries must produce finite fares."""

    @classmethod
    def setUpClass(cls):
        cls.pipeline = _trained_pipeline()

    def _predict(self, **overrides) -> float:
        row = _build_user_row(**overrides)
        return float(self.pipeline.predict(row[FEATURE_COLUMNS])[0])

    def test_minimum_duration_15_minutes(self):
        fare = self._predict(duration_minutes=15.0)
        self.assertTrue(np.isfinite(fare))
        self.assertGreater(fare, 0)

    def test_maximum_duration_2400_minutes(self):
        fare = self._predict(duration_minutes=2400.0)
        self.assertTrue(np.isfinite(fare))
        self.assertGreater(fare, 0)

    def test_departure_hour_zero(self):
        fare = self._predict(departure_hour=0.0, arrival_hour=2.0)
        self.assertTrue(np.isfinite(fare))

    def test_departure_hour_just_below_24(self):
        fare = self._predict(departure_hour=23.9, arrival_hour=2.0)
        self.assertTrue(np.isfinite(fare))

    def test_arrival_hour_zero(self):
        fare = self._predict(departure_hour=22.0, arrival_hour=0.0)
        self.assertTrue(np.isfinite(fare))

    def test_arrival_hour_just_below_24(self):
        fare = self._predict(departure_hour=0.0, arrival_hour=23.9)
        self.assertTrue(np.isfinite(fare))

    def test_zero_stops_nonstop(self):
        fare = self._predict(number_of_stops=0)
        self.assertTrue(np.isfinite(fare))

    def test_four_stops_maximum(self):
        fare = self._predict(
            route="DEL → BOM → HYD → MAA → COK → CCU",
            number_of_stops=4,
        )
        self.assertTrue(np.isfinite(fare))

    def test_january_1_boundary_date(self):
        fare = self._predict(journey_date=pd.Timestamp("2019-01-01"))
        self.assertTrue(np.isfinite(fare))

    def test_december_31_boundary_date(self):
        fare = self._predict(journey_date=pd.Timestamp("2019-12-31"))
        self.assertTrue(np.isfinite(fare))

    def test_midnight_departure_is_night_period(self):
        row = _build_user_row(departure_hour=0.0, arrival_hour=2.5, duration_minutes=150.0)
        self.assertEqual(row["Departure_Period"].iloc[0], "Night")

    def test_noon_departure_is_afternoon_period(self):
        row = _build_user_row(departure_hour=12.0, arrival_hour=14.0, duration_minutes=120.0)
        self.assertEqual(row["Departure_Period"].iloc[0], "Afternoon")

    def test_early_morning_departure_is_morning_period(self):
        row = _build_user_row(departure_hour=6.0, arrival_hour=8.0, duration_minutes=120.0)
        self.assertEqual(row["Departure_Period"].iloc[0], "Morning")

    def test_evening_departure_is_evening_period(self):
        row = _build_user_row(departure_hour=17.0, arrival_hour=19.0, duration_minutes=120.0)
        self.assertEqual(row["Departure_Period"].iloc[0], "Evening")


# ---------------------------------------------------------------------------
# 5. Different routes
# ---------------------------------------------------------------------------

class DifferentRouteTests(unittest.TestCase):
    """Nonstop, one-stop and multi-stop routes must each return a finite fare."""

    @classmethod
    def setUpClass(cls):
        cls.pipeline = _trained_pipeline()

    def _predict(self, route: str, number_of_stops: int, **overrides) -> float:
        kw = dict(
            airline="IndiGo",
            source="Delhi",
            destination="Kolkata",
            additional_info="No info",
            journey_date=pd.Timestamp("2019-06-15"),
            departure_hour=9.0,
            arrival_hour=11.5,
            duration_minutes=150.0,
        )
        kw.update(overrides)
        row = _build_user_row(route=route, number_of_stops=number_of_stops, **kw)
        return float(self.pipeline.predict(row[FEATURE_COLUMNS])[0])

    def test_nonstop_direct_route(self):
        fare = self._predict("DEL → CCU", number_of_stops=0)
        self.assertTrue(np.isfinite(fare))
        self.assertGreater(fare, 0)

    def test_one_stop_via_varanasi(self):
        fare = self._predict("DEL → VNS → CCU", number_of_stops=1)
        self.assertTrue(np.isfinite(fare))
        self.assertGreater(fare, 0)

    def test_two_stop_longer_route(self):
        fare = self._predict(
            "DEL → BOM → HYD → CCU",
            number_of_stops=2,
            duration_minutes=480,
        )
        self.assertTrue(np.isfinite(fare))
        self.assertGreater(fare, 0)

    def test_three_stop_route(self):
        fare = self._predict(
            "DEL → BOM → HYD → MAA → CCU",
            number_of_stops=3,
            duration_minutes=720,
        )
        self.assertTrue(np.isfinite(fare))
        self.assertGreater(fare, 0)

    def test_nonstop_route_leg_count_is_one(self):
        row = _build_user_row(route="DEL → CCU", number_of_stops=0)
        self.assertEqual(int(row["Route_Leg_Count"].iloc[0]), 1)

    def test_one_stop_route_leg_count_is_two(self):
        row = _build_user_row(
            route="DEL → VNS → CCU",
            number_of_stops=1,
            arrival_hour=14.0,
            duration_minutes=300.0,
        )
        self.assertEqual(int(row["Route_Leg_Count"].iloc[0]), 2)

    def test_different_source_destination_pairs(self):
        pairs = [
            ("BOM → DEL", "Mumbai", "Delhi", 0),
            ("BLR → DEL", "Bangalore", "Delhi", 0),
            ("CCU → BOM", "Kolkata", "Mumbai", 0),
        ]
        for route, src, dst, stops in pairs:
            with self.subTest(route=route):
                fare = self._predict(
                    route=route,
                    number_of_stops=stops,
                    source=src,
                    destination=dst,
                )
                self.assertTrue(np.isfinite(fare))
                self.assertGreater(fare, 0)

    def test_stop_category_nonstop(self):
        row = _build_user_row(route="DEL → CCU", number_of_stops=0)
        self.assertEqual(row["Stop_Category"].iloc[0], "Nonstop")

    def test_stop_category_one_stop(self):
        row = _build_user_row(
            route="DEL → VNS → CCU", number_of_stops=1,
            arrival_hour=14.0, duration_minutes=300.0,
        )
        self.assertEqual(row["Stop_Category"].iloc[0], "One stop")

    def test_stop_category_two_or_more_stops(self):
        row = _build_user_row(
            route="DEL → BOM → HYD → CCU", number_of_stops=2,
            arrival_hour=18.0, duration_minutes=540.0,
        )
        self.assertEqual(row["Stop_Category"].iloc[0], "Two or more stops")


# ---------------------------------------------------------------------------
# 6. Different booking windows (Journey_Month drives Month_Sin/Cos)
# ---------------------------------------------------------------------------

class BookingWindowTests(unittest.TestCase):
    """Journey month variation must propagate through cyclical encodings."""

    @classmethod
    def setUpClass(cls):
        cls.pipeline = _trained_pipeline()

    def _build_row(self, journey_date: str) -> pd.DataFrame:
        return _build_user_row(journey_date=pd.Timestamp(journey_date))

    def test_january_month_sin_is_zero(self):
        row = self._build_row("2019-01-15")
        self.assertAlmostEqual(float(row["Month_Sin"].iloc[0]), 0.0, places=10)

    def test_april_month_sin_is_one(self):
        row = self._build_row("2019-04-15")
        self.assertAlmostEqual(float(row["Month_Sin"].iloc[0]), 1.0, places=10)

    def test_july_month_sin_is_zero_and_cos_is_negative(self):
        row = self._build_row("2019-07-15")
        self.assertAlmostEqual(float(row["Month_Sin"].iloc[0]), 0.0, places=10)
        self.assertAlmostEqual(float(row["Month_Cos"].iloc[0]), -1.0, places=10)

    def test_month_sin_cos_for_all_twelve_months_are_in_range(self):
        for month in range(1, 13):
            date = f"2019-{month:02d}-15"
            row = self._build_row(date)
            sin_val = float(row["Month_Sin"].iloc[0])
            cos_val = float(row["Month_Cos"].iloc[0])
            with self.subTest(month=month):
                self.assertGreaterEqual(sin_val, -1.0 - 1e-9)
                self.assertLessEqual(sin_val, 1.0 + 1e-9)
                self.assertGreaterEqual(cos_val, -1.0 - 1e-9)
                self.assertLessEqual(cos_val, 1.0 + 1e-9)

    def test_season_labels_correct_for_all_months(self):
        expected = {
            1: "Winter", 2: "Winter", 3: "Summer", 4: "Summer",
            5: "Summer", 6: "Summer", 7: "Monsoon", 8: "Monsoon",
            9: "Monsoon", 10: "Post-Monsoon", 11: "Post-Monsoon", 12: "Winter",
        }
        for month, season in expected.items():
            with self.subTest(month=month):
                row = self._build_row(f"2019-{month:02d}-15")
                self.assertEqual(row["Season"].iloc[0], season)

    def test_summer_and_winter_journeys_both_return_finite_fares(self):
        for date in ["2019-01-15", "2019-06-01"]:
            with self.subTest(date=date):
                row = self._build_row(date)
                fare = float(self.pipeline.predict(row[FEATURE_COLUMNS])[0])
                self.assertTrue(np.isfinite(fare))
                self.assertGreater(fare, 0)

    def test_weekend_indicator_correct_for_saturday(self):
        row = self._build_row("2019-01-05")  # Saturday
        self.assertEqual(int(row["Is_Weekend"].iloc[0]), 1)

    def test_weekend_indicator_correct_for_monday(self):
        row = self._build_row("2019-01-07")  # Monday
        self.assertEqual(int(row["Is_Weekend"].iloc[0]), 0)

    def test_different_months_produce_different_month_sin(self):
        jan = float(self._build_row("2019-01-15")["Month_Sin"].iloc[0])
        jun = float(self._build_row("2019-06-15")["Month_Sin"].iloc[0])
        self.assertNotAlmostEqual(jan, jun, places=5)


# ---------------------------------------------------------------------------
# 7. Route-city consistency helpers
# ---------------------------------------------------------------------------

class RouteConsistencyTests(unittest.TestCase):
    """validate_stops_match_route and route helper functions."""

    def test_nonstop_route_and_zero_stops_is_consistent(self):
        from app.app import validate_stops_match_route
        self.assertIsNone(validate_stops_match_route(0, "DEL → CCU"))

    def test_one_stop_route_and_one_stop_is_consistent(self):
        from app.app import validate_stops_match_route
        self.assertIsNone(validate_stops_match_route(1, "DEL → VNS → CCU"))

    def test_nonstop_route_with_one_stop_selected_returns_message(self):
        from app.app import validate_stops_match_route
        result = validate_stops_match_route(1, "DEL → CCU")
        self.assertIsNotNone(result)
        self.assertIn("1", result)

    def test_route_shorter_than_two_airports_returns_message(self):
        from app.app import validate_stops_match_route
        result = validate_stops_match_route(0, "DEL")
        self.assertIsNotNone(result)

    def test_empty_route_returns_none(self):
        from app.app import validate_stops_match_route
        self.assertIsNone(validate_stops_match_route(0, ""))

    def test_route_matches_cities_correct_pair(self):
        from app.app import route_matches_cities
        self.assertTrue(route_matches_cities("DEL → CCU", "Delhi", "Kolkata"))

    def test_route_matches_cities_wrong_source(self):
        from app.app import route_matches_cities
        self.assertFalse(route_matches_cities("BOM → DEL", "Delhi", "Delhi"))

    def test_suggest_route_returns_nonstop_when_present(self):
        from app.app import suggest_route
        routes = ["DEL → CCU", "DEL → VNS → CCU", "BOM → DEL"]
        result = suggest_route("Delhi", "Kolkata", routes)
        self.assertEqual(result, "DEL → CCU")

    def test_suggest_route_falls_back_to_first_matching_route(self):
        from app.app import suggest_route
        routes = ["DEL → VNS → CCU", "BOM → DEL"]
        result = suggest_route("Delhi", "Kolkata", routes)
        self.assertEqual(result, "DEL → VNS → CCU")

    def test_routes_for_city_pair_filters_correctly(self):
        from app.app import routes_for_city_pair
        routes = ["DEL → CCU", "DEL → VNS → CCU", "BOM → DEL"]
        result = routes_for_city_pair("Delhi", "Kolkata", routes)
        self.assertIn("DEL → CCU", result)
        self.assertIn("DEL → VNS → CCU", result)
        self.assertNotIn("BOM → DEL", result)


# ---------------------------------------------------------------------------
# 8. Feature engineering contract
# ---------------------------------------------------------------------------

class FeatureEngineeringContractTests(unittest.TestCase):
    """engineer_features output schema and value contracts."""

    @classmethod
    def setUpClass(cls):
        cls.df = engineer_features(_cleaned_rows())

    def test_output_columns_match_feature_columns_plus_target(self):
        self.assertEqual(list(self.df.columns), FEATURE_COLUMNS + [TARGET_COLUMN])

    def test_no_nulls_in_engineered_features(self):
        self.assertFalse(self.df[FEATURE_COLUMNS].isnull().any().any())

    def test_stop_category_values_are_valid(self):
        valid = {"Nonstop", "One stop", "Two or more stops"}
        for val in self.df["Stop_Category"]:
            self.assertIn(val, valid)

    def test_is_weekend_is_binary(self):
        self.assertTrue(self.df["Is_Weekend"].isin([0, 1]).all())

    def test_month_sin_cos_are_in_valid_range(self):
        self.assertTrue((self.df["Month_Sin"].between(-1.0, 1.0)).all())
        self.assertTrue((self.df["Month_Cos"].between(-1.0, 1.0)).all())

    def test_departure_period_values_are_valid(self):
        valid = {"Night", "Morning", "Afternoon", "Evening"}
        for val in self.df["Departure_Period"]:
            self.assertIn(val, valid)

    def test_target_column_excluded_from_feature_columns(self):
        self.assertNotIn(TARGET_COLUMN, FEATURE_COLUMNS)

    def test_missing_additional_info_becomes_unknown(self):
        rows = _cleaned_rows()
        rows.loc[0, "Additional_Info"] = None
        df = engineer_features(rows)
        self.assertEqual(df.loc[0, "Additional_Info"], "Unknown")

    def test_blank_additional_info_becomes_unknown(self):
        rows = _cleaned_rows()
        rows.loc[0, "Additional_Info"] = ""
        df = engineer_features(rows)
        self.assertEqual(df.loc[0, "Additional_Info"], "Unknown")

    def test_duration_minutes_preserved_correctly(self):
        self.assertEqual(self.df.loc[0, "Duration_Minutes"], 150)

    def test_route_leg_count_one_for_nonstop(self):
        self.assertEqual(self.df.loc[0, "Route_Leg_Count"], 1)

    def test_route_leg_count_two_for_one_stop(self):
        # Row 6 is BOM → PNQ → DEL (one stop, two legs)
        self.assertEqual(self.df.loc[6, "Route_Leg_Count"], 2)


if __name__ == "__main__":
    unittest.main()




