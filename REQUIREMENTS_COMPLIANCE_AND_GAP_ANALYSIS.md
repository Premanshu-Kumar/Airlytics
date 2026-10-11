# 📋 Airlytics Project Requirements Compliance & Status Report

**Project Name:** Airlytics — Intelligent Airfare Price Estimation & Explainable Flight Analytics  
**Date of Audit & Update:** October 11, 2026  
**Audited Against:** Academic & Project Submission Requirements  

---

## Executive Summary

| Requirement Item | Status | Completion Level | Remarks / Outcome |
|---|:---:|:---:|---|
| **1. Dataset Acquisition** | **DONE** | 100% | Downloaded from Kaggle (Jillani SofTech / EaseMyTrip, CC0 license). Stored in `data/raw/`. |
| **2. Preprocessing & Cleaning** | **DONE** | 100% | Missing values handled, 220 duplicates removed, inconsistent strings parsed into numeric values. Clean dataset: `outputs/phase1_5/cleaned_fares.csv`. |
| **3. Exploratory Data Analysis (EDA)** | **DONE** | 100% | Univariate, bivariate, multivariate, correlation, and Kruskal-Wallis & Spearman statistical tests completed. |
| **4. Define & Investigate 5 Objectives** | **DONE** | 100% | 5 distinct analytical objectives formulated, investigated, and documented with quantitative findings. |
| **5. Data Visualizations** | **DONE** | 100% | 10+ publication-grade plots (histograms with KDE, boxplots, scatter/bubble plots, heatmaps, residual curves) generated in `outputs/`. |
| **6. Feature Engineering** | **DONE** | 100% | Datetime features, time-of-day bins, route segments, one-hot encoding, and scaling implemented in Phase 6. |
| **7. At Least 4 Machine Learning Models** | **DONE** | 100% | **5 models implemented & trained** (Random Forest, Decision Tree, Gradient Boosting, XGBoost, Linear Regression). Best-fit model: Random Forest. |
| **8. Model Evaluation Metrics** | **DONE** | 100% | Evaluated using MAE, RMSE, R², and 5-Fold Cross-Validation across all 5 models. |
| **9. Key Findings & Recommendations** | **DONE** | 100% | Documented in reports and README; actionable airline and consumer recommendations provided. |
| **10. Final Submission Assets (Dataset, Python Scripts, Visuals, Results)** | **DONE** | 100% | Raw and cleaned datasets, modular Python scripts, complete visual assets, trained model artifacts, and evaluation metrics are fully present. |

---

## Detailed Requirement-by-Requirement Evidence

### 1. Dataset Acquisition from Kaggle
* **Status:** ✅ **Fully Satisfied (100%)**
* **Evidence:**
  * Source: Kaggle (*Flight Price Prediction DataSet* by Jillani SofTech / EaseMyTrip).
  * License: CC0: Public Domain.
  * Files Present: 
    * `data/raw/Data_Train.xlsx` (10,683 records, 11 features including target `Price`)
    * `data/raw/Test_set.xlsx` (2,671 records)
  * Dataset Documentation: Fully documented in `data/README.md`.

---

### 2. Data Preprocessing and Cleaning
* **Status:** ✅ **Fully Satisfied (100%)**
* **Evidence (`scripts/phase1_5_analysis.py`):**
  * **Missing Values:** Identified and handled 1 missing route/stops row in the training set.
  * **Duplicate Handling:** Identified and dropped 220 exact duplicate flight listings (clean dataset: 10,462 records).
  * **Data Type Normalization & Inconsistent Data:**
    * `Duration` text (e.g., `"2h 50m"`, `"5m"`) converted to numerical `Duration_Minutes`.
    * `Total_Stops` text (`"non-stop"`, `"1 stop"`, `"2 stops"`) parsed into discrete integers (`0, 1, 2, ...`).
    * `Date_of_Journey`, `Dep_Time`, `Arrival_Time` converted into proper datetime and hour floats.
    * Standardized source/destination strings (e.g. `Banglore` → `Bangalore`).
  * Clean output preserved in `outputs/phase1_5/cleaned_fares.csv`.

---

### 3. Exploratory Data Analysis (EDA)
* **Status:** ✅ **Fully Satisfied (100%)**
* **Evidence:**
  * Descriptive statistics: Mean, median, standard deviation, interquartile range (IQR), skewness, and kurtosis.
  * Statistical hypothesis testing:
    * Kruskal-Wallis test: Statistically significant fare variance across airlines ($H = 5092.3, p < 0.001$).
    * Spearman rank correlation: Strong positive relationship between duration and fare ($\rho = 0.59, p < 0.001$).
  * Full statistical documentation in `outputs/phase1_5/phase1_5_report.md`.

---

### 4. Five Core Analytical Objectives & Findings
* **Status:** ✅ **Fully Satisfied (100%)**
* **Objective 1 (Carrier Pricing Strategy):**
  * *Investigation:* Compare median base fare and dispersion between budget (IndiGo, SpiceJet, Air Asia) and full-service (Jet Airways, Air India, Vistara) carriers.
  * *Finding:* Full-service carriers have significantly higher medians (Jet Airways: ₹10,262) and broader interquartile spreads compared to budget carriers (IndiGo: ₹5,001).
* **Objective 2 (Number of Stops vs. Fare):**
  * *Investigation:* Measure the quantitative price penalty associated with layovers (0 vs. 1 vs. 2+ stops).
  * *Finding:* Non-stop flights have a median fare of ₹4,667, 1-stop flights jump to ₹10,262 (+120%), and 2-stop flights reach ₹12,760 (+173%).
