# Airlytics dataset

## Source and license

- **Name:** Flight Price Prediction DataSet, version 1
- **Publisher:** Jillani SofTech
- **Dataset page:** https://www.kaggle.com/datasets/jillanisofttech/flight-price-prediction-dataset
- **Publisher description:** Says the flight-booking data was obtained from the EaseMyTrip website.
- **License displayed on Kaggle:** CC0: Public Domain
- **Download date:** 2026-09-26

The two original workbooks are preserved in `data/raw/`. The analysis uses
`Data_Train.xlsx`, which contains the observed `Price` target. The companion
`Test_set.xlsx` contains 2,671 rows and no target, so it is retained for source
completeness but excluded from fare analysis and model training.

## Schema

`Data_Train.xlsx` contains 10,683 rows and 11 columns:

| Column | Meaning | Type / notes |
|---|---|---|
| `Airline` | Airline label | Categorical |
| `Date_of_Journey` | Journey date | `d/m/YYYY` string |
| `Source` | Departure city | Categorical; source includes the spelling `Banglore` |
| `Destination` | Arrival city | Categorical |
| `Route` | Route via airport codes | Text |
| `Dep_Time` | Departure clock time | `HH:MM` |
| `Arrival_Time` | Arrival time, sometimes with date text | Text |
| `Duration` | Flight duration | Text such as `2h 50m` |
| `Total_Stops` | Number of stops | Text such as `non-stop` or `2 stops` |
| `Additional_Info` | Additional listing information | Categorical/text |
| `Price` | Observed fare | Numeric target; currency is not stated in the dataset metadata |

## Limitations

The data describes historical fares, not current availability or future prices.
The source metadata does not specify the extraction method, observation-level
collection dates, currency, fare class, included taxes/fees, or booking date.
Consequently booking-window effects cannot be studied, and observed differences
must not be interpreted as causal. The companion test workbook has no fare
labels and is not used to compute statistics.

## Re-running the analysis

See `scripts/phase1_5_analysis.py` and
[`outputs/phase1_5/phase1_5_report.md`](../outputs/phase1_5/phase1_5_report.md).
Phases 6–7 use the cleaned training data to engineer prediction-time features
and train three regression candidates. Booking-window effects cannot be
modeled because the source has no booking-date field; see the generated
[`Phase 6 report`](../outputs/phase6/phase6_report.md) and
[`Phase 7 report`](../outputs/phase7/phase7_report.md).
Phase 8 cross-validates the candidates, evaluates a held-out partition, and
reports the final comparison in
[`outputs/phase8/phase8_report.md`](../outputs/phase8/phase8_report.md).
Phase 9 produces global and individual SHAP explanations for the selected
model in [`outputs/phase9/phase9_report.md`](../outputs/phase9/phase9_report.md).
The raw workbooks are included under the source's CC0 designation; retain this
source and license attribution when reusing them.
