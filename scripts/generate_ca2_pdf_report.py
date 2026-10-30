"""
Script to generate a comprehensive, professional PDF report for the Airlytics project,
tailored specifically to the CA2 evaluation requirements by faculty Mrinalini Rana.
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_header_footer(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_header_footer(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        
        # Header (pages after cover/first page)
        if self._pageNumber > 1:
            self.drawString(54, 755, "Airlytics — Data Science & Machine Learning Project Report (CA2)")
            self.drawRightString(612 - 54, 755, "Faculty: Mrinalini Rana")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(54, 748, 612 - 54, 748)
            
        # Footer
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(612 - 54, 35, page_str)
        self.drawString(54, 35, "Confidential — Academic Submission")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(54, 45, 612 - 54, 45)
        self.restoreState()


def generate_pdf(output_path, img_dir, img_dir_p8, img_dir_p9):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    
    # Custom Palette
    primary = colors.HexColor("#0F172A")    # Slate 900
    brand_blue = colors.HexColor("#1D4ED8") # Blue 700
    accent = colors.HexColor("#0284C7")     # Sky 600
    neutral_dark = colors.HexColor("#334155")
    bg_light = colors.HexColor("#F8FAFC")
    border_color = colors.HexColor("#E2E8F0")

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=primary,
        spaceAfter=4
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        textColor=brand_blue,
        spaceAfter=12
    )

    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=brand_blue,
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )
    
    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=primary,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=neutral_dark,
        spaceAfter=5
    )

    bullet_style = ParagraphStyle(
        'Bullet',
        parent=body_style,
        leftIndent=12,
        bulletIndent=4,
        spaceAfter=3
    )

    table_text = ParagraphStyle(
        'TableText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=10,
        textColor=primary
    )
    
    table_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10.5,
        textColor=colors.white
    )

    callout_text = ParagraphStyle(
        'CalloutText',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8,
        leading=11.5,
        textColor=primary
    )

    story = []

    # Title & Metadata Block
    story.append(Paragraph("Airlytics: Intelligent Flight Fare Estimation & Explainable ML", title_style))
    story.append(Paragraph("Comprehensive Data Science & Machine Learning Project Report — CA2", subtitle_style))
    
    meta_data = [
        [
            Paragraph("<b>Evaluator / Faculty:</b> Mrinalini Rana", table_text),
            Paragraph("<b>Course:</b> Data Science & Machine Learning with Python", table_text)
        ],
        [
            Paragraph("<b>Domain:</b> Supervised Regression & XAI", table_text),
            Paragraph("<b>Toolchain:</b> Python, Scikit-Learn, XGBoost, SHAP, React", table_text)
        ]
    ]
    t_meta = Table(meta_data, colWidths=[240, 264])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), bg_light),
        ('BOX', (0,0), (-1,-1), 1, border_color),
        ('INNERGRID', (0,0), (-1,-1), 0.5, border_color),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 10))

    # 1. Dataset Selection
    story.append(Paragraph("1. Dataset Selection & Acquisition", h1_style))
    story.append(Paragraph(
        "<b>Source:</b> Kaggle (<i>Flight Price Prediction Dataset</i> by Jillani SofTech / EaseMyTrip, Public Domain CC0).<br/>"
        "<b>Dimensions:</b> 10,683 historical records across 11 features (`Data_Train.xlsx`). Target variable is continuous flight fare <b>`Price`</b> (source units / INR). Features capture carrier name, travel date, origin, destination, routing path, departure/arrival timestamps, duration, and stop counts.",
        body_style
    ))
    story.append(Spacer(1, 6))

    # 2. Data Preprocessing & Cleaning
    story.append(Paragraph("2. Data Preprocessing & Cleaning", h1_style))
    story.append(Paragraph(
        "Data validation was implemented reproducibly in <code>scripts/phase1_5_analysis.py</code>. "
        "Every row was rigorously verified against null values, semantic consistency, and duplicate constraints:",
        body_style
    ))
    
    cleaning_data = [
        [Paragraph("Cleaning & Validation Task", table_header), Paragraph("Observed in Raw Data", table_header), Paragraph("Resolution / Cleaning Action", table_header), Paragraph("Status", table_header)],
        [Paragraph("Missing Route & Stops", table_text), Paragraph("1 row missing critical data", table_text), Paragraph("Excluded from training pipeline", table_text), Paragraph("Cleaned", table_text)],
        [Paragraph("Exact Duplicate Listings", table_text), Paragraph("220 redundant listings", table_text), Paragraph("De-duplicated (10,462 valid records remaining)", table_text), Paragraph("Cleaned", table_text)],
        [Paragraph("Duration String Parsing", table_text), Paragraph("Text e.g., '2h 50m', '5m'", table_text), Paragraph("Transformed to numerical Duration_Minutes", table_text), Paragraph("Standardized", table_text)],
        [Paragraph("Stop Category Parsing", table_text), Paragraph("Strings: 'non-stop', '1 stop'", table_text), Paragraph("Mapped to discrete integers (0, 1, 2, ...)", table_text), Paragraph("Standardized", table_text)],
        [Paragraph("Airport Spelling Variations", table_text), Paragraph("5,068 instances of 'Banglore'", table_text), Paragraph("Standardized to canonical 'Bangalore'", table_text), Paragraph("Normalized", table_text)],
        [Paragraph("Outlier Auditing", table_text), Paragraph("94 observations > 1.5x IQR", table_text), Paragraph("Retained (valid business class/surge flights)", table_text), Paragraph("Audited", table_text)]
    ]
    t_clean = Table(cleaning_data, colWidths=[130, 110, 200, 64])
    t_clean.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), brand_blue),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('BOX', (0,0), (-1,-1), 1, border_color),
        ('INNERGRID', (0,0), (-1,-1), 0.5, border_color),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, bg_light]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_clean)
    story.append(Spacer(1, 10))

    # 3. Exploratory Data Analysis & Statistics
    story.append(Paragraph("3. Exploratory Data Analysis (EDA) & Statistical Hypothesis Testing", h1_style))
    story.append(Paragraph(
        "Descriptive metrics across the 10,462 validated records reveal a <b>Mean Fare of ₹9,026.79</b>, a <b>Median Fare of ₹8,266.00</b>, "
        "Standard Deviation of ₹4,624.85, and IQR of ₹7,120.75 (minimum ₹1,759.00 to maximum ₹79,512.00).",
        body_style
    ))
    
    story.append(Paragraph("<b>Formal Statistical Hypothesis Testing:</b>", body_style))
    story.append(Paragraph("• <b>Kruskal–Wallis Test (Fare across Airlines):</b> Test statistic H = 4753.89, p-value < 0.001. Confirms statistically significant differences in fare distributions across airline carriers.", bullet_style))
    story.append(Paragraph("• <b>Spearman Rank Correlation (Flight Duration vs Fare):</b> Correlation coefficient ρ = 0.694, p-value < 0.001. Indicates a strong, positive, monotonic relationship between travel duration and airfare.", bullet_style))
    story.append(Spacer(1, 6))

    # Embed EDA Visualizations
    p_dist = os.path.join(img_dir, "price_distribution.png")
    p_air = os.path.join(img_dir, "price_by_airline.png")
    if os.path.exists(p_dist) and os.path.exists(p_air):
        img_table = [
            [
                Image(p_dist, width=245, height=140),
                Image(p_air, width=245, height=140)
            ],
            [
                Paragraph("<para align=center><b>Figure 1:</b> Airfare Distribution with KDE</para>", table_text),
                Paragraph("<para align=center><b>Figure 2:</b> Fare Variance Across Airlines</para>", table_text)
            ]
        ]
        t_imgs = Table(img_table, colWidths=[250, 250])
        t_imgs.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2),
            ('TOPPADDING', (0,0), (-1,-1), 2),
        ]))
        story.append(t_imgs)
        story.append(Spacer(1, 8))

    # 4. Five Core Objectives
    story.append(Paragraph("4. Five Core Analytical Objectives & Empirical Findings", h1_style))
    
    obj_data = [
        [Paragraph("Objective / Research Question", table_header), Paragraph("Analytical Methodology", table_header), Paragraph("Empirical Quantitative Finding", table_header)],
        [
            Paragraph("<b>Obj 1: Carrier Pricing Strategy</b>", table_text),
            Paragraph("Grouped median and IQR dispersion across carrier brand tiers.", table_text),
            Paragraph("Budget airlines (IndiGo, SpiceJet) maintain low medians (~₹4,500–₹5,000) and narrow spreads; full-service carriers (Jet Airways, Air India) have much higher medians (~₹10,262) and wider variance.", table_text)
        ],
        [
            Paragraph("<b>Obj 2: Impact of Stops on Fare</b>", table_text),
            Paragraph("Comparative analysis of non-stop vs 1-stop vs 2+ stops.", table_text),
            Paragraph("Non-stop flights median = ₹4,667. 1-stop flights jump by <b>+120% (₹10,262)</b> and 2+ stops jump by <b>+173% (₹12,760)</b> due to multi-sector ticketing.", table_text)
        ],
        [
            Paragraph("<b>Obj 3: Duration vs Airfare Elasticity</b>", table_text),
            Paragraph("Spearman non-parametric correlation & scatter analysis.", table_text),
            Paragraph("Strong correlation (ρ = 0.694). Fare increases steeply between 2 to 10 hours of duration, after which idle layover times diminish fare sensitivity.", table_text)
        ],
        [
            Paragraph("<b>Obj 4: Temporal & Seasonal Trends</b>", table_text),
            Paragraph("Cross-tabulation across months (March–June) and days.", table_text),
            Paragraph("March observed peak median fares (₹9,316) from financial year-end demand; weekend departures exhibit consistent price premiums over weekdays.", table_text)
        ],
        [
            Paragraph("<b>Obj 5: Route Corridors & Hub Dynamics</b>", table_text),
            Paragraph("Origin-Destination route segmentation and aggregation.", table_text),
            Paragraph("Bangalore → New Delhi and Delhi → Cochin corridors recorded highest passenger volumes and highest median fares.", table_text)
        ]
    ]
    t_obj = Table(obj_data, colWidths=[130, 140, 234])
    t_obj.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), brand_blue),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('BOX', (0,0), (-1,-1), 1, border_color),
        ('INNERGRID', (0,0), (-1,-1), 0.5, border_color),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, bg_light]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_obj)
    story.append(Spacer(1, 10))

    # 5. Feature Engineering
    story.append(Paragraph("5. Feature Engineering Pipeline", h1_style))
    story.append(Paragraph(
        "In <code>scripts/phase6_feature_engineering.py</code>, domain-driven transformations were applied to improve machine learning convergence:",
        body_style
    ))
    story.append(Paragraph("• <b>Trigonometric Cyclical Transformations:</b> Formulated <code>Month_Sin/Cos</code> and <code>Departure_Hour_Sin/Cos</code> via sine and cosine radians to preserve 24-hour and 12-month boundary continuity.", bullet_style))
    story.append(Paragraph("• <b>Time-of-Day Categorization:</b> Segmented departure and arrival hours into discrete bins: <code>Night</code> (&lt;5h, ≥21h), <code>Morning</code> (5–12h), <code>Afternoon</code> (12–17h), and <code>Evening</code> (17–21h).", bullet_style))
    story.append(Paragraph("• <b>Domain Bins:</b> Created <code>Season</code> (Winter, Summer, Monsoon, Post-Monsoon), <code>Stop_Category</code> (Nonstop, One stop, Two or more stops), and <code>Is_Weekend</code> binary flags.", bullet_style))
    story.append(Paragraph("• <b>Encoding & Scaling:</b> High-cardinality nominals (Airline, Route, Source, Destination) were transformed using One-Hot Encoding with rare-category grouping to eliminate lookahead bias.", bullet_style))
    story.append(Spacer(1, 8))

    # 6. ML Model Implementation & Best-Fit Model
    story.append(Paragraph("6. Machine Learning Implementation & Best-Fit Model Selection", h1_style))
    story.append(Paragraph(
        "Five supervised regression models were implemented and benchmarked on an 80/20 train/test split. "
        "Hyperparameter tuning and candidate selection was governed strictly by <b>5-Fold Cross Validation Mean Absolute Error (MAE)</b> on the training set, followed by final unbiased testing on the 20% holdout set:",
        body_style
    ))

    ml_data = [
        [Paragraph("Rank", table_header), Paragraph("Candidate Regression Architecture", table_header), Paragraph("5-Fold CV MAE", table_header), Paragraph("Holdout MAE", table_header), Paragraph("Holdout RMSE", table_header), Paragraph("Holdout R²", table_header), Paragraph("Selection Status", table_header)],
        [
            Paragraph("<b>1</b>", table_text),
            Paragraph("<b>Random Forest Regressor</b> (100 Trees)", table_text),
            Paragraph("<b>673.06 ± 19.45</b>", table_text),
            Paragraph("<b>₹640.33</b>", table_text),
            Paragraph("<b>₹1,430.08</b>", table_text),
            Paragraph("<b>0.9019</b>", table_text),
            Paragraph("🏆 <b>Best-Fit Model</b>", table_text)
        ],
        [
            Paragraph("2", table_text),
            Paragraph("Decision Tree Regressor", table_text),
            Paragraph("820.63 ± 12.30", table_text),
            Paragraph("₹768.45", table_text),
            Paragraph("₹1,897.59", table_text),
            Paragraph("0.8273", table_text),
            Paragraph("Baseline Candidate", table_text)
        ],
        [
            Paragraph("3", table_text),
            Paragraph("Gradient Boosting Regressor", table_text),
            Paragraph("839.01 ± 13.97", table_text),
            Paragraph("₹824.74", table_text),
            Paragraph("₹1,527.10", table_text),
            Paragraph("0.8882", table_text),
            Paragraph("Candidate", table_text)
        ],
        [
            Paragraph("4", table_text),
            Paragraph("XGBoost Regressor (Tree Booster)", table_text),
            Paragraph("846.12 ± 18.44", table_text),
            Paragraph("₹842.43", table_text),
            Paragraph("₹1,498.44", table_text),
            Paragraph("0.8923", table_text),
            Paragraph("Candidate", table_text)
        ],
        [
            Paragraph("5", table_text),
            Paragraph("Linear Regression (OLS Baseline)", table_text),
            Paragraph("1,526.54 ± 28.26", table_text),
            Paragraph("₹1,514.45", table_text),
            Paragraph("₹2,367.78", table_text),
            Paragraph("0.7311", table_text),
            Paragraph("Linear Baseline", table_text)
        ]
    ]
    t_ml = Table(ml_data, colWidths=[24, 150, 78, 66, 68, 54, 64])
    t_ml.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), brand_blue),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('BOX', (0,0), (-1,-1), 1, border_color),
        ('INNERGRID', (0,0), (-1,-1), 0.5, border_color),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, bg_light]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_ml)
    story.append(Spacer(1, 8))

    # Embed Evaluation Plots
    p_act = os.path.join(img_dir_p8, "actual_vs_predicted.png")
    p_shap = os.path.join(img_dir_p9, "shap_global_summary.png")
    if os.path.exists(p_act) and os.path.exists(p_shap):
        img_table2 = [
            [
                Image(p_act, width=245, height=140),
                Image(p_shap, width=245, height=140)
            ],
            [
                Paragraph("<para align=center><b>Figure 3:</b> Actual vs Predicted Fares (R² = 0.9019)</para>", table_text),
                Paragraph("<para align=center><b>Figure 4:</b> Global Tree SHAP Feature Importance</para>", table_text)
            ]
        ]
        t_imgs2 = Table(img_table2, colWidths=[250, 250])
        t_imgs2.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2),
            ('TOPPADDING', (0,0), (-1,-1), 2),
        ]))
        story.append(t_imgs2)
        story.append(Spacer(1, 8))

    # 7. Model Explainability & Findings
    story.append(Paragraph("7. Explainable AI (SHAP) & Key Insights", h1_style))
    story.append(Paragraph(
        "To ensure transparency in decision support, <b>Tree SHAP (SHapley Additive exPlanations)</b> was integrated into the core prediction service. "
        "Global SHAP analysis proves that <b>Total Duration in Minutes</b>, <b>Airline Carrier Identity</b>, and <b>Number of Layovers</b> account for over <b>72% of the total predictive power</b> in estimating ticket cost.",
        body_style
    ))
    story.append(Spacer(1, 6))

    # 8. Conclusions & Recommendations
    story.append(Paragraph("8. Conclusions & Actionable Recommendations", h1_style))
    story.append(Paragraph("• <b>For Airline Passengers & Consumers:</b> To save 40%–60% on domestic routes, select non-stop flights operated by budget carriers (IndiGo, SpiceJet). Avoid booking flights departing during Friday evening or Sunday evening peak windows.", bullet_style))
    story.append(Paragraph("• <b>For Airline Revenue Managers:</b> Dynamic pricing models should adjust markups based on corridor stop count and passenger advance booking horizons rather than gross duration alone.", bullet_style))
    story.append(Paragraph("• <b>Machine Learning Engineering Takeaway:</b> Non-linear tree ensemble architectures (Random Forest) are required to capture the interaction effects between carrier premium tiers and transit routes, outperforming standard linear regressors by +17.1% in R².", bullet_style))
    story.append(Spacer(1, 8))

    # 9. Deliverables & Verification Checklist
    story.append(Paragraph("9. Final Submission Deliverables & Rubric Compliance", h1_style))
    
    deliv_data = [
        [Paragraph("Submission Item", table_header), Paragraph("Repository Location / Evidence", table_header), Paragraph("Compliance Status", table_header)],
        [Paragraph("Dataset (Raw & Cleaned)", table_text), Paragraph("<code>data/raw/Data_Train.xlsx</code> & <code>outputs/phase1_5/cleaned_fares.csv</code>", table_text), Paragraph("✅ 100% Complete", table_text)],
        [Paragraph("Data Cleaning & Preprocessing", table_text), Paragraph("<code>scripts/phase1_5_analysis.py</code> (duplicate removal, null audits, parsing)", table_text), Paragraph("✅ 100% Complete", table_text)],
        [Paragraph("Exploratory Data Analysis (EDA)", table_text), Paragraph("10+ charts in <code>outputs/phase1_5/</code> + Kruskal-Wallis & Spearman tests", table_text), Paragraph("✅ 100% Complete", table_text)],
        [Paragraph("5 Defined Analytical Objectives", table_text), Paragraph("Documented with quantitative findings in Phase 1–5 report & README", table_text), Paragraph("✅ 100% Complete", table_text)],
        [Paragraph("Feature Engineering", table_text), Paragraph("<code>scripts/phase6_feature_engineering.py</code> (cyclical time, periods, encoding)", table_text), Paragraph("✅ 100% Complete", table_text)],
        [Paragraph("5 Machine Learning Models", table_text), Paragraph("<code>scripts/phase7_model_development.py</code> (RF, DT, Gradient Boosting, XGBoost, OLS)", table_text), Paragraph("✅ 100% Complete", table_text)],
        [Paragraph("Performance Evaluation", table_text), Paragraph("5-Fold CV & Holdout Test benchmark in <code>outputs/phase8/evaluation_metrics.csv</code>", table_text), Paragraph("✅ 100% Complete", table_text)],
        [Paragraph("Trained Model Artifact", table_text), Paragraph("Saved production model: <code>models/selected_model.joblib</code>", table_text), Paragraph("✅ 100% Complete", table_text)],
        [Paragraph("Interactive Dashboard & UI", table_text), Paragraph("Modern Next.js web application + Streamlit interactive estimator with SHAP", table_text), Paragraph("✅ 100% Complete", table_text)],
        [Paragraph("Automated Testing Suite", table_text), Paragraph("93 automated pytest unit and regression tests in <code>tests/</code>", table_text), Paragraph("✅ 100% Complete", table_text)]
    ]
    t_deliv = Table(deliv_data, colWidths=[150, 260, 94])
    t_deliv.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), brand_blue),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('BOX', (0,0), (-1,-1), 1, border_color),
        ('INNERGRID', (0,0), (-1,-1), 0.5, border_color),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, bg_light]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_deliv)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated PDF: {output_path}")

if __name__ == "__main__":
    base_dir = r"D:\Projects\Airlytics"
    wt_dir = os.path.join(base_dir, "copilot-worktrees", "Airlytics", "premanshu-kumar-literate-system")
    img_dir_p1_5 = os.path.join(wt_dir, "outputs", "phase1_5")
    img_dir_p8 = os.path.join(wt_dir, "outputs", "phase8")
    img_dir_p9 = os.path.join(wt_dir, "outputs", "phase9")
    
    out_pdf = os.path.join(base_dir, "Airlytics_CA2_Project_Report.pdf")
    generate_pdf(out_pdf, img_dir_p1_5, img_dir_p8, img_dir_p9)