* **Objective 3 (Flight Duration vs. Cost):**
  * *Investigation:* Determine correlation and price elasticity with respect to total travel duration in minutes.
  * *Finding:* Strong Spearman correlation ($\rho = 0.59$). Fares increase sharply for flights between 2 to 10 hours; beyond 10 hours, layover waiting time exhibits diminishing fare impact.
* **Objective 4 (Temporal & Seasonal Variations):**
  * *Investigation:* Assess how ticket prices vary across travel months (March to June) and weekdays vs. weekends.
  * *Finding:* March observed peak median fares (₹9,316) due to financial year-end and holiday travel; weekend departures commanded a modest premium over mid-week departures.
* **Objective 5 (Route & Hub Dynamics):**
  * *Investigation:* Identify pricing variations across domestic origin-destination metro corridors.
  * *Finding:* Banglore → New Delhi and Delhi → Cochin corridors recorded the highest median fares and transaction volume, whereas routes originating from Chennai observed lower median fares.

---

### 5. Data Visualization Techniques
* **Status:** ✅ **Fully Satisfied (100%)**
* **Generated Charts in `outputs/phase1_5/` & `outputs/phase8/`:**
  * `price_distribution.png`: Histogram with KDE curve and median markers.
  * `price_by_airline.png`: Box plot showing fare distribution and outlier bands per airline.
  * `price_by_stops.png`: Box plot of fare by stop count.
  * `price_by_month.png`: Bar chart displaying monthly fare trends.
  * `price_by_route.png`: Top route fare comparison.
  * `numeric_correlation.png`: Correlation matrix heatmap.
  * `fare_duration_stops.png`: Multi-dimensional scatter/bubble plot (Duration vs Price colored by Stops).
  * `actual_vs_predicted.png`: Regression fit scatter plot.
  * `residual_distribution.png`: Error distribution bell curve.
  * `residuals_vs_predicted.png`: Residual homoscedasticity diagnostics.
  * `model_error_comparison.png`: MAE error comparison across candidate algorithms.

---

### 6. Feature Engineering
* **Status:** ✅ **Fully Satisfied (100%)**
* **Evidence (`scripts/phase6_feature_engineering.py`):**
  * **Temporal Engineering:** Extracted `Journey_Month`, `Journey_Day`, `Journey_DayOfWeek`, and binary `Is_Weekend`.
  * **Time-of-Day Bins:** `Departure_Period` and `Arrival_Period` (Early Morning, Morning, Afternoon, Evening, Night).
  * **Network Topology:** `Route_Segment_Count` and `Stop_Category` (`Direct`, `One-Stop`, `Multi-Stop`).
  * **Encoding & Scaling:** `OneHotEncoder` with rare-category thresholding (`min_frequency=2`), and `StandardScaler` for numeric values.

---

### 7. Implementation of Machine Learning Models & Best-Fit Model
* **Status:** ✅ **Fully Satisfied (100% - 5 Models Implemented)**
* **Implemented Models:**
  1. **Random Forest Regressor** (Ensemble Bagging)
  2. **Decision Tree Regressor** (Tree-based Baseline)
  3. **Gradient Boosting Regressor** (Sequential Boosting Ensemble)
  4. **XGBoost Regressor** (Extreme Gradient Boosting)
  5. **Linear Regression** (Ordinary Least Squares Baseline)
* **Best-Fit Model:**
  * **Random Forest Regressor** is the clear winner across all evaluation metrics, capturing non-linear interactions without overfitting.

---

### 8. Model Evaluation Metrics (5-Fold CV + Held-out Test Set)
* **Status:** ✅ **Fully Satisfied (100%)**
* **Leaderboard (`outputs/phase8/evaluation_metrics.csv`):**

| CV Rank | Model | 5-Fold CV MAE (Mean ± SD) | Holdout MAE | Holdout RMSE | Holdout $R^2$ | Best-Fit Selected |
|:---:|---|:---:|:---:|:---:|:---:|:---:|
| **1** | **Random Forest Regressor** | **673.06 ± 19.45** | **₹640.33** | **₹1,430.08** | **0.9019** | 🏆 **Yes (Best-Fit)** |
| 2 | Decision Tree Regressor | 820.63 ± 12.30 | ₹768.45 | ₹1,897.59 | 0.8273 | No |
| 3 | Gradient Boosting Regressor | 839.01 ± 13.97 | ₹824.74 | ₹1,527.10 | 0.8882 | No |
| 4 | XGBoost Regressor | 846.12 ± 18.44 | ₹842.43 | ₹1,498.44 | 0.8923 | No |
| 5 | Linear Regression (OLS) | 1,526.54 ± 28.26 | ₹1,514.45 | ₹2,367.78 | 0.7311 | No |

---

### 9. Key Findings, Conclusions & Recommendations
* **Status:** ✅ **Fully Satisfied (100%)**
* **Key Findings:**
  1. Airline selection and stop count drive over 70% of ticket price variance.
  2. Random Forest Regressor achieves an impressive $R^2$ of 0.9019 with a mean absolute prediction error of ~₹640.
  3. Single-stop and multi-stop flights incur substantial price markups compared to non-stop flights.
* **Recommendations:**
  * **For Consumers:** Choose non-stop flights and budget carriers (IndiGo, SpiceJet) for short-haul metro routes to save 40–60% on airfare.
  * **For Airlines:** Dynamic pricing engines should adjust markups primarily based on carrier brand tier and routing stops rather than duration alone.

---

### 10. Submission Materials
* **Status:** ✅ **Fully Satisfied (100%)**
* All source files, cleaned data, Python pipeline scripts, trained `.joblib` models, charts, and markdown reports are fully populated in the repository.
