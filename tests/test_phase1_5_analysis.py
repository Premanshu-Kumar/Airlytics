import math
import unittest

from scripts.phase1_5_analysis import parse_duration, parse_hour, parse_stops


class ParseFlightFeatureTests(unittest.TestCase):
    def test_duration_is_converted_to_minutes(self):
        self.assertEqual(parse_duration("2h 50m"), 170)
        self.assertEqual(parse_duration("19h"), 1140)
        self.assertEqual(parse_duration("45m"), 45)

    def test_invalid_or_missing_duration_is_missing(self):
        self.assertTrue(math.isnan(parse_duration("unknown")))
        self.assertTrue(math.isnan(parse_duration(None)))

    def test_stop_count_supports_nonstop_and_numeric_labels(self):
        self.assertEqual(parse_stops("non-stop"), 0)
        self.assertEqual(parse_stops("2 stops"), 2)
        self.assertTrue(math.isnan(parse_stops("unknown")))

    def test_clock_time_is_decimal_hour(self):
        self.assertEqual(parse_hour("05:30"), 5.5)
        self.assertEqual(parse_hour("01:10 22 Mar"), 1 + 10 / 60)
        self.assertTrue(math.isnan(parse_hour("25:00")))
