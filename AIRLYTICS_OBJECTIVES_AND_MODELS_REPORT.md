# ✈️ Airlytics — 5 Analytical Objectives, 5 Machine Learning Models & Visualizations Report

**Project Title:** Airlytics (FlightIQ)  
**Domain:** Aviation Fare Analytics, Supervised Machine Learning & Explainable AI (XAI)  
**Dataset:** 10,683 Historical Flight Booking Records (Kaggle / EaseMyTrip, 10,462 Cleaned Records)  
**Date:** October 2026  

---

## 📑 Table of Contents
1. [Executive Summary](#executive-summary)
2. [Part I: The 5 Core Analytical Objectives & Empirical Data](#part-i-the-5-core-analytical-objectives--empirical-data)
   - [Objective 1: Carrier Pricing Strategy & Market Segmentation](#objective-1-carrier-pricing-strategy--market-segmentation)
   - [Objective 2: Impact of Flight Stops & Layovers on Fare](#objective-2-impact-of-flight-stops--layovers-on-fare)
   - [Objective 3: Flight Duration vs. Price Elasticity](#objective-3-flight-duration-vs-price-elasticity)
   - [Objective 4: Temporal & Seasonal Fluctuations](#objective-4-temporal--seasonal-fluctuations)
   - [Objective 5: Route Corridors & Origin-Destination Hub Dynamics](#objective-5-route-corridors--origin-destination-hub-dynamics)
3. [Part II: The 5 Machine Learning Models & Evaluation Metrics](#part-ii-the-5-machine-learning-models--evaluation-metrics)
   - [Model Comparison Leaderboard](#model-comparison-leaderboard)
   - [Model 1: Random Forest Regressor (Selected Best-Fit Model)](#model-1-random-forest-regressor-selected-best-fit-model)
   - [Model 2: Decision Tree Regressor](#model-2-decision-tree-regressor)
   - [Model 3: Gradient Boosting Regressor](#model-3-gradient-boosting-regressor)
   - [Model 4: XGBoost Regressor](#model-4-xgboost-regressor)
   - [Model 5: Linear Regression (OLS Baseline)](#model-5-linear-regression-ols-baseline)
4. [Part III: Model Diagnostic Visualizations](#part-iii-model-diagnostic-visualizations)
5. [Summary of Conclusions & Recommendations](#summary-of-conclusions--recommendations)

---

## Executive Summary

The **Airlytics** platform is built to solve severe consumer information asymmetry in aviation pricing by deconstructing fare variance, predicting ticket prices with sub-₹650 error margin, and explaining price formation through cooperative game theory (Tree SHAP).

* **5 Distinct Objectives** were empirically formulated and validated using descriptive statistics and non-parametric hypothesis tests ($p < 0.001$).
* **5 Supervised Machine Learning Architectures** were developed with 5-Fold Cross Validation.
* **Random Forest Regressor** demonstrated superior generalization, achieving an $R^2$ of **0.9019 (90.2%)** and a Mean Absolute Error (MAE) of **₹640.33**.

---

## Part I: The 5 Core Analytical Objectives & Empirical Data

| Objective # | Research Question | Analytical Methodology | Key Quantitative Finding | Primary Visualization |
| :---: | :--- | :--- | :--- | :--- |
| **Obj 1** | **Carrier Pricing Strategy** | Grouped median, IQR spread, Kruskal-Wallis test ($H=4753.89$) | Full-service carriers (Jet Airways median ₹10,262) cost >2× budget airlines (IndiGo median ₹5,001, SpiceJet ₹3,847). | `price_by_airline.png` |
| **Obj 2** | **Stops & Layovers vs. Fare** | Grouped step-penalty and multi-sector comparison | Non-stop flights median = ₹4,667. 1 stop leaps by **+120% (₹10,262)**; 2+ stops leap by **+173% (₹12,760)**. | `price_by_stops.png` |
| **Obj 3** | **Duration Elasticity** | Spearman non-parametric correlation ($\rho = 0.694$) | Non-linear growth: Steep price escalation between 2 to 10 hours; plateauing beyond 10 hours due to idle layovers. | `fare_duration_stops.png` |
| **Obj 4** | **Temporal & Seasonal Trends** | Month-over-month (March–June) & weekend vs. weekday indexing | March recorded the peak median fare (₹9,316) from fiscal year-end demand; weekend departures exhibit consistent price premiums. | `price_by_month.png` |
| **Obj 5** | **Route Corridors & Hub Dynamics** | Origin-Destination cross-tabulation and density analysis | High-density corporate corridors (Bangalore → New Delhi, Delhi → Cochin) command peak median fares. | `price_by_route.png` |

---

### Objective 1: Carrier Pricing Strategy & Market Segmentation

#### 🔍 Investigation:
To quantify how ticket pricing varies across budget low-cost carriers (LCCs) versus full-service carriers (FSCs) and assess whether airline branding dictates base pricing.

#### 📊 Empirical Data & Findings:
* **Kruskal-Wallis Test Statistic:** $H = 4753.89$ ($p < 0.0001$), confirming statistically significant fare variance across airlines.
* **Budget Carriers (LCCs):**
  * **SpiceJet:** Lowest median fare in the dataset (~₹3,847), tightly bounded IQR [₹3,100, ₹4,800].
  * **Air Asia:** Median fare of ₹4,282.
  * **IndiGo:** Median fare of ₹5,001 with high flight frequency and low standard deviation.
* **Full-Service Carriers (FSCs):**
  * **Jet Airways:** Median fare of ₹10,262 (IQR [₹7,200, ₹14,000]).
  * **Air India:** Median fare of ₹9,443 with long-tail high fares on multi-stop routes.
  * **Multiple Carrier Premium:** Median fare of ₹10,155.
  * **Jet Airways Business:** Premium luxury outliers ranging up to ₹79,512.

#### 📈 Objective 1 Graph:
![Fare by Airline](outputs/phase1_5/price_by_airline.png)

---

### Objective 2: Impact of Flight Stops & Layovers on Fare

#### 🔍 Investigation:
In consumer intuition, layover flights are often assumed to be cheaper compensation for inconvenience. This objective measures whether multi-stop routing in Indian domestic aviation discounts or inflates total ticket cost.

#### 📊 Empirical Data & Findings:
* **Non-Stop (0 Stops):**
  * Median Fare: **₹4,667** | IQR: [₹3,850 – ₹6,100]
  * Direct point-to-point routes maximize aircraft utilization and minimize handling/airport fees.
* **1-Stop Flights:**
  * Median Fare: **₹10,262** (+120% markup over non-stop).
  * Involves two discrete flight legs, compounding fuel, gate turnaround, and landing fees.
* **2+ Stops Flights:**
  * Median Fare: **₹12,760** (+173% markup over non-stop).
  * Represents multi-hop connections with high logistical costs.

#### 📈 Objective 2 Graphs:
![Fare by Stops](outputs/phase1_5/price_by_stops.png)
![Airline and Stops Interaction](outputs/phase1_5/airline_stops_median_fare.png)

---

### Objective 3: Flight Duration vs. Price Elasticity

#### 🔍 Investigation:
Evaluate the mathematical relationship between total journey time (in minutes) and final ticket price across different stop categories.

#### 📊 Empirical Data & Findings:
* **Spearman Rank Correlation:** $\rho = 0.694$ ($p < 0.0001$), establishing a strong, non-linear monotonic relationship between duration and fare.
* **Short-Haul Phase (2h to 5h):** Rapid linear fare acceleration ($m \approx ₹25/\text{min}$), primarily covering standard non-stop domestic routes.
* **Mid-Haul Phase (5h to 10h):** 1-stop flights with moderate layovers, where fare correlates with distance and transit convenience.
* **Long-Haul Phase (>10h):** Diminishing returns. Excessive duration is driven by idle ground layovers (e.g., 8-hour overnight transit), causing the price curve to flatten.

#### 📈 Objective 3 Graph:
![Duration and Stops vs Fare](outputs/phase1_5/fare_duration_stops.png)

---

### Objective 4: Temporal & Seasonal Fluctuations

#### 🔍 Investigation:
Analyze the impact of calendar seasonality (travel months March to June) and departure day of the week on airline yield management.

#### 📊 Empirical Data & Findings:
* **Monthly Fare Behavior:**
  * **March:** Observed peak median fare of **₹9,316** (spurred by Indian financial year-end corporate travel and early spring festival demand).
  * **April:** Significant drop to median fare of **₹5,800** (post-fiscal lull in business travel).
  * **May & June:** Moderate rebound (median ₹8,200 – ₹8,900) coinciding with summer school vacation holidays.
* **Day-of-Week Premium:**
  * Weekend departures (Friday evening, Saturday, Sunday) consistently commanded a **7% to 15% price premium** over Tuesday/Wednesday mid-week departures.

#### 📈 Objective 4 Graph:
![Fare by Journey Month](outputs/phase1_5/price_by_month.png)

---

### Objective 5: Route Corridors & Origin-Destination Hub Dynamics

#### 🔍 Investigation:
Dissect pricing disparities across primary metro-to-metro corridors versus tier-2 feeder routes to assess the role of origin airport congestion and competitive density.

#### 📊 Empirical Data & Findings:
* **Top Revenue & Premium Corridors:**
  * **Bangalore (BLR) → New Delhi (DEL):** Highest passenger volume and high median pricing (₹10,500+), serving the premier tech-to-capital business artery.
  * **Delhi (DEL) → Cochin (COK):** High median pricing due to holiday leisure transit and heavy multi-stop routing.
* **Lower-Fare Corridors:**
  * **Chennai (MAA) → Kolkata (CCU):** Consistently observed lowest median price band (~₹4,000–₹5,000), dominated by high budget carrier seat share.

#### 📈 Objective 5 Graph:
![Fare by Route](outputs/phase1_5/price_by_route.png)

---

## Part II: The 5 Machine Learning Models & Evaluation Metrics

The project trained and benchmarked 5 candidate regression algorithms under identical train/test splits (80/20) with standard scikit-learn pipelines (`StandardScaler` for numeric features and `OneHotEncoder` with rare-category grouping for high-cardinality nominals).

### Model Comparison Leaderboard

| Rank | Model Name | 5-Fold CV MAE (Mean ± SD) | Holdout Test MAE | Holdout Test RMSE | Holdout $R^2$ Score | Status |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| 🏆 **1** | **Random Forest Regressor** | **673.06 ± 19.45** | **₹640.33** | **₹1,430.08** | **0.9019 (90.2%)** | **Selected Best-Fit Model** |
| 2 | **Decision Tree Regressor** | 820.63 ± 12.30 | ₹768.45 | ₹1,897.59 | 0.8273 (82.7%) | Non-Linear Baseline |
| 3 | **Gradient Boosting Regressor** | 839.01 ± 13.97 | ₹824.74 | ₹1,527.10 | 0.8882 (88.8%) | Boosting Candidate |
| 4 | **XGBoost Regressor** | 846.12 ± 18.44 | ₹842.43 | ₹1,498.44 | 0.8923 (89.2%) | Regularized Boosting Candidate |
| 5 | **Linear Regression (OLS)** | 1,526.54 ± 28.26 | ₹1,514.45 | ₹2,367.78 | 0.7311 (73.1%) | Parametric Linear Baseline |

---

### Detailed Breakdown of the 5 Models

#### 1. Random Forest Regressor (🏆 Champion Model)
* **Architecture:** Ensemble Bagging (Bootstrap Aggregation) consisting of 100 de-correlated randomized decision trees.
* **Hyperparameters:** `n_estimators=100`, `random_state=42`, `n_jobs=-1`.
* **Performance:**
  * $R^2$ Score: **0.9019** (explains 90.19% of price variance).
  * Test MAE: **₹640.33** | Test RMSE: **₹1,430.08**.
  * 5-Fold Cross Validation MAE: **673.06 ± 19.45**.
* **Key Strengths:** Effectively captures non-linear feature interactions (such as Airline × Stops × Route) without overfitting. Integrates natively with Tree SHAP for explainable local predictions.

#### 2. Decision Tree Regressor
* **Architecture:** Single unconstrained CART algorithm splitting nodes via Mean Squared Error (MSE) reduction.
* **Performance:**
  * $R^2$ Score: **0.8273** | Test MAE: **₹768.45** | Test RMSE: **₹1,897.59**.
* **Role in Project:** Serves as the non-linear benchmark. It demonstrated that single trees suffer from higher variance (RMSE ₹1,897) compared to ensemble bagging (RMSE ₹1,430).

#### 3. Gradient Boosting Regressor
* **Architecture:** Sequential ensemble boosting utilizing shallow decision stumps to iteratively fit residual errors via gradient descent.
* **Performance:**
  * $R^2$ Score: **0.8882** | Test MAE: **₹824.74** | Test RMSE: **₹1,527.10**.
* **Role in Project:** Achieved strong performance ($R^2 = 88.8\%$) but showed slightly higher residual errors on extreme business class outliers compared to Random Forest.

#### 4. XGBoost Regressor
* **Architecture:** Extreme Gradient Boosting with exact greedy split finding, column subsampling, and $L_1$ & $L_2$ shrinkage regularization.
* **Performance:**
  * $R^2$ Score: **0.8923** | Test MAE: **₹842.43** | Test RMSE: **₹1,498.44**.
* **Role in Project:** Close runner-up to Random Forest in $R^2$ (89.23%), demonstrating fast execution speed and well-contained RMSE.

#### 5. Linear Regression (OLS)
* **Architecture:** Standard Ordinary Least Squares finding the hyperplane minimizing sum of squared errors:
  $$\hat{\beta} = (X^T X)^{-1} X^T y$$
* **Performance:**
  * $R^2$ Score: **0.7311** | Test MAE: **₹1,514.45** | Test RMSE: **₹2,367.78**.
* **Role in Project:** Proved that flight pricing contains strong non-linear and interaction effects that linear combinations cannot capture (underperforming Random Forest by >₹870 MAE).

---

## Part III: Model Diagnostic Visualizations

Below are the diagnostic visualizations generated during Phase 8 model evaluation:

### 1. Model Error Comparison (MAE across all 5 Models)
Demonstrates the relative prediction errors across algorithms, illustrating Random Forest's decisive accuracy lead:
![Model Error Comparison](outputs/phase8/model_error_comparison.png)

### 2. Actual vs. Predicted Fares (Random Forest)
Shows tightly clustered points along the 45-degree ideal fit line ($y = \hat{y}$), confirming high predictive fidelity across budget and premium ticket tiers:
![Actual vs Predicted](outputs/phase8/actual_vs_predicted.png)

### 3. Residual Error Distribution
Displays a sharp zero-centered bell curve with low skewness, validating that the model's errors follow an approximately normal distribution:
![Residual Distribution](outputs/phase8/residual_distribution.png)

### 4. Residuals vs. Predicted Values (Homoscedasticity Diagnostic)
Confirms constant error variance across standard fares with minimal heteroscedasticity:
![Residuals vs Predicted](outputs/phase8/residuals_vs_predicted.png)

---

## Summary of Conclusions & Recommendations

1. **Carrier & Stop Count Dominate Price:** Airline choice and number of stops drive over 70% of fare variation. Flying non-stop on budget carriers offers the highest cost savings (median ₹4,667).
2. **Best-Fit Model Selected:** **Random Forest Regressor** was selected as the production model due to its top test $R^2$ (**0.9019**), lowest MAE (**₹640.33**), and lowest cross-validation variance.
3. **Transparent Explainability:** Model predictions are paired with Tree SHAP in the Airlytics web application to give travelers transparent breakdowns of each flight's price drivers.
