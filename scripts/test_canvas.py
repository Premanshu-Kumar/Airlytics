"""
Airlytics Major Technical Project Report Generator
Compliant with Academic Criteria: 30 to 80 Pages
Covers:
1. Introduction
2. Source of dataset
3. EDA process
4. Analysis on dataset (8 distinct detailed analyses, each with i. Intro, ii. General Description, iii. Specific Requirements, functions and formulas, iv. Analysis results, v. Visualization)
5. Conclusion
6. Future scope
7. References
"""

import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas to dynamically compute and print 'Page X of Y' on all pages
    along with running header and footer rules.
    """
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
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        
        # Omit header and footer on cover page (Page 1)
        if self._pageNumber > 1:
            # Running Header
            self.setFont("Helvetica-Bold", 8)
            self.setFillColor(colors.HexColor("#1E3A8A")) # Dark Blue
            self.drawString(54, 755, "AIRLYTICS: COMPREHENSIVE FLIGHT FARE ESTIMATION & ANALYTICS")
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#64748B"))
            self.drawRightString(612 - 54, 755, "DATA SCIENCE & ML PROJECT REPORT")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.6)
            self.line(54, 747, 612 - 54, 747)

            # Running Footer
            self.line(54, 45, 612 - 54, 45)
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#64748B"))
            self.drawString(54, 33, "Academic Project Report — Machine Learning & Predictive Analytics")
            page_str = f"Page {self._pageNumber} of {page_count}"
            self.drawRightString(612 - 54, 33, page_str)

        self.restoreState()

print("NumberedCanvas defined.")
