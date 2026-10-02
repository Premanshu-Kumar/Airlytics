import unittest

from streamlit.testing.v1 import AppTest


APP_PATH = "app/app.py"


class Phase10AppTests(unittest.TestCase):
    def setUp(self):
        self.app = AppTest.from_file(APP_PATH, default_timeout=120).run()

    def _selectbox(self, label):
        return next(widget for widget in self.app.selectbox if widget.label == label)

    def test_route_and_additional_info_options_match_training_data(self):
        source = self._selectbox("Source city").value
        destination = self._selectbox("Destination city").value
        route = self._selectbox("Route (airport codes with layovers)")
        airports = [part.strip() for part in route.value.split("→")]

        self.assertGreaterEqual(len(route.options), 1)
        self.assertEqual(airports[0], {"Bangalore": "BLR"}.get(source, source[:3].upper()))
        self.assertEqual(
            airports[-1],
            {"Cochin": "COK", "Delhi": "DEL", "New Delhi": "DEL"}.get(
                destination, destination[:3].upper()
            ),
        )
        self.assertIn("No Info", self._selectbox("Additional info").options)
        self.assertIn("No info", self._selectbox("Additional info").options)
        self.assertEqual(self.app.warning, [])
        self.assertEqual(self.app.error, [])

    def test_changing_city_pair_refreshes_compatible_routes(self):
        self._selectbox("Source city").select("Mumbai").run()
        self._selectbox("Destination city").select("Cochin").run()

        source = self._selectbox("Source city").value
        destination = self._selectbox("Destination city").value
        route = self._selectbox("Route (airport codes with layovers)")
        airports = [part.strip() for part in route.value.split("→")]

        self.assertEqual(source, "Mumbai")
        self.assertEqual(destination, "Cochin")
        self.assertEqual(airports[0], "BOM")
        self.assertEqual(airports[-1], "COK")
        self.assertTrue(
            all(
                option.split("→")[0].strip() == "BOM"
                and option.split("→")[-1].strip() == "COK"
                for option in route.options
            )
        )

    def test_inconsistent_stop_count_blocks_estimate(self):
        self._selectbox("Number of stops").select("2").run()
        self.assertTrue(self.app.warning)

        next(button for button in self.app.button if button.label.endswith("Estimate fare")).click().run()

        self.assertTrue(any("Correct the route and stop count" in error.value for error in self.app.error))
        self.assertEqual(self.app.metric, [])

    def test_valid_estimate_displays_fare_without_runtime_errors(self):
        next(button for button in self.app.button if button.label.endswith("Estimate fare")).click().run()

        self.assertEqual(self.app.exception, [])
        self.assertEqual(self.app.error, [])
        self.assertEqual(self.app.warning, [])
        self.assertEqual(len(self.app.metric), 1)
        self.assertEqual(self.app.metric[0].label, "Estimated fare (source units)")


if __name__ == "__main__":
    unittest.main()
