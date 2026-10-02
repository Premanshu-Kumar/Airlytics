# ✈️ Airlytics

### Intelligent Airfare Price Estimation & Explainable Flight Analytics

> **Airlytics** is an end-to-end Machine Learning project that estimates
> airfare from route, airline, travel date, duration, stops,
> booking-window and related travel features, while explaining the major
> factors behind each prediction.

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://www.python.org/)
[![Scikit-learn](https://img.shields.io/badge/ML-Scikit--learn-orange)](https://scikit-learn.org/)
[![XGBoost](https://img.shields.io/badge/Model-XGBoost-red)](https://xgboost.readthedocs.io/)
[![SHAP](https://img.shields.io/badge/Explainability-SHAP-purple)](https://shap.readthedocs.io/)
[![Streamlit](https://img.shields.io/badge/App-Streamlit-ff4b4b?logo=streamlit)](https://streamlit.io/)

------------------------------------------------------------------------

## 🌐 What is Airlytics?

Airlytics combines **airfare analytics, predictive modeling and
explainable AI** into one system.

The system learns patterns from historical flight/fare data and
estimates the expected fare for a selected flight configuration.

It also answers an important question:

> **"Why did the model estimate this fare?"**

Airlytics therefore goes beyond a basic flight-price prediction notebook
and implements a complete Predictive Analytics workflow:

``` text
Real-World Problem
       ↓
Data Collection
       ↓
Data Cleaning
       ↓
EDA & Visualization
       ↓
Statistical Analysis
       ↓
Feature Engineering
       ↓
Machine Learning
       ↓
Model Comparison
       ↓
Evaluation
       ↓
Explainable AI
       ↓
Interactive Fare Estimator
```

------------------------------------------------------------------------

# 🎓 Academic Task Alignment

**University:** Lovely Professional University\
**Course:** Predictive Analytics\
**Course Code:** INT234\
**Academic Task:** 2\
**Task Type:** Skill-based Assignment\
**Maximum Marks:** 100\
**Submission Date:** 31 October 2026

### Requirements Covered

  -----------------------------------------------------------------------
  Assignment Requirement              Airlytics
  ----------------------------------- -----------------------------------
  Machine Learning / Deep Learning    ✅ Supervised ML Regression

  Real-world social/consumer problem  ✅ Consumer airfare estimation

  Data Collection                     ✅ Historical flight/fare data

  Data Visualization                  ✅ Matplotlib, Seaborn, Plotly

  EDA                                 ✅ Univariate, bivariate &
                                      multivariate analysis

  Statistical Analysis                ✅ Descriptive & correlation
                                      analysis

  Data Cleaning                       ✅ Missing values, duplicates,
                                      invalid values & outliers

  Data Transformation                 ✅ Encoding & feature processing

  Model Development                   ✅ Multiple regression models

  Model Evaluation                    ✅ MAE, RMSE & R²

  Feature Importance                  ✅ Model-based importance

  Explainable AI                      ✅ SHAP

  Interactive Demonstration           ✅ Airfare estimator

  GitHub                              ✅ Complete repository

  LinkedIn                            ✅ Project showcase
  -----------------------------------------------------------------------

------------------------------------------------------------------------

# 🎯 Problem Statement

Airfare prices can vary significantly depending on factors such as:

-   Airline
-   Origin and destination
-   Travel date
-   Booking window
-   Flight duration
-   Number of stops
-   Departure time
-   Seasonality
-   Day of week

Because these variables interact in complex ways, consumers may find it
difficult to estimate the expected cost of a flight before booking.

### Airlytics aims to solve this problem by:

> **Using historical flight-price data and Machine Learning to estimate
> airfare for a given flight configuration and explain the factors
> contributing to the prediction.**

The system is designed as a **consumer price-estimation and
decision-support tool**, not as a guarantee of the future market price.

------------------------------------------------------------------------

# 🌍 Real-World Relevance

Air travel plays an important role in:

-   Education
-   Employment
-   Tourism
-   Business
-   Family travel
-   Emergency travel

Airfare can also represent a significant expense for travelers.

Airlytics provides a data-driven way to understand historical airfare
patterns and estimate an expected price based on available flight and
booking features.

------------------------------------------------------------------------

# 🎯 Project Objectives

1.  Collect and validate a real-world airfare dataset.
2.  Understand the structure and characteristics of flight-price data.
3.  Perform data cleaning and preprocessing.
4.  Conduct exploratory data analysis.
5.  Perform statistical analysis.
6.  Engineer meaningful travel and booking-related features.
7.  Develop multiple Machine Learning regression models.
8.  Compare models using MAE, RMSE and R².
9.  Identify important airfare-related features.
10. Explain individual predictions using SHAP.
11. Build an interactive airfare estimator.
12. Document the complete Predictive Analytics lifecycle.

------------------------------------------------------------------------

# 🧠 Machine Learning Problem

### Learning Type

**Supervised Machine Learning**

### Problem Type

**Regression**

### Target

``` text
Airfare / Ticket Price
```

### Potential Input Features

``` text
Airline
Source
Destination
Route
Travel Date
Departure Time
Arrival Time
Duration
Number of Stops
Booking Window
Day of Week
Month
Season
Weekend Indicator
```

The final feature set will depend on the selected dataset and the
information realistically available when making a prediction.

------------------------------------------------------------------------

# 🔄 Airlytics Architecture

``` text
                    ┌──────────────────────┐
                    │   HISTORICAL DATA    │
                    │   Flight/Fare Data   │
                    └──────────┬───────────┘
                               ↓
                    ┌──────────────────────┐
                    │  DATA COLLECTION &   │
                    │      VALIDATION      │
                    └──────────┬───────────┘
                               ↓
                    ┌──────────────────────┐
                    │    DATA CLEANING     │
                    │ Missing / Duplicate  │
                    │ Invalid / Outliers   │
                    └──────────┬───────────┘
                               ↓
                    ┌──────────────────────┐
                    │         EDA          │
                    │ Visualization &      │
                    │ Pattern Discovery    │
                    └──────────┬───────────┘
                               ↓
                    ┌──────────────────────┐
                    │ STATISTICAL ANALYSIS │
                    │ Correlation & Stats  │
                    └──────────┬───────────┘
                               ↓
                    ┌──────────────────────┐
                    │ FEATURE ENGINEERING  │
                    │ Date / Time / Route  │
                    │ Booking Window       │
                    └──────────┬───────────┘
                               ↓
                    ┌──────────────────────┐
                    │   PREPROCESSING      │
                    │ Encoding / Scaling   │
                    └──────────┬───────────┘
                               ↓
                    ┌──────────────────────┐
                    │   TRAIN / TEST       │
                    │      STRATEGY        │
                    └──────────┬───────────┘
                               ↓
          ┌────────────────────┼────────────────────┐
          ↓                    ↓                    ↓
  Linear Regression     Random Forest           XGBoost
          ↓                    ↓                    ↓
          └────────────────────┼────────────────────┘
                               ↓
                    ┌──────────────────────┐
                    │   MODEL EVALUATION   │
                    │   MAE / RMSE / R²    │
                    └──────────┬───────────┘
                               ↓
                    ┌──────────────────────┐
                    │  MODEL COMPARISON    │
                    └──────────┬───────────┘
                               ↓
                 ┌─────────────┴─────────────┐
                 ↓                           ↓
        Feature Importance                 SHAP
                 └─────────────┬─────────────┘
                               ↓
                    ┌──────────────────────┐
                    │   AIRLYTICS ENGINE   │
                    └──────────┬───────────┘
                               ↓
                    ┌──────────────────────┐
                    │ INTERACTIVE WEB APP  │
                    └──────────────────────┘
```

------------------------------------------------------------------------

# 📊 Dataset

## Dataset Requirements

The dataset should contain historical flight/fare observations that
support airfare regression.

Potential fields:

  Feature          Description                       Type
  ---------------- --------------------------------- -----------------------
  Airline          Operating airline                 Categorical
  Source           Departure location                Categorical
  Destination      Arrival location                  Categorical
  Route            Origin-destination combination    Categorical
  Travel Date      Intended travel date              Date
  Departure Time   Departure time                    Time
  Arrival Time     Arrival time                      Time
  Duration         Flight duration                   Numerical
  Stops            Number of stops                   Numerical/Categorical
  Price            Historical airfare                Target
  Booking Date     Date of booking, if available     Date
  Booking Window   Days between booking and travel   Numerical

### Booking Window

If both booking date and travel date are available:

``` text
Booking Window = Travel Date - Booking Date
```

This allows Airlytics to investigate how advance booking relates to
observed airfare.

------------------------------------------------------------------------

# 🔎 Dataset Source

The implemented analysis documents:

-   Dataset name, publisher and source URL
-   Dataset version and download date
-   Number of rows and columns
-   Feature descriptions and target variable
-   Dataset license as listed by the publisher
-   Data collection limitations

The exact source used in the analysis is recorded in:

``` text
data/README.md
```

Only datasets permitted for the intended academic/research use will be
used.

## Implemented Phases 1–10

Phases 1–5 are completed against the labeled EaseMyTrip-derived dataset. The
dataset source, CC0 license as listed by its publisher, schema, and limitations
are documented in [`data/README.md`](data/README.md). The reproducible cleaning,
EDA, statistical tests, generated charts, and findings are in
[`outputs/phase1_5/phase1_5_report.md`](outputs/phase1_5/phase1_5_report.md);
rerun them with `python scripts/phase1_5_analysis.py`.

The source does not provide booking dates or explicitly identify the currency.
The analysis therefore excludes booking-window conclusions and reports fares
in source units rather than asserting a currency.

Phases 6–7 are also implemented. Install the modeling dependencies and run
feature engineering followed by model development:

```powershell
python -m pip install -r requirements-modeling.txt
python scripts/phase6_feature_engineering.py
python scripts/phase7_model_development.py
python scripts/phase8_model_evaluation.py
python scripts/phase9_explainability.py
```

Phase 6 writes `outputs/phase6/engineered_fares.csv` and its feature report.
Phase 7 trains Linear Regression, Random Forest, and XGBoost pipelines and
writes the fitted artifacts and development-validation results to
`outputs/phase7/`. Booking-window features are excluded because no booking date
is present in the source. The fare target and target-derived outlier flag are
not used as model inputs; scaling and categorical encoding are fitted within
each training pipeline.

Phase 8 ranks candidates using five-fold cross-validation on the training
partition, reports MAE, RMSE, and R² on a separate held-out partition, and
refits the selected candidate on all labeled observations for later phases.
Evaluation metrics, predictions, diagnostics, report, and selected model are
written to `outputs/phase8/`.

Phase 9 uses Tree SHAP on the selected Random Forest to aggregate one-hot
encoded contributions back to the original feature names. It writes global
SHAP and impurity-based importance, a global summary, and an individual
prediction waterfall with additive contributions to `outputs/phase9/`. The
default local example is source row 0; use `--row-index` to select another
engineered row. Because the selected model is refit on all labeled rows, this
local explanation is illustrative rather than an independent test example.

Phase 10 provides a Streamlit airfare estimator using the selected Phase 8
model, with routes and additional-information categories taken from the
training data, input consistency checks, and per-estimate SHAP explanations.
Install the app dependencies and launch it with:

```powershell
python -m pip install -r requirements-app.txt
streamlit run app/app.py
```

The fare output uses source units, and estimates are limited to patterns
learned from historical 2019 observations.

------------------------------------------------------------------------

# 🧹 Data Cleaning

Airlytics will investigate and document:

## Missing Values

-   Detection
-   Missingness analysis
-   Appropriate imputation
-   Justified row/column removal

## Duplicate Records

-   Detection
-   Validation
-   Removal of inappropriate duplicates

## Invalid Values

Examples:

-   Negative prices
-   Invalid durations
-   Invalid dates
-   Invalid stop counts
-   Inconsistent airline names
-   Inconsistent location names

## Outliers

Methods may include:

-   IQR
-   Box plots
-   Distribution analysis
-   Domain-based validation

Outliers will not automatically be removed.

------------------------------------------------------------------------

# 🔧 Data Transformation

## Categorical Features

Potential categorical variables:

``` text
Airline
Source
Destination
Route
Stop Category
```

Possible methods:

-   One-Hot Encoding
-   Appropriate categorical encoding
-   Native categorical handling where supported

## Numerical Features

Potential operations:

-   Scaling
-   Numerical conversion
-   Log transformation for strongly skewed variables
-   Robust handling of extreme values

Preprocessing will be designed to minimize data leakage.

------------------------------------------------------------------------

# 🧠 Feature Engineering

Airlytics converts raw flight information into predictive features.

## Date Features

``` text
Year
Month
Day
Day of Week
Weekend
Season
```

## Time Features

``` text
Departure Hour
Arrival Hour
Departure Period
Arrival Period
```

## Flight Features

``` text
Duration in Minutes
Number of Stops
Stop Category
Route
```

## Booking Features

``` text
Booking Window
Early Booking Indicator
Last-Minute Booking Indicator
```

Only features that are realistically available at prediction time should
be included in the production estimator.

------------------------------------------------------------------------

# 📈 Exploratory Data Analysis

Airlytics will perform:

## Univariate Analysis

-   Fare distribution
-   Duration distribution
-   Airline frequency
-   Route frequency
-   Stops distribution
-   Booking-window distribution

## Bivariate Analysis

``` text
Airline        → Price
Route          → Price
Stops          → Price
Duration       → Price
Booking Window → Price
Month          → Price
Day of Week    → Price
```

## Multivariate Analysis

Potential visualizations:

-   Correlation heatmap
-   Airline-route fare analysis
-   Booking-window vs fare
-   Seasonal fare trends
-   Route-level fare variation
-   Fare distribution by number of stops

------------------------------------------------------------------------

# 📐 Statistical Analysis

## Descriptive Statistics

``` text
Mean
Median
Minimum
Maximum
Variance
Standard Deviation
Quartiles
```

## Correlation Analysis

Potential methods:

-   Pearson correlation
-   Spearman correlation

The selected method will depend on variable type and distribution.

### Questions investigated

-   How does airfare vary with booking window?
-   Which routes have the greatest price variation?
-   How does duration relate to airfare?
-   How do fare distributions differ between airlines?
-   Are there seasonal fare patterns?

------------------------------------------------------------------------

# 🤖 Machine Learning Models

Airlytics trains and compares multiple regression algorithms.

## 1. Linear Regression

A simple and interpretable baseline.

## 2. Random Forest Regressor

Useful for non-linear relationships and feature interactions.

## 3. XGBoost Regressor

A gradient-boosting model designed for structured/tabular data.

## 4. CatBoost Regressor --- Optional

Useful for datasets containing many categorical variables.

Initial candidate models are trained on the Phase 6 features. Final model
selection is deferred until the broader Phase 8 evaluation.

------------------------------------------------------------------------

# 🧪 Training Strategy

The Phase 7 development run uses a reproducible random split:

``` text
Training → 80%
Testing  → 20%
```

Phase 8 uses five-fold shuffled cross-validation on the training partition
for candidate selection and reserves the held-out partition for final metrics.

If the dataset has meaningful temporal ordering, a time-aware validation
strategy may be considered instead of randomly mixing future
observations into training data.

------------------------------------------------------------------------

# 📊 Model Evaluation

Because Airlytics solves a regression problem, the primary metrics are:

## MAE --- Mean Absolute Error

Measures the average absolute prediction error.

## RMSE --- Root Mean Squared Error

Penalizes larger prediction errors more strongly.

## R² --- Coefficient of Determination

Measures the proportion of target variation explained by the model.

------------------------------------------------------------------------

# 🏆 Model Comparison

The following are Phase 7 development-validation results from the fixed 80/20
split (random state 42), in fare source units. They are preliminary; Phase 8
cross-validation and holdout metrics are reported separately.

| Model | MAE | RMSE | R² |
|---|---:|---:|---:|
| Linear Regression | 1,514.45 | 2,367.78 | 0.7311 |
| Random Forest | 640.33 | 1,430.08 | 0.9019 |
| XGBoost | 842.43 | 1,498.44 | 0.8923 |

The Random Forest has the lowest MAE on this split; this is not a final model
selection decision. CatBoost remains optional and was not trained.

------------------------------------------------------------------------

# 🔍 Feature Importance

Phase 9 calculates mean absolute grouped SHAP contributions and aggregates
Random Forest impurity importance across one-hot encoded categories.

The global comparison and SHAP summary use the original input features:

``` text
Route
Airline
Booking Window
Travel Month
Duration
Stops
Departure Time
```

See [`outputs/phase9/phase9_report.md`](outputs/phase9/phase9_report.md) for
measured results and interpretation limits.

------------------------------------------------------------------------

# 🧠 Explainable AI with SHAP

Airlytics can use **SHAP (SHapley Additive exPlanations)** to explain
individual predictions.

Example:

``` text
Predicted Fare
     ₹7,850

Contributing Factors

Booking Window     ██████████
Route              █████████
Airline            ███████
Travel Season      █████
Duration           ███
Stops              ██
```

The values above are UI examples only.

Global and individual SHAP values are generated from the selected Phase 8
model. The local waterfall and full per-feature contributions are documented
in [`outputs/phase9/phase9_report.md`](outputs/phase9/phase9_report.md).

### Explainability Goal

Instead of only showing:

> **Estimated Fare: ₹7,850**

Airlytics can also show:

> **Which features contributed most strongly to this estimate?**

------------------------------------------------------------------------

# 🖥️ Interactive Airfare Estimator

The final application will allow a user to enter flight information.

## User Inputs

``` text
Airline
Source
Destination
Travel Date
Departure Time
Arrival Time
Duration
Number of Stops
Booking Window
```

## Output

``` text
Estimated Fare
```

## Additional Output

``` text
Major Influencing Features
Feature Importance
Prediction Explanation
```

The application can be implemented using **Streamlit**.

------------------------------------------------------------------------

# 🎨 Prototype UI

``` text
┌────────────────────────────────────────────────────┐
│                    ✈️ AIRLYTICS                   │
│        Intelligent Airfare Price Estimation       │
├────────────────────────────────────────────────────┤
│                                                    │
│ Airline          [ Select Airline ▼ ]             │
│                                                    │
│ From             [ Delhi ▼ ]                       │
│ To               [ Mumbai ▼ ]                      │
│                                                    │
│ Travel Date      [ DD / MM / YYYY ]                │
│                                                    │
│ Departure Time   [ 10:30 AM ]                      │
│ Arrival Time     [ 12:45 PM ]                      │
│                                                    │
│ Duration         [ 2h 15m ]                        │
│ Stops            [ Non-stop ▼ ]                    │
│ Booking Window   [ 30 days ]                       │
│                                                    │
│             [ ✈ ESTIMATE FARE ]                   │
│                                                    │
├────────────────────────────────────────────────────┤
│                 ESTIMATED FARE                    │
│                                                    │
│                     ₹7,850                        │
│                                                    │
├────────────────────────────────────────────────────┤
│              PRICE EXPLANATION                    │
│                                                    │
│ Booking Window       ██████████                    │
│ Route                █████████                     │
│ Airline              ███████                       │
│ Travel Season        █████                         │
│ Duration             ███                           │
│                                                    │
└────────────────────────────────────────────────────┘
```

The ₹7,850 value is a UI example, not an actual model result.

------------------------------------------------------------------------

# 🏗️ Technical Architecture

``` text
                         USER
                          │
                          ▼
                 ┌────────────────┐
                 │ Streamlit App  │
                 └───────┬────────┘
                         │
                         ▼
                 ┌────────────────┐
                 │ Input Validation│
                 └───────┬────────┘
                         │
                         ▼
                 ┌────────────────┐
                 │ Feature         │
                 │ Engineering     │
                 └───────┬────────┘
                         │
                         ▼
                 ┌────────────────┐
                 │ Preprocessing   │
                 │ Pipeline        │
                 └───────┬────────┘
                         │
                         ▼
                 ┌────────────────┐
                 │ Trained ML     │
                 │ Model           │
                 └───────┬────────┘
                         │
                  ┌──────┴───────┐
                  ▼              ▼
          ┌─────────────┐ ┌──────────────┐
          │ Fare        │ │ SHAP /       │
          │ Prediction  │ │ Explanation  │
          └──────┬──────┘ └──────┬───────┘
                 │               │
                 └───────┬───────┘
                         ▼
                 ┌────────────────┐
                 │ Final Result   │
                 │ + Explanation  │
                 └────────────────┘
```

------------------------------------------------------------------------

# 🧰 Technology Stack

### Programming

-   Python

### Data Analysis

-   Pandas
-   NumPy

### Visualization

-   Matplotlib
-   Seaborn
-   Plotly

### Machine Learning

-   Scikit-learn
-   XGBoost
-   CatBoost (optional)

### Explainable AI

-   SHAP

### Application

-   Streamlit

### Development

-   VS Code
-   Jupyter Notebook

### Version Control

-   Git
-   GitHub

------------------------------------------------------------------------

# 📁 Repository Structure

``` text
Airlytics/
│
├── README.md
├── requirements.txt
├── .gitignore
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── README.md
│
├── notebooks/
│   ├── 01_data_collection.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_eda.ipynb
│   ├── 04_statistical_analysis.ipynb
│   ├── 05_feature_engineering.ipynb
│   ├── 06_model_training.ipynb
│   └── 07_model_evaluation.ipynb
│
├── src/
│   ├── data_processing.py
│   ├── feature_engineering.py
│   ├── train.py
│   ├── evaluate.py
│   └── predict.py
│
├── models/
│   ├── preprocessing_pipeline.pkl
│   └── best_model.pkl
│
├── app/
│   └── app.py
│
├── reports/
│   ├── figures/
│   ├── model_results/
│   └── final_report.pdf
│
├── screenshots/
│   ├── eda/
│   ├── model/
│   └── application/
│
└── LICENSE
```

------------------------------------------------------------------------

# 🔬 Development Roadmap

## Phase 1 --- Problem Definition

-   Define problem
-   Define objectives
-   Define target
-   Define project scope

## Phase 2 --- Dataset Selection & Collection

-   Find suitable dataset
-   Verify source
-   Verify license
-   Download data
-   Document schema

## Phase 3 --- Data Cleaning

-   Missing values
-   Duplicates
-   Invalid records
-   Outlier analysis
-   Data types

## Phase 4 --- EDA

-   Univariate analysis
-   Bivariate analysis
-   Multivariate analysis
-   Price trends
-   Airline analysis
-   Route analysis
-   Booking-window analysis

## Phase 5 --- Statistical Analysis

-   Descriptive statistics
-   Correlation
-   Distribution analysis
-   Statistical observations

## Phase 6 --- Feature Engineering

-   Date features
-   Time features
-   Duration
-   Stops
-   Route
-   Season
-   Booking window

## Phase 7 --- Model Development

-   Linear Regression
-   Random Forest
-   XGBoost
-   Optional CatBoost

## Phase 8 --- Model Evaluation

-   Cross-validation
-   MAE
-   RMSE
-   R²
-   Holdout comparison

## Phase 9 --- Explainable AI

-   Feature importance
-   SHAP global explanation
-   SHAP individual prediction explanation

## Phase 10 --- Application

-   Streamlit interface with training-data route/category options
-   Flight route and stop-count validation
-   Prediction through the fitted Phase 8 pipeline
-   Prediction and user-input display
-   Individual SHAP explanations and global feature reference

## Phase 11 --- Testing

-   Valid inputs
-   Missing inputs
-   Unknown categories
-   Boundary values
-   Different routes
-   Different booking windows

## Phase 12 --- Documentation & Submission

-   Final README
-   Final report
-   Screenshots
-   GitHub repository
-   LinkedIn post
-   Viva preparation

------------------------------------------------------------------------

# 🎤 Viva / Project Demonstration

The final demonstration is designed around every demonstration point
specified in the academic task.

## 1. Problem Selected & Real-World Relevance

Explain:

> Airfare varies according to multiple factors, making expected pricing
> difficult to estimate. Airlytics uses historical flight data and
> Machine Learning to provide a data-driven airfare estimate.

## 2. Project Objectives

Explain:

``` text
Data Collection
      ↓
Data Cleaning
      ↓
EDA
      ↓
Statistical Analysis
      ↓
Feature Engineering
      ↓
ML Regression
      ↓
Model Evaluation
      ↓
Explainability
      ↓
Interactive Estimator
```

## 3. Dataset Source & Structure

Explain:

-   Dataset source
-   Number of rows
-   Number of columns
-   Feature types
-   Target variable
-   Dataset limitations

## 4. Data Cleaning & Transformation

Demonstrate:

``` text
Raw Data
   ↓
Missing Values
   ↓
Duplicates
   ↓
Invalid Data
   ↓
Outliers
   ↓
Encoding
   ↓
Feature Engineering
   ↓
ML Dataset
```

## 5. Methodologies Used & Outcomes

Explain:

-   EDA
-   Statistical analysis
-   Feature engineering
-   Preprocessing
-   Regression models
-   Model comparison
-   Evaluation metrics
-   Feature importance
-   SHAP explainability
-   Interactive prediction

------------------------------------------------------------------------

# 📊 Expected Outputs

### Data Analysis

-   Clean dataset
-   Feature dictionary
-   EDA charts
-   Statistical analysis

### Machine Learning

-   Trained models
-   Model comparison
-   MAE
-   RMSE
-   R²

### Explainability

-   Feature importance
-   SHAP plots
-   Individual prediction explanations

### Application

-   Interactive airfare estimator

### Academic Deliverables

-   Final report
-   GitHub repository
-   LinkedIn project showcase
-   Viva demonstration

------------------------------------------------------------------------

# 📝 Final Report Structure

1.  Introduction
2.  Problem Statement
3.  Real-World Relevance
4.  Objectives
5.  Dataset Source and Structure
6.  Data Cleaning
7.  Data Transformation
8.  Exploratory Data Analysis
9.  Statistical Analysis
10. Feature Engineering
11. Machine Learning Methodology
12. Model Development
13. Model Evaluation
14. Model Comparison
15. Feature Importance
16. Explainable AI
17. Interactive Application
18. Results and Discussion
19. Limitations
20. Conclusion
21. Future Scope
22. References

------------------------------------------------------------------------

# 🏆 Assignment Rubric Mapping

## 10 Marks --- Problem Statement, Objectives & Dataset

Airlytics covers:

-   ✅ Problem Statement
-   ✅ Real-world relevance
-   ✅ Objectives
-   ✅ Dataset source
-   ✅ Dataset structure
-   ✅ Target variable
-   ✅ Feature descriptions

## 60 Marks --- Implementation & Report

Airlytics covers:

-   ✅ Data Collection
-   ✅ Data Cleaning
-   ✅ Data Transformation
-   ✅ EDA
-   ✅ Statistical Analysis
-   ✅ Data Visualization
-   ✅ Feature Engineering
-   ✅ Model Development
-   ✅ Model Comparison
-   ✅ MAE
-   ✅ RMSE
-   ✅ R²
-   ✅ Feature Importance
-   ✅ Explainable AI
-   ✅ Application Demonstration
-   ✅ Results & Discussion

## 10 Marks --- LinkedIn

The project showcase can contain:

-   Project overview
-   Problem statement
-   Technology stack
-   EDA visualizations
-   Model results
-   Application screenshots
-   GitHub repository
-   Key learning outcomes

## 20 Marks --- GitHub

The repository will contain:

-   README
-   Source code
-   Notebooks
-   Dataset documentation
-   Requirements
-   Model files
-   Application
-   Results
-   Screenshots
-   Final report

------------------------------------------------------------------------

# ⚠️ Limitations

Airlytics may be limited by:

-   Dataset size and quality
-   Route coverage
-   Airline coverage
-   Historical data availability
-   Missing inventory information
-   Promotional pricing
-   Sudden market changes
-   External economic or operational events

Therefore:

> **Airlytics provides a data-driven estimate based on historical
> patterns and available features; it does not guarantee the actual
> future ticket price.**

------------------------------------------------------------------------

# 🚀 Future Scope

Potential future improvements:

-   Real-time airfare data integration
-   Larger multi-airline datasets
-   Time-series airfare modeling
-   Dynamic fare trend analysis
-   Personalized fare alerts
-   Advanced uncertainty estimation
-   Deep Learning models
-   More geographical regions
-   Cloud deployment
-   Mobile-friendly interface

------------------------------------------------------------------------

# 📌 Success Checklist

-   [x] Problem statement completed
-   [x] Real-world relevance documented
-   [x] Objectives defined
-   [x] Dataset source documented
-   [x] Dataset structure documented
-   [x] Data cleaning completed
-   [x] Data transformation completed
-   [x] EDA completed
-   [x] Statistical analysis completed
-   [x] Feature engineering completed
-   [x] Multiple ML models trained
-   [x] MAE calculated
-   [x] RMSE calculated
-   [x] R² calculated
-   [x] Cross-validation completed
-   [x] Model evaluation and comparison completed
-   [x] Feature importance completed
-   [x] Global SHAP explanation completed
-   [x] Individual SHAP explanation completed
-   [x] Interactive estimator completed
-   [ ] Testing completed
-   [ ] Final report completed
-   [ ] GitHub repository completed
-   [ ] LinkedIn submission completed
-   [ ] Viva demonstration completed

------------------------------------------------------------------------

# 🎓 Project Summary

Airlytics demonstrates a complete Predictive Analytics workflow:

``` text
REAL-WORLD PROBLEM
        ↓
DATA COLLECTION
        ↓
DATA CLEANING
        ↓
EDA & VISUALIZATION
        ↓
STATISTICAL ANALYSIS
        ↓
FEATURE ENGINEERING
        ↓
MACHINE LEARNING
        ↓
MODEL COMPARISON
        ↓
EVALUATION
        ↓
EXPLAINABLE AI
        ↓
INTERACTIVE APPLICATION
        ↓
DATA-DRIVEN AIRFARE ESTIMATION
```

### Core Statement

> **Airlytics transforms historical airfare data into an explainable
> Machine Learning system that estimates expected flight prices and
> identifies the factors associated with those estimates.**

------------------------------------------------------------------------

# 👨‍💻 Author

**Premanshu Kumar**

B.Tech Computer Science Engineering --- Data Science

### Areas

-   Data Science
-   Machine Learning
-   Predictive Analytics
-   Python
-   Data Visualization
-   Explainable AI

------------------------------------------------------------------------

# ⭐ Project Status

**Status:** 🚧 In Development — Phases 1–5 complete

Phases 6–12 (feature engineering, modeling, evaluation, explainability,
application, testing, and final submission) remain in progress.

------------------------------------------------------------------------

# 📄 License

This project is licensed under the **Apache License 2.0**.

See `LICENSE` for details.

---
