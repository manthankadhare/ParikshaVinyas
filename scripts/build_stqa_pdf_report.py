import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm, inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

PDF_PATH = r"docs/ParikshaVinyas_STQA_REPORT.pdf"
FIG_DIR = r"docs/ParikshaVinyas_Overleaf_Project/figures"

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, total_pages):
        w, h = A4
        # 1. Double border on EVERY page
        # Outer border
        self.setLineWidth(0.8)
        self.setStrokeColor(colors.HexColor("#1C4E79"))
        self.rect(8 * mm, 8 * mm, w - 16 * mm, h - 16 * mm)

        # Inner border
        self.setLineWidth(0.35)
        self.setStrokeColor(colors.HexColor("#1C4E79"))
        self.rect(10 * mm, 10 * mm, w - 20 * mm, h - 20 * mm)

        # 2. Header and Footer (from Chapter 1 onwards, page >= 7)
        if self._pageNumber >= 7:
            self.setFont("Helvetica-Bold", 8.5)
            self.setFillColor(colors.HexColor("#222222"))
            self.drawString(14 * mm, h - 17 * mm, "230102103015")
            self.drawRightString(w - 14 * mm, h - 17 * mm, "Software Testing and Quality Assurance (CO2405)")

            self.setFont("Helvetica", 8.5)
            self.setFillColor(colors.HexColor("#444444"))
            self.drawRightString(w - 14 * mm, 13 * mm, f"Page {self._pageNumber} of {total_pages}")


def build_pdf():
    doc = SimpleDocTemplate(
        PDF_PATH,
        pagesize=A4,
        leftMargin=14 * mm,
        rightMargin=14 * mm,
        topMargin=20 * mm,
        bottomMargin=20 * mm
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        "CoverTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=15,
        leading=19,
        alignment=1, # Center
        textColor=colors.HexColor("#961E1E")
    )

    sub_title_style = ParagraphStyle(
        "CoverSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=17,
        alignment=1,
        textColor=colors.HexColor("#1C4E79")
    )

    center_text = ParagraphStyle(
        "CenterText",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=11,
        leading=15,
        alignment=1,
        textColor=colors.HexColor("#222222")
    )

    center_bold = ParagraphStyle(
        "CenterBold",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=15,
        alignment=1,
        textColor=colors.HexColor("#111111")
    )

    h1_style = ParagraphStyle(
        "ChapterHeading",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=15,
        leading=19,
        alignment=1,
        textColor=colors.HexColor("#1C4E79"),
        spaceAfter=12
    )

    h2_style = ParagraphStyle(
        "SectionHeading",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#1C4E79"),
        spaceBefore=10,
        spaceAfter=6
    )

    h3_style = ParagraphStyle(
        "SubSectionHeading",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor("#333333"),
        spaceBefore=8,
        spaceAfter=4
    )

    body_style = ParagraphStyle(
        "BodyJustify",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=13.5,
        alignment=4, # Justify
        textColor=colors.HexColor("#222222"),
        spaceAfter=6
    )

    body_bold = ParagraphStyle(
        "BodyBold",
        parent=body_style,
        fontName="Helvetica-Bold"
    )

    caption_style = ParagraphStyle(
        "FigureCaption",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8.5,
        leading=11.5,
        alignment=1,
        textColor=colors.HexColor("#444444"),
        spaceBefore=4,
        spaceAfter=8
    )

    table_header = ParagraphStyle(
        "TableHeader",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8.5,
        leading=11,
        alignment=1,
        textColor=colors.white
    )

    table_cell = ParagraphStyle(
        "TableCell",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor("#222222")
    )

    table_cell_bold = ParagraphStyle(
        "TableCellBold",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor("#111111")
    )

    story = []

    # ============================================================
    # 1. COVER PAGE
    # ============================================================
    logo_path = os.path.join(FIG_DIR, "upl-logo.png")
    if os.path.exists(logo_path):
        story.append(Image(logo_path, width=420, height=135))
    story.append(Spacer(1, 8 * mm))
    story.append(Paragraph("A", center_bold))
    story.append(Spacer(1, 1.5 * mm))
    story.append(Paragraph("Mini Project Report", sub_title_style))
    story.append(Spacer(1, 1 * mm))
    story.append(Paragraph("(Software Testing and Quality Assurance (CO2405))", center_bold))
    story.append(Spacer(1, 3 * mm))
    story.append(Paragraph("on", center_text))
    story.append(Spacer(1, 2 * mm))
    story.append(Paragraph("“ParikshaVinyas – Smart Examination Hall and Seat<br/>Allocation Management System Testing”", title_style))
    story.append(Spacer(1, 6 * mm))
    story.append(Paragraph("Submitted as part of the curriculum of", center_text))
    story.append(Spacer(1, 1 * mm))
    story.append(Paragraph("Bachelor of Engineering", center_bold))
    story.append(Spacer(1, 1 * mm))
    story.append(Paragraph("in", center_text))
    story.append(Spacer(1, 1 * mm))
    story.append(Paragraph("Computer Engineering", center_bold))
    story.append(Spacer(1, 6 * mm))
    story.append(Paragraph("Submitted By", center_text))
    story.append(Spacer(1, 2 * mm))

    sub_table = [
        [Paragraph("<b>Manthan Kadhare</b>", center_text), Paragraph("<b>230102103015</b>", center_text)]
    ]
    t_sub = Table(sub_table, colWidths=[200, 200])
    t_sub.setStyle(TableStyle([("ALIGN", (0, 0), (-1, -1), "CENTER")]))
    story.append(t_sub)

    story.append(Spacer(1, 5 * mm))
    story.append(Paragraph("Under the guidance of", center_text))
    story.append(Spacer(1, 1.5 * mm))
    story.append(Paragraph("<b>Ms. Rupali Attarde</b>", center_bold))
    story.append(Spacer(1, 5 * mm))
    story.append(Paragraph("Submitted To", center_text))
    story.append(Spacer(1, 1.5 * mm))
    story.append(Paragraph("<b>Department of Computer Engineering</b>", center_bold))
    story.append(Spacer(1, 1 * mm))
    story.append(Paragraph("<b>Shroff S.R. Rotary Institute of Chemical Technology</b>", center_bold))
    story.append(Spacer(1, 1 * mm))
    story.append(Paragraph("<b>2026–2027</b>", center_bold))
    story.append(PageBreak())

    # ============================================================
    # 2. CERTIFICATE PAGE
    # ============================================================
    story.append(Paragraph("<b>Shroff S.R. Rotary Institute of Chemical Technology</b>", center_bold))
    story.append(Spacer(1, 1 * mm))
    story.append(Paragraph("<b>Department of Computer Engineering</b>", center_bold))
    story.append(Spacer(1, 1 * mm))
    story.append(Paragraph("<b>Academic Year 2026–27</b>", center_bold))
    story.append(Spacer(1, 12 * mm))
    story.append(Paragraph("CERTIFICATE", h1_style))
    story.append(Spacer(1, 8 * mm))
    cert_text = (
        "This is to certify that <b>Manthan Kadhare, (230102103015)</b> is a student of "
        "Semester VII of BE Computer Engineering, UPL University of Sustainable Technology, "
        "SRICT, Vataria, Ankleshwar, has successfully completed a Mini Project Report "
        "(<b>Software Testing and Quality Assurance</b>) (<b>CO2405</b>) on "
        "<b>“ParikshaVinyas – Smart Examination Hall and Seat Allocation Management System Testing”</b> "
        "and submitted the report during academic year 2026–27."
    )
    story.append(Paragraph(cert_text, body_style))
    story.append(Spacer(1, 20 * mm))
    story.append(Paragraph("Date: _____ / _____ / _________", body_bold))
    story.append(Spacer(1, 35 * mm))

    sig_data = [
        [Paragraph("____________________________<br/><b>Subject Coordinator</b><br/><b>Ms. Rupali Attarde</b>", center_text),
         Paragraph("____________________________<br/><b>Head of the Department</b><br/><b>Ms. Mital Patel</b>", center_text)]
    ]
    t_sig = Table(sig_data, colWidths=[240, 240])
    story.append(t_sig)
    story.append(PageBreak())

    # ============================================================
    # 3. DECLARATION PAGE
    # ============================================================
    story.append(Spacer(1, 10 * mm))
    story.append(Paragraph("DECLARATION", h1_style))
    story.append(Spacer(1, 10 * mm))
    decl_text1 = (
        "I, <b>Manthan Kadhare (230102103015)</b>, am the student of Semester VII of "
        "BE Computer Engineering, UPL University of Sustainable Technology, SRICT, Vataria, "
        "hereby declare that this report is prepared by me based on the information gathered during "
        "the preparation of the Mini Project Report (<b>Software Testing and Quality Assurance</b>) in "
        "Semester VII."
    )
    story.append(Paragraph(decl_text1, body_style))
    story.append(Spacer(1, 4 * mm))
    decl_text2 = (
        "I further declare that the testing execution records, test cases, automation scripts, "
        "defect logs, and experimental findings presented in this report represent authentic work "
        "carried out by me on the application under test, <b>ParikshaVinyas</b>."
    )
    story.append(Paragraph(decl_text2, body_style))
    story.append(Spacer(1, 40 * mm))
    story.append(Paragraph("<b>Manthan Kadhare</b><br/><b>(230102103015)</b>", ParagraphStyle("RightSig", parent=body_bold, alignment=2)))
    story.append(PageBreak())

    # ============================================================
    # 4. ACKNOWLEDGEMENT PAGE
    # ============================================================
    story.append(Spacer(1, 10 * mm))
    story.append(Paragraph("ACKNOWLEDGEMENT", h1_style))
    story.append(Spacer(1, 10 * mm))
    ack_text1 = (
        "I would like to express my sincere gratitude to all those who have supported and guided me "
        "throughout my Mini Project Report in <b>Software Testing and Quality Assurance (CO2405)</b>."
    )
    story.append(Paragraph(ack_text1, body_style))
    story.append(Spacer(1, 3 * mm))
    ack_text2 = (
        "<b>Ms. Rupali Attarde</b>, our Subject Coordinator and Mentor, has helped me immensely with her "
        "expert guidance, insightful technical feedback, and constant support. Her meticulous reviews, "
        "ideas on software quality assurance, and encouragement have been invaluable in structuring "
        "comprehensive test suites and completing this report."
    )
    story.append(Paragraph(ack_text2, body_style))
    story.append(Spacer(1, 3 * mm))
    ack_text3 = (
        "I also extend my sincere thanks to <b>Ms. Mital Patel</b>, Head of the Department of Computer Engineering, "
        "for her continuous encouragement, administrative leadership, and academic support throughout the semester."
    )
    story.append(Paragraph(ack_text3, body_style))
    story.append(Spacer(1, 3 * mm))
    ack_text4 = (
        "Finally, I want to thank the faculty members, laboratory staff, and my fellow students of the "
        "Department of Computer Engineering, Shroff S.R. Rotary Institute of Chemical Technology, "
        "UPL University of Sustainable Technology, for their direct and indirect assistance during the "
        "testing and documentation phases."
    )
    story.append(Paragraph(ack_text4, body_style))
    story.append(Spacer(1, 35 * mm))
    story.append(Paragraph("<b>Manthan Kadhare</b><br/><b>(230102103015)</b>", ParagraphStyle("RightSig2", parent=body_bold, alignment=2)))
    story.append(PageBreak())

    # ============================================================
    # 5. TABLE OF CONTENTS
    # ============================================================
    story.append(Paragraph("CONTENTS", h1_style))
    story.append(Spacer(1, 4 * mm))

    toc_items = [
        ("1", "Introduction", "7"),
        ("1.1", "Background", "7"),
        ("1.2", "Problem Statement", "7"),
        ("1.3", "Objectives", "8"),
        ("1.4", "Scope of the Project", "8"),
        ("2", "Software/Application Under Test (AUT)", "14"),
        ("2.1", "Application Overview", "14"),
        ("2.2", "Functional Requirements", "14"),
        ("2.3", "Non-Functional Requirements", "15"),
        ("2.4", "System Architecture / Application Flow", "15"),
        ("3", "Software Testing Methodology", "17"),
        ("3.1", "Testing Process", "17"),
        ("3.2", "Types of Testing Used", "17"),
        ("4", "Manual Testing", "19"),
        ("4.1", "Test Case Design", "19"),
        ("4.1.1", "Test Case Execution Summary", "21"),
        ("4.2", "Test Case Techniques", "21"),
        ("4.2.1", "Equivalence Partitioning", "21"),
        ("4.2.2", "Boundary Value Analysis", "22"),
        ("4.2.3", "Decision Table Testing", "22"),
        ("4.3", "Summary", "22"),
        ("5", "Automation Testing", "23"),
        ("5.1", "Automation Tool", "23"),
        ("5.2", "Automation Environment", "23"),
        ("5.3", "Automated Test Cases", "24"),
        ("5.3.6", "Automation Test Summary", "28"),
        ("5.4", "Summary", "28"),
        ("6", "AI-Based Testing", "29"),
        ("6.1", "Introduction to AI in Software Testing", "29"),
        ("6.2", "AI Tools Used (Gemini, Claude, NotebookLM)", "29"),
        ("6.3", "AI-Assisted Test Case Generation", "31"),
        ("6.4", "AI-Assisted Test Cases and Results", "31"),
        ("6.5", "AI-Based Test Analysis and Risk Identification", "34"),
        ("6.6", "Human Validation of AI-Generated Test Cases", "34"),
        ("6.7", "Summary", "34"),
        ("7", "Defect/Bug Reporting", "35"),
        ("7.1", "Introduction", "35"),
        ("7.2", "Detailed Defect Reports (BUG001 to BUG006)", "35"),
        ("7.3", "Summary", "39"),
        ("8", "Test Results and Analysis", "40"),
        ("8.1", "Introduction", "40"),
        ("8.2", "Test Execution Summary", "40"),
        ("8.3", "Test Result Calculation", "40"),
        ("8.4", "Pass Percentage Calculations", "41"),
        ("8.5", "Failure Percentage Calculations", "41"),
        ("8.6", "Percentage Summary", "41"),
        ("8.7", "Comparison of Testing Approaches", "42"),
        ("8.8", "Overall Test Results", "42"),
        ("8.9", "Conclusion", "43"),
        ("9", "Conclusion & Future Scope", "44"),
        ("", "REFERENCES", "45"),
        ("", "ABBREVIATIONS", "46"),
        ("", "APPENDIX", "47")
    ]

    toc_rows = []
    for num, title, page in toc_items:
        dots = ". " * int((58 - len(title) - len(num)) / 2)
        toc_rows.append([
            Paragraph(f"<b>{num}</b>", table_cell_bold),
            Paragraph(f"{title} {dots}", table_cell),
            Paragraph(f"<b>{page}</b>", table_cell_bold)
        ])
    t_toc = Table(toc_rows, colWidths=[30, 410, 40])
    t_toc.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 1),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
    ]))
    story.append(t_toc)
    story.append(PageBreak())

    # ============================================================
    # 6. LIST OF TABLES AND FIGURES
    # ============================================================
    story.append(Paragraph("LIST OF TABLES", h1_style))
    story.append(Spacer(1, 3 * mm))
    lot_items = [
        ("2.1", "Functional Requirements of ParikshaVinyas", "14"),
        ("3.1", "Testing Workflow Followed for ParikshaVinyas", "17"),
        ("3.2", "Types of Testing Used in ParikshaVinyas", "18"),
        ("4.1", "Manual Test Cases for the ParikshaVinyas Application", "19"),
        ("4.2", "Summary of Manual Test Results", "21"),
        ("4.3", "Equivalence Partitioning Test Cases", "21"),
        ("4.4", "Boundary Value Analysis Test Cases", "22"),
        ("4.5", "Decision Table Test Scenarios for Examination Scheduling", "22"),
        ("5.1", "Automation Testing Environment", "23"),
        ("5.7", "Summary of Selected Automation Test Cases", "28"),
        ("7.1", "Defect Report for BUG001", "35"),
        ("7.2", "Defect Report for BUG002", "36"),
        ("7.3", "Defect Report for BUG003", "36"),
        ("7.4", "Defect Report for BUG004", "37"),
        ("7.5", "Defect Report for BUG005", "38"),
        ("7.6", "Defect Report for BUG006", "38"),
        ("8.1", "Summary of Test Execution Across All Approaches", "40"),
        ("8.2", "Pass and Fail Percentage Summary", "41"),
        ("8.3", "Comparison of Applied Testing Approaches", "42"),
        ("8.4", "Overall Software Quality and Verification Metrics", "42"),
    ]
    lot_rows = []
    for num, title, page in lot_items:
        dots = ". " * int((58 - len(title) - len(num)) / 2)
        lot_rows.append([
            Paragraph(f"<b>{num}</b>", table_cell_bold),
            Paragraph(f"{title} {dots}", table_cell),
            Paragraph(f"<b>{page}</b>", table_cell_bold)
        ])
    t_lot = Table(lot_rows, colWidths=[30, 410, 40])
    t_lot.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 1),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
    ]))
    story.append(t_lot)

    story.append(Spacer(1, 6 * mm))
    story.append(Paragraph("LIST OF FIGURES", h1_style))
    story.append(Spacer(1, 3 * mm))
    lof_items = [
        ("1.1", "ParikshaVinyas Authentication and Login Module", "9"),
        ("1.2", "ParikshaVinyas Administrator Dashboard and Real-Time Metrics", "9"),
        ("1.3", "ParikshaVinyas Student Management and Directory Module", "10"),
        ("1.4", "ParikshaVinyas Examination Hall Directory", "10"),
        ("1.5", "Interactive Hall Seating Layout and Desk Blocking Matrix", "11"),
        ("1.6", "Academic Courses Directory Module", "11"),
        ("1.7", "Academic Subjects Management Module", "12"),
        ("1.8", "Examination Timetable Scheduling Module", "12"),
        ("1.9", "Automated Seat Allocation Wizard and Strategy Selection", "12"),
        ("1.10", "Seat Allocation Execution Summary and Capacity Audit", "13"),
        ("1.11", "Interactive Visual Seating Grid with Modal Detail Inspection", "13"),
        ("1.12", "Manual Seat Allocation and Candidate Reassignment Interface", "13"),
        ("1.13", "Examination Reports and Official PDF Export Center", "14"),
        ("1.14", "Invigilator Portal and Hall Duty Schedule", "14"),
        ("1.15", "Student Portal and Personalized Seating Slip", "14"),
        ("1.16", "System Activity and Security Audit Logs", "14"),
        ("2.1", "ParikshaVinyas System Architecture and Workflow Flowchart", "16"),
        ("5.1", "AT-01: Student Registration Form with Empty Fields", "24"),
        ("5.2", "AT-01: Required-Field Validation Alert", "24"),
        ("5.3", "AT-01: Automated Test Result in Terminal", "24"),
        ("5.4", "AT-02: Registration Form with Existing Enrollment Number", "25"),
        ("5.5", "AT-02: Duplicate Enrollment Validation Warning", "25"),
        ("5.6", "AT-02: Automated Test Result in Terminal", "25"),
        ("5.7", "AT-03: Overlapping Examination Timetable Form", "26"),
        ("5.8", "AT-03: Timetable Collision Rejection Notification", "26"),
        ("5.9", "AT-03: Automated Test Result in Terminal", "26"),
        ("5.10", "AT-04: Authenticated Student Portal Session", "27"),
        ("5.11", "AT-04: HTTP 403 Forbidden Access Control Response", "27"),
        ("5.12", "AT-04: Automated Test Result in Terminal", "27"),
        ("5.13", "AT-05: Allocation Form with Capacity Overflow Condition", "28"),
        ("5.14", "AT-05: Insufficient Capacity Warning and Atomic Rollback", "28"),
        ("5.15", "AT-05: Automated Test Result in Terminal", "28"),
        ("6.1", "Google Gemini: AI-Assisted Test Case Generation", "30"),
        ("6.2", "Claude: Review of Test Scenarios and Invariant Logic", "30"),
        ("6.3", "Google NotebookLM: Risk and Defect Correlation Analysis", "30"),
        ("6.4", "AI-01: In-App AI QA Workspace and Test Case Generation", "32"),
        ("6.5", "AI-01: Checkerboard Seat Allocation Verification in Grid", "32"),
        ("6.6", "AI-02: Damaged Desk Exclusion in Visual Layout Grid", "32"),
        ("6.7", "AI-03: Multi-Column Search and Directory Filtering", "33"),
        ("6.8", "AI-04: Reports Management Center for PDF Seating Slips", "33"),
        ("6.9", "AI-04: Multi-Hall PDF Seating Arrangement Preview", "33"),
        ("6.10", "AI-05: IDOR Prevention Response on Unauthorized Roster Export", "34"),
        ("7.1", "BUG001: Verification of Atomic Rollback on Capacity Shortage", "35"),
        ("7.2", "BUG002: Rejection of Overlapping Examination Timetable", "36"),
        ("7.3", "BUG003: Guard Preventing Blocking of Occupied Desks", "37"),
        ("7.4", "BUG004: Graceful Handling of In-Batch Duplicate Enrollment Numbers", "37"),
        ("7.5", "BUG005: Allocation Preservation Guard During Capacity Shortage", "38"),
        ("7.6", "BUG006: HTTP 403 Forbidden Response Blocking Unauthorized Roster Export", "39"),
        ("A.1", "STQA Test Execution Matrix and Defect Tracking Session in Progress", "47"),
    ]
    lof_rows = []
    for num, title, page in lof_items:
        dots = ". " * int((58 - len(title) - len(num)) / 2)
        lof_rows.append([
            Paragraph(f"<b>{num}</b>", table_cell_bold),
            Paragraph(f"{title} {dots}", table_cell),
            Paragraph(f"<b>{page}</b>", table_cell_bold)
        ])
    t_lof = Table(lof_rows, colWidths=[30, 410, 40])
    t_lof.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 1),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
    ]))
    story.append(t_lof)
    story.append(PageBreak())

    # Helper for inserting figures
    def add_fig(filename, caption_text, width=420, height=210):
        p = os.path.join(FIG_DIR, filename)
        if os.path.exists(p):
            story.append(Image(p, width=width, height=height))
            story.append(Paragraph(caption_text, caption_style))
        else:
            print("Missing fig:", p)

    # ============================================================
    # CHAPTER 1: INTRODUCTION
    # ============================================================
    story.append(Paragraph("Chapter 1", ParagraphStyle("ChPre", parent=h1_style, fontSize=13, spaceAfter=2)))
    story.append(Paragraph("INTRODUCTION", h1_style))
    story.append(Spacer(1, 4 * mm))

    story.append(Paragraph("1.1 Background", h2_style))
    story.append(Paragraph(
        "Software testing is an essential discipline within the Software Development Life Cycle (SDLC) aimed at "
        "systematically evaluating an application's functional correctness, algorithmic robustness, data integrity, "
        "and security access boundaries. Testing ensures that the software complies strictly with operational requirements "
        "and behaves predictably under extreme boundary conditions.",
        body_style
    ))
    story.append(Paragraph(
        "In collegiate academic administration, examination planning is a mission-critical, zero-tolerance operational domain. "
        "Every semester, university examination cells must coordinate seat allocations for thousands of candidates across "
        "multiple departments, faculties, and physical halls. Historically, manual allocation procedures have suffered from "
        "severe vulnerabilities: accidental room over-allocation, duplicate desk assignments, placing candidates of the "
        "same academic cohort adjacent to each other (enabling unfair practices), and timetable scheduling clashes.",
        body_style
    ))
    story.append(Paragraph(
        "<b>ParikshaVinyas (परीक्षाविन्यास)</b> is an automated, web-based examination hall planning and seat allocation "
        "management system developed to address these operational challenges. As an application under test for Software "
        "Testing and Quality Assurance (STQA), ParikshaVinyas provides a rich testing target: it incorporates algorithmic "
        "seating distribution rules, dynamic visual seating matrices, multi-role access controls (Admin, Invigilator, Student), "
        "on-the-fly binary PDF generation, and strict transactional database uniqueness guarantees.",
        body_style
    ))

    story.append(Paragraph("1.2 Problem Statement", h2_style))
    story.append(Paragraph(
        "Traditional collegiate examination cell operations face significant manual bottlenecks and points of failure:",
        body_style
    ))
    story.append(Paragraph(
        "• <b>Complex Capacity Computations:</b> Usable hall capacity requires calculating physical rows and columns while "
        "dynamically subtracting damaged, obstructed, or maintenance-blocked desks. Manual calculations frequently lead to "
        "desk shortages on the morning of examinations.<br/>"
        "• <b>Academic Malpractice Risks:</b> Manual allotment often seats students from the same department and semester side-by-side, "
        "creating opportunities for cheating and collusion.<br/>"
        "• <b>Timetable Clashes:</b> Scheduling multiple department examinations without automated temporal conflict detection "
        "causes room collisions and student exam overlaps.<br/>"
        "• <b>Transactional Fragility:</b> In legacy systems, allocating seats for an exam with insufficient capacity often leads "
        "to partial database commits, corrupting student records and creating orphaned allocations.<br/>"
        "• <b>Absence of Role-Based Security:</b> Invigilators and students often lack partitioned interfaces, introducing "
        "Insecure Direct Object Reference (IDOR) vulnerabilities and risks of unauthorized data access.",
        body_style
    ))

    story.append(Paragraph("1.3 Objectives", h2_style))
    story.append(Paragraph(
        "The primary objectives of this STQA engineering project are:",
        body_style
    ))
    story.append(Paragraph(
        "1. To conduct an exhaustive quality assurance audit of ParikshaVinyas across all functional modules.<br/>"
        "2. To design and execute rigorous manual test suites utilizing formal black-box techniques: Boundary Value Analysis (BVA), "
        "Equivalence Partitioning (EP), Decision Tables, and State Transition Analysis.<br/>"
        "3. To implement automated end-to-end browser regression test suites using Python Playwright and pytest in Chromium.<br/>"
        "4. To explore and evaluate cutting-edge AI-assisted testing methodologies (Google Gemini, Claude, and Google NotebookLM) "
        "for scenario derivation and architectural risk identification.<br/>"
        "5. To systematically log, reproduce, resolve, and regression-test identified software defects.<br/>"
        "6. To quantitatively compute testing metrics (Pass/Fail ratios, defect density) and provide actionable quality recommendations.",
        body_style
    ))

    story.append(Paragraph("1.4 Scope of the Project", h2_style))
    story.append(Paragraph(
        "The testing scope encompasses all functional modules and user interfaces of ParikshaVinyas:",
        body_style
    ))

    story.append(Paragraph("1.4.1 Authentication and Access Control", h3_style))
    story.append(Paragraph(
        "Validates session establishment, role redirection, and brute-force rejection for System Administrators, "
        "Exam Invigilators, and Students (Figure 1.1).",
        body_style
    ))
    add_fig("fig1_01_login.png", "Figure 1.1: ParikshaVinyas Authentication and Login Module", width=420, height=210)

    story.append(Paragraph("1.4.2 Administrator Dashboard", h3_style))
    story.append(Paragraph(
        "Displays real-time examination statistics, active hall capacity meters, scheduled examination summaries, and "
        "interactive metric cards (Figure 1.2).",
        body_style
    ))
    add_fig("fig1_02_dashboard.png", "Figure 1.2: ParikshaVinyas Administrator Dashboard and Real-Time Metrics", width=420, height=210)

    story.append(Paragraph("1.4.3 Student Management Module", h3_style))
    story.append(Paragraph(
        "Supports single candidate registration, bulk CSV ingestion, substring enrollment searches, and course/semester "
        "directory filtering (Figure 1.3).",
        body_style
    ))
    add_fig("fig1_03_students.png", "Figure 1.3: ParikshaVinyas Student Management and Directory Module", width=420, height=210)

    story.append(Paragraph("1.4.4 Examination Hall Management and Layout Grid", h3_style))
    story.append(Paragraph(
        "Manages building blocks, dimension configurations (rows × columns), and interactive seat blocking where broken desks "
        "can be toggled to 'Blocked' state (Figures 1.4 and 1.5).",
        body_style
    ))
    add_fig("fig1_04_halls.png", "Figure 1.4: ParikshaVinyas Examination Hall Directory", width=420, height=200)
    add_fig("fig1_05_hall_layout.png", "Figure 1.5: Interactive Hall Seating Layout and Desk Blocking Matrix", width=420, height=200)

    story.append(Paragraph("1.4.5 Academic Course and Subject Management", h3_style))
    story.append(Paragraph(
        "Maintains degree curricula, subject codes, and semester credit mappings with referential integrity constraints (Figures 1.6 and 1.7).",
        body_style
    ))
    add_fig("fig1_06_courses.png", "Figure 1.6: Academic Courses Directory Module", width=420, height=195)
    add_fig("fig1_07_subjects.png", "Figure 1.7: Academic Subjects Management Module", width=420, height=195)

    story.append(Paragraph("1.4.6 Examination Timetable Scheduling", h3_style))
    story.append(Paragraph(
        "Schedules formal examinations with date, time interval, course, and semester associations while enforcing collision detection (Figure 1.8).",
        body_style
    ))
    add_fig("fig1_08_exams.png", "Figure 1.8: Examination Timetable Scheduling Module", width=420, height=200)

    story.append(Paragraph("1.4.7 Automated Seat Allocation Engine", h3_style))
    story.append(Paragraph(
        "Executes multi-strategy allocation (Sequential, Seeded Random, Mixed-Course Checkerboard) with atomic transactional guarantees (Figures 1.9 and 1.10).",
        body_style
    ))
    add_fig("fig1_09_allocation_wizard.png", "Figure 1.9: Automated Seat Allocation Wizard and Strategy Selection", width=420, height=200)
    add_fig("fig1_10_allocation_summary.png", "Figure 1.10: Seat Allocation Execution Summary and Capacity Audit", width=420, height=200)

    story.append(Paragraph("1.4.8 Visual Seating Grid and Manual Allocation", h3_style))
    story.append(Paragraph(
        "Renders visual seat matrices (Allocated, Available, Blocked) and permits manual candidate reassignment and bilateral seat swapping (Figures 1.11 and 1.12).",
        body_style
    ))
    add_fig("fig1_11_visual_grid.png", "Figure 1.11: Interactive Visual Seating Grid with Modal Detail Inspection", width=420, height=200)
    add_fig("fig1_12_manual_allocation.png", "Figure 1.12: Manual Seat Allocation and Candidate Reassignment Interface", width=420, height=200)

    story.append(Paragraph("1.4.9 Examination Reports and PDF Generation", h3_style))
    story.append(Paragraph(
        "Streams binary ReportLab PDF seating charts, student desk slips, and hall attendance rosters (Figure 1.13).",
        body_style
    ))
    add_fig("fig1_13_reports.png", "Figure 1.13: Examination Reports and Official PDF Export Center", width=420, height=200)

    story.append(Paragraph("1.4.10 Invigilator, Student Portals, and Activity Logs", h3_style))
    story.append(Paragraph(
        "Dedicated role-partitioned portals for invigilators and students, backed by an immutable system audit trail (Figures 1.14, 1.15, and 1.16).",
        body_style
    ))
    add_fig("fig1_14_invigilator.png", "Figure 1.14: Invigilator Portal and Hall Duty Schedule", width=420, height=195)
    add_fig("fig1_15_student_portal.png", "Figure 1.15: Student Portal and Personalized Seating Slip", width=420, height=195)
    add_fig("fig1_16_activity_logs.png", "Figure 1.16: System Activity and Security Audit Logs", width=420, height=195)

    story.append(PageBreak())

    # ============================================================
    # CHAPTER 2: APPLICATION UNDER TEST
    # ============================================================
    story.append(Paragraph("Chapter 2", ParagraphStyle("ChPre2", parent=h1_style, fontSize=13, spaceAfter=2)))
    story.append(Paragraph("SOFTWARE/APPLICATION UNDER TEST (AUT)", h1_style))
    story.append(Spacer(1, 4 * mm))

    story.append(Paragraph("2.1 Application Overview", h2_style))
    story.append(Paragraph(
        "<b>ParikshaVinyas</b> is engineered using a decoupled, 4-tier application architecture: Presentation Layer, "
        "Security & Routing Layer, Business Service Layer, and Persistence Layer. The backend is implemented in Python 3.11 "
        "using the Flask microframework. Persistence is managed via SQLAlchemy ORM over SQLite, enforcing composite unique constraints "
        "and referential integrity cascades. PDF reporting is handled through Python ReportLab.",
        body_style
    ))

    story.append(Paragraph("2.2 Functional Requirements", h2_style))
    story.append(Paragraph("The functional requirements of the ParikshaVinyas system are listed in Table 2.1.", body_style))

    fr_data = [
        [Paragraph("<b>Req ID</b>", table_header), Paragraph("<b>Requirement Description</b>", table_header)],
        [Paragraph("<b>FR01</b>", table_cell_bold), Paragraph("System shall authenticate users with role-based credentials (Admin, Invigilator, Student).", table_cell)],
        [Paragraph("<b>FR02</b>", table_cell_bold), Paragraph("System shall provide an administrative dashboard displaying real-time metrics and charts.", table_cell)],
        [Paragraph("<b>FR03</b>", table_cell_bold), Paragraph("System shall support full CRUD operations for students and bulk CSV ingestion.", table_cell)],
        [Paragraph("<b>FR04</b>", table_cell_bold), Paragraph("System shall validate student enrollment numbers and emails for uniqueness.", table_cell)],
        [Paragraph("<b>FR05</b>", table_cell_bold), Paragraph("System shall manage examination halls, building blocks, and row/column grid dimensions.", table_cell)],
        [Paragraph("<b>FR06</b>", table_cell_bold), Paragraph("System shall allow administrators to mark individual desks as blocked or damaged.", table_cell)],
        [Paragraph("<b>FR07</b>", table_cell_bold), Paragraph("System shall manage degree programs, academic courses, and semester curriculum subjects.", table_cell)],
        [Paragraph("<b>FR08</b>", table_cell_bold), Paragraph("System shall schedule examinations while enforcing date and timetable collision checks.", table_cell)],
        [Paragraph("<b>FR09</b>", table_cell_bold), Paragraph("System shall execute automated allocation using Sequential, Random, and Mixed strategies.", table_cell)],
        [Paragraph("<b>FR10</b>", table_cell_bold), Paragraph("System shall enforce pre-allocation capacity verification and atomic rollback on shortage.", table_cell)],
        [Paragraph("<b>FR11</b>", table_cell_bold), Paragraph("System shall render an interactive visual grid displaying Allocated, Available, and Blocked desks.", table_cell)],
        [Paragraph("<b>FR12</b>", table_cell_bold), Paragraph("System shall permit manual seat assignment and bilateral candidate seat swapping.", table_cell)],
        [Paragraph("<b>FR13</b>", table_cell_bold), Paragraph("System shall generate downloadable ReportLab PDF seating charts and CSV data exports.", table_cell)],
        [Paragraph("<b>FR14</b>", table_cell_bold), Paragraph("System shall provide a dedicated Invigilator Portal displaying assigned hall rosters.", table_cell)],
        [Paragraph("<b>FR15</b>", table_cell_bold), Paragraph("System shall provide a secure Student Portal displaying confirmed desk allotment slips.", table_cell)],
        [Paragraph("<b>FR16</b>", table_cell_bold), Paragraph("System shall log administrative and security events into an immutable activity audit trail.", table_cell)]
    ]
    t_fr = Table(fr_data, colWidths=[60, 410])
    t_fr.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1C4E79")),
        ("ALIGN", (0, 0), (-1, 0), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CCCCCC")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8F9FA")]),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    story.append(t_fr)
    story.append(Spacer(1, 4 * mm))

    story.append(Paragraph("2.3 Non-Functional Requirements", h2_style))
    story.append(Paragraph(
        "• <b>Performance:</b> The allocation engine processes 500+ student assignments in under 250 milliseconds.<br/>"
        "• <b>Data Integrity:</b> Database-level unique constraints (`uq_exam_student_seat` and `uq_exam_hall_pos_seat`) prevent duplicate seat allocations.<br/>"
        "• <b>Security:</b> Cryptographic password hashing (PBKDF2), CSRF token validation on all POST requests, and strict RBAC authorization guards.<br/>"
        "• <b>Usability:</b> Mobile-responsive layout, high-contrast visual cues for desk statuses, and intuitive error banners.",
        body_style
    ))

    story.append(Paragraph("2.4 System Architecture / Application Flow", h2_style))
    story.append(Paragraph("The system architecture and component interaction workflow are illustrated in Figure 2.1.", body_style))
    add_fig("parikshavinyas_architecture.png", "Figure 2.1: ParikshaVinyas System Architecture and Workflow Flowchart", width=420, height=380)

    story.append(PageBreak())

    # ============================================================
    # CHAPTER 3: TESTING METHODOLOGY
    # ============================================================
    story.append(Paragraph("Chapter 3", ParagraphStyle("ChPre3", parent=h1_style, fontSize=13, spaceAfter=2)))
    story.append(Paragraph("SOFTWARE TESTING METHODOLOGY", h1_style))
    story.append(Spacer(1, 4 * mm))

    story.append(Paragraph("3.1 Testing Process", h2_style))
    story.append(Paragraph("Testing followed a structured 8-phase STQA lifecycle (Table 3.1).", body_style))

    wf_data = [
        [Paragraph("<b>Phase</b>", table_header), Paragraph("<b>Activity</b>", table_header), Paragraph("<b>Description</b>", table_header)],
        [Paragraph("1", table_cell_bold), Paragraph("Requirement Analysis", table_cell_bold), Paragraph("Analyzed functional specifications, constraints, and database uniqueness rules.", table_cell)],
        [Paragraph("2", table_cell_bold), Paragraph("Test Planning", table_cell_bold), Paragraph("Formulated manual and automated testing scopes, tools, and pass criteria.", table_cell)],
        [Paragraph("3", table_cell_bold), Paragraph("Test Case Design", table_cell_bold), Paragraph("Designed black-box test scenarios using BVA, EP, and Decision Tables.", table_cell)],
        [Paragraph("4", table_cell_bold), Paragraph("Environment Setup", table_cell_bold), Paragraph("Configured Python virtual environment, Chromium browser, and test seeds.", table_cell)],
        [Paragraph("5", table_cell_bold), Paragraph("Test Execution", table_cell_bold), Paragraph("Executed 39 manual test cases and 46 automated Playwright/pytest scripts.", table_cell)],
        [Paragraph("6", table_cell_bold), Paragraph("Defect Reporting", table_cell_bold), Paragraph("Logged defects with severity, priority, reproduction steps, and root causes.", table_cell)],
        [Paragraph("7", table_cell_bold), Paragraph("Regression Testing", table_cell_bold), Paragraph("Verified bug fixes through targeted regression tests and E2E re-execution.", table_cell)],
        [Paragraph("8", table_cell_bold), Paragraph("Test Closure", table_cell_bold), Paragraph("Evaluated quality metrics, calculated pass percentages, and finalized report.", table_cell)]
    ]
    t_wf = Table(wf_data, colWidths=[40, 120, 310])
    t_wf.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1C4E79")),
        ("ALIGN", (0, 0), (-1, 0), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CCCCCC")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8F9FA")]),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    story.append(t_wf)
    story.append(Spacer(1, 4 * mm))

    story.append(Paragraph("3.2 Types of Testing Used", h2_style))
    story.append(Paragraph("Multiple software testing types were applied to ensure comprehensive coverage (Table 3.2).", body_style))

    type_data = [
        [Paragraph("<b>Sr.</b>", table_header), Paragraph("<b>Testing Type</b>", table_header), Paragraph("<b>Application to ParikshaVinyas</b>", table_header)],
        [Paragraph("1", table_cell_bold), Paragraph("Unit Testing", table_cell_bold), Paragraph("Tested isolated algorithmic functions (capacity check, seat coordinate calculation).", table_cell)],
        [Paragraph("2", table_cell_bold), Paragraph("Functional Testing", table_cell_bold), Paragraph("Verified form submissions, CRUD operations, and core seating allotment.", table_cell)],
        [Paragraph("3", table_cell_bold), Paragraph("Integration Testing", table_cell_bold), Paragraph("Evaluated interactions between Flask routes, SQLAlchemy models, and SQLite.", table_cell)],
        [Paragraph("4", table_cell_bold), Paragraph("System Testing", table_cell_bold), Paragraph("Executed complete end-to-end user workflows from login to PDF download.", table_cell)],
        [Paragraph("5", table_cell_bold), Paragraph("Boundary Value Analysis", table_cell_bold), Paragraph("Tested semester range limits [1, 8] and hall capacity limits [N-1, N, N+1].", table_cell)],
        [Paragraph("6", table_cell_bold), Paragraph("Equivalence Partitioning", table_cell_bold), Paragraph("Tested valid/invalid classes for email syntax, passwords, and timetable slots.", table_cell)],
        [Paragraph("7", table_cell_bold), Paragraph("Decision Table Testing", table_cell_bold), Paragraph("Modeled complex scheduling collision conditions and allocation regeneration guards.", table_cell)],
        [Paragraph("8", table_cell_bold), Paragraph("Usability Testing", table_cell_bold), Paragraph("Verified responsive visual grid rendering, mobile navigation, and colour coding.", table_cell)],
        [Paragraph("9", table_cell_bold), Paragraph("Security Testing", table_cell_bold), Paragraph("Audited RBAC boundaries, CSRF token validation, and URL redirection sanitization.", table_cell)]
    ]
    t_type = Table(type_data, colWidths=[30, 130, 310])
    t_type.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1C4E79")),
        ("ALIGN", (0, 0), (-1, 0), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CCCCCC")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8F9FA")]),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    story.append(t_type)

    story.append(PageBreak())

    # ============================================================
    # CHAPTER 4: MANUAL TESTING
    # ============================================================
    story.append(Paragraph("Chapter 4", ParagraphStyle("ChPre4", parent=h1_style, fontSize=13, spaceAfter=2)))
    story.append(Paragraph("MANUAL TESTING", h1_style))
    story.append(Spacer(1, 4 * mm))

    story.append(Paragraph("4.1 Test Case Design", h2_style))
    story.append(Paragraph("Table 4.1 documents the 39 manual test cases executed for ParikshaVinyas.", body_style))

    tc_data = [
        [Paragraph("<b>Test ID</b>", table_header), Paragraph("<b>Module</b>", table_header), Paragraph("<b>Scenario</b>", table_header), Paragraph("<b>Expected Result</b>", table_header), Paragraph("<b>Status</b>", table_header)],
        [Paragraph("TC-01", table_cell_bold), Paragraph("Auth", table_cell), Paragraph("Admin login valid credentials", table_cell), Paragraph("Redirects to admin dashboard", table_cell), Paragraph("<b>Pass</b>", table_cell_bold)],
        [Paragraph("TC-02", table_cell_bold), Paragraph("Auth", table_cell), Paragraph("Student login via enrollment", table_cell), Paragraph("Redirects to student portal", table_cell), Paragraph("<b>Pass</b>", table_cell_bold)],
        [Paragraph("TC-03", table_cell_bold), Paragraph("Auth", table_cell), Paragraph("Invigilator login", table_cell), Paragraph("Redirects to assigned duties", table_cell), Paragraph("<b>Pass</b>", table_cell_bold)],
        [Paragraph("TC-04", table_cell_bold), Paragraph("Students", table_cell), Paragraph("Register student valid fields", table_cell), Paragraph("Candidate added to directory", table_cell), Paragraph("<b>Pass</b>", table_cell_bold)],
        [Paragraph("TC-05", table_cell_bold), Paragraph("Students", table_cell), Paragraph("Search candidates by enrollment", table_cell), Paragraph("Filters matching candidate records", table_cell), Paragraph("<b>Pass</b>", table_cell_bold)],
        [Paragraph("TC-06", table_cell_bold), Paragraph("Students", table_cell), Paragraph("Filter by Course and Semester", table_cell), Paragraph("Returns only matching students", table_cell), Paragraph("<b>Pass</b>", table_cell_bold)],
        [Paragraph("TC-07", table_cell_bold), Paragraph("Halls", table_cell), Paragraph("Create hall rows/cols", table_cell), Paragraph("Capacity computed accurately", table_cell), Paragraph("<b>Pass</b>", table_cell_bold)],
        [Paragraph("TC-08", table_cell_bold), Paragraph("Halls", table_cell), Paragraph("Toggle seat blocking state", table_cell), Paragraph("Usable capacity decreases by 1", table_cell), Paragraph("<b>Pass</b>", table_cell_bold)],
        [Paragraph("TC-09", table_cell_bold), Paragraph("Scheduling", table_cell), Paragraph("Schedule exam future date", table_cell), Paragraph("Exam created in scheduled state", table_cell), Paragraph("<b>Pass</b>", table_cell_bold)],
        [Paragraph("TC-10", table_cell_bold), Paragraph("Allocation", table_cell), Paragraph("Sequential allocation surplus", table_cell), Paragraph("All students assigned desks", table_cell), Paragraph("<b>Pass</b>", table_cell_bold)],
        [Paragraph("TC-11", table_cell_bold), Paragraph("Allocation", table_cell), Paragraph("Seeded random allocation", table_cell), Paragraph("Reproducible desk allotment", table_cell), Paragraph("<b>Pass</b>", table_cell_bold)],
        [Paragraph("TC-12", table_cell_bold), Paragraph("Allocation", table_cell), Paragraph("Mixed course checkerboard", table_cell), Paragraph("Adjacent seats alternate course", table_cell), Paragraph("<b>Pass</b>", table_cell_bold)],
        [Paragraph("TC-13", table_cell_bold), Paragraph("Allocation", table_cell), Paragraph("Manual seat assignment to desk", table_cell), Paragraph("Candidate assigned; logged", table_cell), Paragraph("<b>Pass</b>", table_cell_bold)],
        [Paragraph("TC-14", table_cell_bold), Paragraph("Allocation", table_cell), Paragraph("Bilateral manual seat swap", table_cell), Paragraph("Desks exchanged without conflict", table_cell), Paragraph("<b>Pass</b>", table_cell_bold)],
        [Paragraph("TC-15", table_cell_bold), Paragraph("Reports", table_cell), Paragraph("Generate binary ReportLab PDF", table_cell), Paragraph("Valid PDF stream generated", table_cell), Paragraph("<b>Pass</b>", table_cell_bold)],
        [Paragraph("TC-16", table_cell_bold), Paragraph("Auth", table_cell), Paragraph("Login with incorrect password", table_cell), Paragraph("Displays invalid credentials error", table_cell), Paragraph("<b>Pass</b>", table_cell_bold)],
        [Paragraph("TC-17", table_cell_bold), Paragraph("Security", table_cell), Paragraph("Student accesses admin route", table_cell), Paragraph("HTTP 403 Forbidden returned", table_cell), Paragraph("<b>Pass</b>", table_cell_bold)],
        [Paragraph("TC-18", table_cell_bold), Paragraph("Students", table_cell), Paragraph("Reject duplicate enrollment", table_cell), Paragraph("Displays duplicate enrollment error", table_cell), Paragraph("<b>Pass</b>", table_cell_bold)],
        [Paragraph("TC-19", table_cell_bold), Paragraph("Students", table_cell), Paragraph("Semester below minimum (0)", table_cell), Paragraph("Rejected: Semester must be >= 1", table_cell), Paragraph("<b>Pass</b>", table_cell_bold)],
        [Paragraph("TC-20", table_cell_bold), Paragraph("Students", table_cell), Paragraph("Semester above maximum (9)", table_cell), Paragraph("Rejected: Semester must be <= 8", table_cell), Paragraph("<b>Pass</b>", table_cell_bold)],
        [Paragraph("TC-21", table_cell_bold), Paragraph("Students", table_cell), Paragraph("Malformed email address", table_cell), Paragraph("HTML5/Backend email error", table_cell), Paragraph("<b>Pass</b>", table_cell_bold)],
        [Paragraph("TC-22", table_cell_bold), Paragraph("Halls", table_cell), Paragraph("Non-positive hall dimensions", table_cell), Paragraph("Rejected: Rows and cols >= 1", table_cell), Paragraph("<b>Pass</b>", table_cell_bold)],
        [Paragraph("TC-23", table_cell_bold), Paragraph("Halls", table_cell), Paragraph("Block an occupied desk", table_cell), Paragraph("Blocked: Seat currently occupied", table_cell), Paragraph("<b>Pass</b>", table_cell_bold)],
        [Paragraph("TC-24", table_cell_bold), Paragraph("Scheduling", table_cell), Paragraph("End time earlier than start time", table_cell), Paragraph("Rejected: End time > start time", table_cell), Paragraph("<b>Pass</b>", table_cell_bold)],
        [Paragraph("TC-25", table_cell_bold), Paragraph("Scheduling", table_cell), Paragraph("Overlapping exam schedule", table_cell), Paragraph("Conflict warning displayed", table_cell), Paragraph("<b>Pass</b>", table_cell_bold)],
        [Paragraph("TC-26", table_cell_bold), Paragraph("Allocation", table_cell), Paragraph("Students exceed capacity (N+1)", table_cell), Paragraph("Atomic rollback; error displayed", table_cell), Paragraph("<b>Pass</b>", table_cell_bold)],
        [Paragraph("TC-27", table_cell_bold), Paragraph("Allocation", table_cell), Paragraph("Skip damaged/blocked desks", table_cell), Paragraph("Damaged desks skipped in grid", table_cell), Paragraph("<b>Pass</b>", table_cell_bold)],
        [Paragraph("TC-28", table_cell_bold), Paragraph("Allocation", table_cell), Paragraph("Allocate ineligible student", table_cell), Paragraph("Rejected: Candidate not enrolled", table_cell), Paragraph("<b>Pass</b>", table_cell_bold)],
        [Paragraph("TC-29", table_cell_bold), Paragraph("Allocation", table_cell), Paragraph("Duplicate seat assignment", table_cell), Paragraph("Prevented by unique constraint", table_cell), Paragraph("<b>Pass</b>", table_cell_bold)],
        [Paragraph("TC-30", table_cell_bold), Paragraph("Security", table_cell), Paragraph("CSRF token omitted from form", table_cell), Paragraph("HTTP 400 Bad Request returned", table_cell), Paragraph("<b>Pass</b>", table_cell_bold)],
        [Paragraph("TC-31", table_cell_bold), Paragraph("Scheduling", table_cell), Paragraph("Timetable collision on edit", table_cell), Paragraph("Warning displayed; update blocked", table_cell), Paragraph("<b>Pass</b>", table_cell_bold)],
        [Paragraph("TC-32", table_cell_bold), Paragraph("Students", table_cell), Paragraph("In-batch duplicate CSV rows", table_cell), Paragraph("Valid committed; duplicates logged", table_cell), Paragraph("<b>Pass</b>", table_cell_bold)],
        [Paragraph("TC-33", table_cell_bold), Paragraph("Halls", table_cell), Paragraph("Resize hall below active seats", table_cell), Paragraph("Collision warning; resize blocked", table_cell), Paragraph("<b>Pass</b>", table_cell_bold)],
        [Paragraph("TC-34", table_cell_bold), Paragraph("Academic", table_cell), Paragraph("Delete course with linked exams", table_cell), Paragraph("Referential guard prevents delete", table_cell), Paragraph("<b>Pass</b>", table_cell_bold)],
        [Paragraph("TC-35", table_cell_bold), Paragraph("Allocation", table_cell), Paragraph("Shortage during force re-alloc", table_cell), Paragraph("Prior allocations preserved", table_cell), Paragraph("<b>Pass</b>", table_cell_bold)],
        [Paragraph("TC-36", table_cell_bold), Paragraph("Allocation", table_cell), Paragraph("Manual seat choice on POST", table_cell), Paragraph("Choice accepted without error", table_cell), Paragraph("<b>Pass</b>", table_cell_bold)],
        [Paragraph("TC-37", table_cell_bold), Paragraph("Invigilator", table_cell), Paragraph("IDOR access to unassigned hall", table_cell), Paragraph("HTTP 403 Forbidden returned", table_cell), Paragraph("<b>Pass</b>", table_cell_bold)],
        [Paragraph("TC-38", table_cell_bold), Paragraph("Security", table_cell), Paragraph("Open redirect via next query", table_cell), Paragraph("Sanitized to local dashboard", table_cell), Paragraph("<b>Pass</b>", table_cell_bold)],
        [Paragraph("TC-39", table_cell_bold), Paragraph("Dashboard", table_cell), Paragraph("Calculate usable capacity", table_cell), Paragraph("Sums usable seats of active halls", table_cell), Paragraph("<b>Pass</b>", table_cell_bold)]
    ]
    t_tc = Table(tc_data, colWidths=[45, 60, 160, 160, 45])
    t_tc.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1C4E79")),
        ("ALIGN", (0, 0), (-1, 0), "CENTER"),
        ("ALIGN", (4, 1), (4, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CCCCCC")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8F9FA")]),
        ("TOPPADDING", (0, 0), (-1, -1), 1.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1.5),
    ]))
    story.append(t_tc)
    story.append(Spacer(1, 4 * mm))

    story.append(Paragraph("4.1.1 Test Case Execution Summary", h3_style))
    story.append(Paragraph("All 39 manual test cases passed successfully (100% pass rate) as summarized in Table 4.2.", body_style))

    sum_data = [
        [Paragraph("<b>Category</b>", table_header), Paragraph("<b>Total Cases</b>", table_header), Paragraph("<b>Passed</b>", table_header), Paragraph("<b>Failed</b>", table_header), Paragraph("<b>Pass Rate</b>", table_header)],
        [Paragraph("Positive Functional Scenarios", table_cell), Paragraph("15", table_cell_bold), Paragraph("15", table_cell_bold), Paragraph("0", table_cell), Paragraph("100%", table_cell_bold)],
        [Paragraph("Negative / Validation Scenarios", table_cell), Paragraph("15", table_cell_bold), Paragraph("15", table_cell_bold), Paragraph("0", table_cell), Paragraph("100%", table_cell_bold)],
        [Paragraph("Defect Regression Scenarios", table_cell), Paragraph("9", table_cell_bold), Paragraph("9", table_cell_bold), Paragraph("0", table_cell), Paragraph("100%", table_cell_bold)],
        [Paragraph("<b>Total</b>", table_cell_bold), Paragraph("<b>39</b>", table_cell_bold), Paragraph("<b>39</b>", table_cell_bold), Paragraph("<b>0</b>", table_cell_bold), Paragraph("<b>100%</b>", table_cell_bold)]
    ]
    t_sum = Table(sum_data, colWidths=[150, 70, 70, 70, 110])
    t_sum.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1C4E79")),
        ("ALIGN", (1, 0), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CCCCCC")),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    story.append(t_sum)
    story.append(Spacer(1, 4 * mm))

    story.append(Paragraph("4.2 Test Case Techniques", h2_style))
    story.append(Paragraph("4.2.1 Equivalence Partitioning", h3_style))
    story.append(Paragraph("Equivalence Partitioning was applied to input domains as detailed in Table 4.3.", body_style))

    ep_data = [
        [Paragraph("<b>Input Field</b>", table_header), Paragraph("<b>Valid Equivalence Class</b>", table_header), Paragraph("<b>Invalid Equivalence Class</b>", table_header)],
        [Paragraph("Enrollment Number", table_cell_bold), Paragraph("Alphanumeric string (e.g., EN2026101)", table_cell), Paragraph("Empty string, existing duplicate enrollment", table_cell)],
        [Paragraph("Email Address", table_cell_bold), Paragraph("Standard format (user@srict.ac.in)", table_cell), Paragraph("String lacking @ or domain (invalid_email)", table_cell)],
        [Paragraph("Password", table_cell_bold), Paragraph("Minimum 8 chars with symbols", table_cell), Paragraph("Empty string, incorrect password credentials", table_cell)],
        [Paragraph("Exam Timetable", table_cell_bold), Paragraph("Start Time < End Time (10:00 - 13:00)", table_cell), Paragraph("Start Time >= End Time (14:00 - 11:00)", table_cell)],
        [Paragraph("Hall Dimensions", table_cell_bold), Paragraph("Positive integers (Rows >= 1, Cols >= 1)", table_cell), Paragraph("Zero or negative integers (Rows=0, Cols=-2)", table_cell)]
    ]
    t_ep = Table(ep_data, colWidths=[100, 180, 190])
    t_ep.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1C4E79")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CCCCCC")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8F9FA")]),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    story.append(t_ep)
    story.append(Spacer(1, 4 * mm))

    story.append(Paragraph("4.2.2 Boundary Value Analysis", h3_style))
    story.append(Paragraph("Boundary Value Analysis evaluated critical numerical limits (Table 4.4).", body_style))

    bva_data = [
        [Paragraph("<b>Parameter</b>", table_header), Paragraph("<b>Boundary Values</b>", table_header), Paragraph("<b>Test Inputs</b>", table_header), Paragraph("<b>Observed Behavior</b>", table_header)],
        [Paragraph("Semester", table_cell_bold), Paragraph("Min=1, Max=8", table_cell), Paragraph("0, 1, 8, 9", table_cell), Paragraph("0 and 9 rejected; 1 and 8 accepted", table_cell)],
        [Paragraph("Hall Capacity", table_cell_bold), Paragraph("N = Usable Seats", table_cell), Paragraph("N-1, N, N+1", table_cell), Paragraph("N-1, N allocate; N+1 rolls back cleanly", table_cell)],
        [Paragraph("Hall Dimensions", table_cell_bold), Paragraph("Min=1", table_cell), Paragraph("0, 1", table_cell), Paragraph("0 rejected; 1 accepted", table_cell)]
    ]
    t_bva = Table(bva_data, colWidths=[90, 110, 90, 180])
    t_bva.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1C4E79")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CCCCCC")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8F9FA")]),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    story.append(t_bva)
    story.append(Spacer(1, 4 * mm))

    story.append(Paragraph("4.2.3 Decision Table Testing", h3_style))
    story.append(Paragraph("Decision Tables modeled complex exam scheduling collisions (Table 4.5).", body_style))

    dt_data = [
        [Paragraph("<b>Conditions</b>", table_header), Paragraph("<b>Rule 1</b>", table_header), Paragraph("<b>Rule 2</b>", table_header), Paragraph("<b>Rule 3</b>", table_header), Paragraph("<b>Rule 4</b>", table_header)],
        [Paragraph("Same Date as Existing Exam?", table_cell_bold), Paragraph("Yes", table_cell), Paragraph("Yes", table_cell), Paragraph("Yes", table_cell), Paragraph("No", table_cell)],
        [Paragraph("Same Course & Semester?", table_cell_bold), Paragraph("Yes", table_cell), Paragraph("Yes", table_cell), Paragraph("No", table_cell), Paragraph("Yes", table_cell)],
        [Paragraph("Time Slot Overlaps?", table_cell_bold), Paragraph("Yes", table_cell), Paragraph("No", table_cell), Paragraph("Yes", table_cell), Paragraph("Yes", table_cell)],
        [Paragraph("<b>Collision Warning Triggered?</b>", table_cell_bold), Paragraph("<b>Yes</b>", table_cell_bold), Paragraph("No", table_cell), Paragraph("No", table_cell), Paragraph("No", table_cell)],
        [Paragraph("<b>Exam Persisted in Database?</b>", table_cell_bold), Paragraph("<b>No</b>", table_cell_bold), Paragraph("<b>Yes</b>", table_cell_bold), Paragraph("<b>Yes</b>", table_cell_bold), Paragraph("<b>Yes</b>", table_cell_bold)]
    ]
    t_dt = Table(dt_data, colWidths=[170, 75, 75, 75, 75])
    t_dt.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1C4E79")),
        ("ALIGN", (1, 0), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CCCCCC")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8F9FA")]),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    story.append(t_dt)

    story.append(PageBreak())

    # ============================================================
    # CHAPTER 5: AUTOMATION TESTING
    # ============================================================
    story.append(Paragraph("Chapter 5", ParagraphStyle("ChPre5", parent=h1_style, fontSize=13, spaceAfter=2)))
    story.append(Paragraph("AUTOMATION TESTING", h1_style))
    story.append(Spacer(1, 4 * mm))

    story.append(Paragraph("5.1 Automation Tool", h2_style))
    story.append(Paragraph(
        "Automated testing was conducted using Python <b>Playwright</b> with the <b>pytest</b> test runner. Playwright was selected "
        "due to its reliable execution in headless Chromium, automatic actionability checks, network request inspection, and "
        "accurate DOM element selectors.",
        body_style
    ))

    story.append(Paragraph("5.2 Automation Environment", h2_style))
    story.append(Paragraph("The automation environment specifications are listed in Table 5.1.", body_style))

    env_data = [
        [Paragraph("<b>Component</b>", table_header), Paragraph("<b>Specification</b>", table_header)],
        [Paragraph("Operating System", table_cell_bold), Paragraph("Microsoft Windows 11 Enterprise (64-bit)", table_cell)],
        [Paragraph("Programming Language", table_cell_bold), Paragraph("Python 3.11.9", table_cell)],
        [Paragraph("Automation Framework", table_cell_bold), Paragraph("Playwright 1.48.0", table_cell)],
        [Paragraph("Test Runner", table_cell_bold), Paragraph("pytest 8.3.3", table_cell)],
        [Paragraph("Browser Engine", table_cell_bold), Paragraph("Chromium 130.0.6723.58", table_cell)],
        [Paragraph("Integrated Development Env", table_cell_bold), Paragraph("Visual Studio Code 1.95", table_cell)],
        [Paragraph("Application Server", table_cell_bold), Paragraph("Flask Development WSGI Server (Port 5000)", table_cell)]
    ]
    t_env = Table(env_data, colWidths=[160, 310])
    t_env.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1C4E79")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CCCCCC")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8F9FA")]),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    story.append(t_env)
    story.append(Spacer(1, 4 * mm))

    story.append(Paragraph("5.3 Automated Test Cases", h2_style))
    story.append(Paragraph(
        "Five representative automated test cases (AT-01 to AT-05) were executed and verified, documenting form input, "
        "system response, and terminal results.",
        body_style
    ))

    # AT-01
    story.append(Paragraph("5.3.1 AT-01: Submit Registration Form with Empty Fields", h3_style))
    story.append(Paragraph("<b>Script:</b> `tests/test_e2e_playwright.py::test_student_validation_empty_fields`<br/>"
                           "<b>Expected:</b> Required field tooltip displayed; submission blocked.<br/>"
                           "<b>Actual:</b> Submission blocked; HTML5 validation tooltip displayed.<br/>"
                           "<b>Status:</b> Passed (1.42s)", body_style))
    add_fig("fig5_01_at01_form.png", "Figure 5.1: AT-01: Registration Form with Empty Fields", width=380, height=170)
    add_fig("fig5_02_at01_validation.png", "Figure 5.2: AT-01: Required-Field Validation Alert", width=380, height=170)
    add_fig("fig5_03_at01_terminal.png", "Figure 5.3: AT-01: Automated Test Result in Terminal", width=380, height=95)

    # AT-02
    story.append(Paragraph("5.3.2 AT-02: Prevent Duplicate Student Enrollment Number", h3_style))
    story.append(Paragraph("<b>Script:</b> `tests/test_e2e_playwright.py::test_duplicate_student_rejection`<br/>"
                           "<b>Expected:</b> System rejects duplicate enrollment with flash error.<br/>"
                           "<b>Actual:</b> Flash error banner displayed; no duplicate saved.<br/>"
                           "<b>Status:</b> Passed (1.68s)", body_style))
    add_fig("fig5_04_at02_form.png", "Figure 5.4: AT-02: Registration with Existing Enrollment", width=380, height=170)
    add_fig("fig5_05_at02_validation.png", "Figure 5.5: AT-02: Duplicate Enrollment Validation Warning", width=380, height=170)
    add_fig("fig5_06_at02_terminal.png", "Figure 5.6: AT-02: Automated Test Result in Terminal", width=380, height=95)

    # AT-03
    story.append(Paragraph("5.3.3 AT-03: Examination Timetable Overlapping Conflict Detection", h3_style))
    story.append(Paragraph("<b>Script:</b> `tests/test_e2e_playwright.py::test_exam_scheduling_conflict`<br/>"
                           "<b>Expected:</b> System detects temporal interval collision and blocks exam creation.<br/>"
                           "<b>Actual:</b> Timetable collision warning shown; exam rejected.<br/>"
                           "<b>Status:</b> Passed (2.11s)", body_style))
    add_fig("fig5_07_at03_form.png", "Figure 5.7: AT-03: Overlapping Examination Timetable Form", width=380, height=170)
    add_fig("fig5_08_at03_validation.png", "Figure 5.8: AT-03: Timetable Collision Rejection Notification", width=380, height=170)
    add_fig("fig5_09_at03_terminal.png", "Figure 5.9: AT-03: Automated Test Result in Terminal", width=380, height=95)

    # AT-04
    story.append(Paragraph("5.3.4 AT-04: Role-Based Access Control Defense", h3_style))
    story.append(Paragraph("<b>Script:</b> `tests/test_e2e_playwright.py::test_rbac_unauthorized_access`<br/>"
                           "<b>Expected:</b> Access blocked; HTTP 403 Forbidden rendered.<br/>"
                           "<b>Actual:</b> HTTP 403 returned; administrative layout protected.<br/>"
                           "<b>Status:</b> Passed (1.35s)", body_style))
    add_fig("fig5_10_at04_form.png", "Figure 5.10: AT-04: Authenticated Student Portal Session", width=380, height=170)
    add_fig("fig5_11_at04_validation.png", "Figure 5.11: AT-04: HTTP 403 Forbidden Access Control Response", width=380, height=170)
    add_fig("fig5_12_at04_terminal.png", "Figure 5.12: AT-04: Automated Test Result in Terminal", width=380, height=95)

    # AT-05
    story.append(Paragraph("5.3.5 AT-05: Capacity Shortage Atomic Rollback during Seat Allocation", h3_style))
    story.append(Paragraph("<b>Script:</b> `tests/test_e2e_playwright.py::test_allocation_capacity_overflow`<br/>"
                           "<b>Expected:</b> Insufficient capacity aborts; 0 partial records committed.<br/>"
                           "<b>Actual:</b> Shortage alert displayed; database rolled back cleanly.<br/>"
                           "<b>Status:</b> Passed (2.84s)", body_style))
    add_fig("fig5_13_at05_form.png", "Figure 5.13: AT-05: Allocation Form with Capacity Overflow Condition", width=380, height=170)
    add_fig("fig5_14_at05_validation.png", "Figure 5.14: AT-05: Insufficient Capacity Warning and Atomic Rollback", width=380, height=170)
    add_fig("fig5_15_at05_terminal.png", "Figure 5.15: AT-05: Automated Test Result in Terminal", width=380, height=95)

    story.append(Spacer(1, 4 * mm))
    story.append(Paragraph("5.3.6 Automation Test Summary", h3_style))
    story.append(Paragraph("Table 5.7 summarizes the executed automated test cases.", body_style))

    at_sum_data = [
        [Paragraph("<b>Test ID</b>", table_header), Paragraph("<b>Test Scenario</b>", table_header), Paragraph("<b>Execution Time</b>", table_header), Paragraph("<b>Status</b>", table_header)],
        [Paragraph("AT-01", table_cell_bold), Paragraph("Student Registration with Empty Fields", table_cell), Paragraph("1.42s", table_cell), Paragraph("<b>Passed</b>", table_cell_bold)],
        [Paragraph("AT-02", table_cell_bold), Paragraph("Duplicate Student Enrollment Number", table_cell), Paragraph("1.68s", table_cell), Paragraph("<b>Passed</b>", table_cell_bold)],
        [Paragraph("AT-03", table_cell_bold), Paragraph("Examination Timetable Conflict", table_cell), Paragraph("2.11s", table_cell), Paragraph("<b>Passed</b>", table_cell_bold)],
        [Paragraph("AT-04", table_cell_bold), Paragraph("Role-Based Access Control Defense", table_cell), Paragraph("1.35s", table_cell), Paragraph("<b>Passed</b>", table_cell_bold)],
        [Paragraph("AT-05", table_cell_bold), Paragraph("Capacity Shortage Atomic Rollback", table_cell), Paragraph("2.84s", table_cell), Paragraph("<b>Passed</b>", table_cell_bold)]
    ]
    t_atsum = Table(at_sum_data, colWidths=[60, 240, 100, 70])
    t_atsum.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1C4E79")),
        ("ALIGN", (2, 0), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CCCCCC")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8F9FA")]),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    story.append(t_atsum)

    story.append(PageBreak())

    # ============================================================
    # CHAPTER 6: AI-BASED TESTING
    # ============================================================
    story.append(Paragraph("Chapter 6", ParagraphStyle("ChPre6", parent=h1_style, fontSize=13, spaceAfter=2)))
    story.append(Paragraph("AI-BASED TESTING", h1_style))
    story.append(Spacer(1, 4 * mm))

    story.append(Paragraph("6.1 Introduction to AI in Software Testing", h2_style))
    story.append(Paragraph(
        "Artificial Intelligence (AI) and Large Language Models (LLMs) significantly enhance software quality assurance. "
        "In this project, AI was utilized to analyze code complexity, uncover non-obvious allocation edge cases, derive decision "
        "tables, and evaluate transaction boundary risks.",
        body_style
    ))

    story.append(Paragraph("6.2 AI Tools Used", h2_style))
    story.append(Paragraph(
        "Three modern AI tools were employed: <b>Google Gemini</b> for boundary discovery (Figure 6.1), "
        "<b>Claude</b> for code invariant inspection (Figure 6.2), and <b>Google NotebookLM</b> for defect synthesis (Figure 6.3).",
        body_style
    ))
    add_fig("fig6_01_gemini.jpg", "Figure 6.1: Google Gemini: AI-Assisted Test Case Generation", width=380, height=190)
    add_fig("fig6_02_claude.jpg", "Figure 6.2: Claude: Review of Test Scenarios and Invariant Logic", width=380, height=190)
    add_fig("fig6_03_notebooklm.jpg", "Figure 6.3: Google NotebookLM: Risk and Defect Correlation Analysis", width=380, height=190)

    story.append(Paragraph("6.3 AI-Assisted Test Cases and Results", h2_style))
    story.append(Paragraph(
        "Five AI-derived scenarios (AI-01 to AI-05) were formulated and evaluated:",
        body_style
    ))

    # AI-01
    story.append(Paragraph("6.3.1 AI-01: Checkerboard Seat Allocation Alternation", h3_style))
    story.append(Paragraph("Verified that mixed-course allocation alternates candidates of different courses consecutively across rows (Figures 6.4 and 6.5).", body_style))
    add_fig("fig6_04_ai01_inapp.png", "Figure 6.4: AI-01: In-App AI QA Workspace and Test Case Generation", width=380, height=170)
    add_fig("fig6_05_ai01_result.png", "Figure 6.5: AI-01: Checkerboard Seat Allocation Verification in Grid", width=380, height=170)

    # AI-02
    story.append(Paragraph("6.3.2 AI-02: Damaged Desk Exclusion in Visual Layout", h3_style))
    story.append(Paragraph("Confirmed that damaged desks marked as blocked are strictly bypassed during automated seat distribution (Figure 6.6).", body_style))
    add_fig("fig6_06_ai02_damaged_desk.png", "Figure 6.6: AI-02: Damaged Desk Exclusion in Visual Layout Grid", width=380, height=170)

    # AI-03
    story.append(Paragraph("6.3.3 AI-03: Multi-Column Student Directory Filter Integrity", h3_style))
    story.append(Paragraph("Validated that combining enrollment substring, course, and semester filters returns exact mathematical subsets (Figure 6.7).", body_style))
    add_fig("fig6_07_ai03_filter.png", "Figure 6.7: AI-03: Multi-Column Search and Directory Filtering", width=380, height=170)

    # AI-04
    story.append(Paragraph("6.3.4 AI-04: ReportLab PDF Header Rendering on Multi-Page Seating Charts", h3_style))
    story.append(Paragraph("Evaluated binary PDF streaming across multi-page seating charts, confirming header alignment on every page (Figures 6.8 and 6.9).", body_style))
    add_fig("fig6_08_ai04_pdf.png", "Figure 6.8: AI-04: Reports Management Center for PDF Seating Slips", width=380, height=170)
    add_fig("fig6_09_ai04_pdf_view.png", "Figure 6.9: AI-04: Multi-Hall PDF Seating Arrangement Preview", width=380, height=170)

    # AI-05
    story.append(Paragraph("6.3.5 AI-05: Invigilator Roster Authorization Boundary (IDOR Prevention)", h3_style))
    story.append(Paragraph("Tested whether invigilators could access rosters of unassigned examinations, verifying strict HTTP 403 enforcement (Figure 6.10).", body_style))
    add_fig("fig6_10_ai05_idor.png", "Figure 6.10: AI-05: IDOR Prevention Response on Unauthorized Roster Export", width=380, height=170)

    story.append(PageBreak())

    # ============================================================
    # CHAPTER 7: DEFECT REPORTING
    # ============================================================
    story.append(Paragraph("Chapter 7", ParagraphStyle("ChPre7", parent=h1_style, fontSize=13, spaceAfter=2)))
    story.append(Paragraph("DEFECT/BUG REPORTING", h1_style))
    story.append(Spacer(1, 4 * mm))

    story.append(Paragraph("7.1 Introduction", h2_style))
    story.append(Paragraph(
        "Defect reporting documents application anomalies and deviations from functional specifications. "
        "Six major defects (BUG001 to BUG006) were identified, reproduced, remediated, and verified.",
        body_style
    ))

    # BUG001
    story.append(Paragraph("7.2.1 BUG001: Capacity Shortage Atomic Rollback Failure", h3_style))
    bug1_data = [
        [Paragraph("<b>Field</b>", table_header), Paragraph("<b>Details</b>", table_header)],
        [Paragraph("Bug ID", table_cell_bold), Paragraph("<b>BUG001</b>", table_cell_bold)],
        [Paragraph("Test Case ID", table_cell_bold), Paragraph("TC-26 / AT-05", table_cell)],
        [Paragraph("Description", table_cell_bold), Paragraph("When candidates exceeded hall capacity, the system aborted but left partial student records committed in database.", table_cell)],
        [Paragraph("Severity / Priority", table_cell_bold), Paragraph("<b>Critical / High</b>", table_cell_bold)],
        [Paragraph("Status", table_cell_bold), Paragraph("<b>Resolved & Verified</b>", table_cell_bold)],
        [Paragraph("Steps to Reproduce", table_cell_bold), Paragraph("1. Select exam with 41 students. 2. Choose hall with 40 seats. 3. Run allocation.", table_cell)],
        [Paragraph("Expected Result", table_cell_bold), Paragraph("System aborts; 0 records committed; error toast shown.", table_cell)],
        [Paragraph("Actual Result", table_cell_bold), Paragraph("40 students committed; 1 unallocated; partial state left in DB.", table_cell)],
        [Paragraph("Resolution", table_cell_bold), Paragraph("Added pre-allocation capacity check and explicit `db.session.rollback()` on error.", table_cell)]
    ]
    t_bug1 = Table(bug1_data, colWidths=[120, 350])
    t_bug1.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1C4E79")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CCCCCC")),
        ("TOPPADDING", (0, 0), (-1, -1), 1.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1.5),
    ]))
    story.append(t_bug1)
    add_fig("fig7_01_bug01.png", "Figure 7.1: BUG001: Verification of Atomic Rollback on Capacity Shortage", width=380, height=160)

    # BUG002
    story.append(Paragraph("7.2.2 BUG002: Timetable Interval Overlap Conflict", h3_style))
    bug2_data = [
        [Paragraph("<b>Field</b>", table_header), Paragraph("<b>Details</b>", table_header)],
        [Paragraph("Bug ID", table_cell_bold), Paragraph("<b>BUG002</b>", table_cell_bold)],
        [Paragraph("Test Case ID", table_cell_bold), Paragraph("TC-25 / AT-03", table_cell)],
        [Paragraph("Description", table_cell_bold), Paragraph("System allowed scheduling overlapping examinations for the same course and semester cohort.", table_cell)],
        [Paragraph("Severity / Priority", table_cell_bold), Paragraph("<b>High / High</b>", table_cell_bold)],
        [Paragraph("Status", table_cell_bold), Paragraph("<b>Resolved & Verified</b>", table_cell_bold)],
        [Paragraph("Resolution", table_cell_bold), Paragraph("Implemented temporal interval overlap query in the exam scheduling route.", table_cell)]
    ]
    t_bug2 = Table(bug2_data, colWidths=[120, 350])
    t_bug2.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1C4E79")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CCCCCC")),
        ("TOPPADDING", (0, 0), (-1, -1), 1.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1.5),
    ]))
    story.append(t_bug2)
    add_fig("fig7_02_bug02.png", "Figure 7.2: BUG002: Rejection of Overlapping Examination Timetable", width=380, height=160)

    # BUG003
    story.append(Paragraph("7.2.3 BUG003: In-Place Desk Blocking Permitted on Occupied Desks", h3_style))
    bug3_data = [
        [Paragraph("<b>Field</b>", table_header), Paragraph("<b>Details</b>", table_header)],
        [Paragraph("Bug ID", table_cell_bold), Paragraph("<b>BUG003</b>", table_cell_bold)],
        [Paragraph("Test Case ID", table_cell_bold), Paragraph("TC-23", table_cell)],
        [Paragraph("Description", table_cell_bold), Paragraph("Toggling seat to 'Blocked' was permitted even when a candidate was actively seated at that desk.", table_cell)],
        [Paragraph("Severity / Priority", table_cell_bold), Paragraph("<b>Medium / Medium</b>", table_cell_bold)],
        [Paragraph("Status", table_cell_bold), Paragraph("<b>Resolved & Verified</b>", table_cell_bold)],
        [Paragraph("Resolution", table_cell_bold), Paragraph("Added allocation lookup guard before toggling seat blocking state.", table_cell)]
    ]
    t_bug3 = Table(bug3_data, colWidths=[120, 350])
    t_bug3.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1C4E79")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CCCCCC")),
        ("TOPPADDING", (0, 0), (-1, -1), 1.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1.5),
    ]))
    story.append(t_bug3)
    add_fig("fig7_03_bug03.png", "Figure 7.3: BUG003: Guard Preventing Blocking of Occupied Desks", width=380, height=160)

    # BUG004
    story.append(Paragraph("7.2.4 BUG004: In-Batch Duplicate Enrollment Error Unhandled During CSV Import", h3_style))
    bug4_data = [
        [Paragraph("<b>Field</b>", table_header), Paragraph("<b>Details</b>", table_header)],
        [Paragraph("Bug ID", table_cell_bold), Paragraph("<b>BUG004</b>", table_cell_bold)],
        [Paragraph("Test Case ID", table_cell_bold), Paragraph("TC-32", table_cell)],
        [Paragraph("Description", table_cell_bold), Paragraph("Duplicate enrollments within the same CSV upload caused an unhandled 500 SQLite IntegrityError.", table_cell)],
        [Paragraph("Severity / Priority", table_cell_bold), Paragraph("<b>High / High</b>", table_cell_bold)],
        [Paragraph("Status", table_cell_bold), Paragraph("<b>Resolved & Verified</b>", table_cell_bold)],
        [Paragraph("Resolution", table_cell_bold), Paragraph("Added in-batch tracking set (`seen_enrollments`) and line-level error reporting.", table_cell)]
    ]
    t_bug4 = Table(bug4_data, colWidths=[120, 350])
    t_bug4.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1C4E79")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CCCCCC")),
        ("TOPPADDING", (0, 0), (-1, -1), 1.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1.5),
    ]))
    story.append(t_bug4)
    add_fig("fig7_04_bug04.png", "Figure 7.4: BUG004: Graceful Handling of In-Batch Duplicate Enrollment Numbers", width=380, height=160)

    # BUG005
    story.append(Paragraph("7.2.5 BUG005: Force Re-Allocation Clears Existing Seating Prior to Capacity Check", h3_style))
    bug5_data = [
        [Paragraph("<b>Field</b>", table_header), Paragraph("<b>Details</b>", table_header)],
        [Paragraph("Bug ID", table_cell_bold), Paragraph("<b>BUG005</b>", table_cell_bold)],
        [Paragraph("Test Case ID", table_cell_bold), Paragraph("TC-35", table_cell)],
        [Paragraph("Description", table_cell_bold), Paragraph("Force re-allocation cleared previous allocations before checking capacity, causing data loss on shortage.", table_cell)],
        [Paragraph("Severity / Priority", table_cell_bold), Paragraph("<b>Critical / High</b>", table_cell_bold)],
        [Paragraph("Status", table_cell_bold), Paragraph("<b>Resolved & Verified</b>", table_cell_bold)],
        [Paragraph("Resolution", table_cell_bold), Paragraph("Deferred clearing old allocations until capacity validation passes completely.", table_cell)]
    ]
    t_bug5 = Table(bug5_data, colWidths=[120, 350])
    t_bug5.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1C4E79")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CCCCCC")),
        ("TOPPADDING", (0, 0), (-1, -1), 1.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1.5),
    ]))
    story.append(t_bug5)
    add_fig("fig7_05_bug05.png", "Figure 7.5: BUG005: Allocation Preservation Guard During Capacity Shortage", width=380, height=160)

    # BUG006
    story.append(Paragraph("7.2.6 BUG006: Insecure Direct Object Reference (IDOR) on Invigilator Roster Export", h3_style))
    bug6_data = [
        [Paragraph("<b>Field</b>", table_header), Paragraph("<b>Details</b>", table_header)],
        [Paragraph("Bug ID", table_cell_bold), Paragraph("<b>BUG006</b>", table_cell_bold)],
        [Paragraph("Test Case ID", table_cell_bold), Paragraph("TC-37 / AI-05", table_cell)],
        [Paragraph("Description", table_cell_bold), Paragraph("Invigilators could download seating rosters of unassigned examinations by altering the URL ID parameter.", table_cell)],
        [Paragraph("Severity / Priority", table_cell_bold), Paragraph("<b>High / High</b>", table_cell_bold)],
        [Paragraph("Status", table_cell_bold), Paragraph("<b>Resolved & Verified</b>", table_cell_bold)],
        [Paragraph("Resolution", table_cell_bold), Paragraph("Enforced ownership check verifying invigilator assignment to the requested exam.", table_cell)]
    ]
    t_bug6 = Table(bug6_data, colWidths=[120, 350])
    t_bug6.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1C4E79")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CCCCCC")),
        ("TOPPADDING", (0, 0), (-1, -1), 1.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1.5),
    ]))
    story.append(t_bug6)
    add_fig("fig7_06_bug06.png", "Figure 7.6: BUG006: HTTP 403 Forbidden Response Blocking Unauthorized Roster Export", width=380, height=160)

    story.append(PageBreak())

    # ============================================================
    # CHAPTER 8: TEST RESULTS AND ANALYSIS
    # ============================================================
    story.append(Paragraph("Chapter 8", ParagraphStyle("ChPre8", parent=h1_style, fontSize=13, spaceAfter=2)))
    story.append(Paragraph("TEST RESULTS AND ANALYSIS", h1_style))
    story.append(Spacer(1, 4 * mm))

    story.append(Paragraph("8.1 Introduction", h2_style))
    story.append(Paragraph(
        "This chapter synthesizes the results obtained from manual testing, automated Playwright/pytest execution, "
        "and AI-assisted verification. The outcomes are evaluated using standardized STQA quality formulas.",
        body_style
    ))

    story.append(Paragraph("8.2 Test Execution Summary", h2_style))
    story.append(Paragraph("Table 8.1 presents the test execution metrics across all three testing approaches.", body_style))

    res_data = [
        [Paragraph("<b>Testing Approach</b>", table_header), Paragraph("<b>Total Cases</b>", table_header), Paragraph("<b>Passed</b>", table_header), Paragraph("<b>Failed</b>", table_header), Paragraph("<b>Pass Rate</b>", table_header)],
        [Paragraph("Manual Testing", table_cell_bold), Paragraph("39", table_cell), Paragraph("39", table_cell), Paragraph("0", table_cell), Paragraph("<b>100.00%</b>", table_cell_bold)],
        [Paragraph("Automation Testing", table_cell_bold), Paragraph("5", table_cell), Paragraph("5", table_cell), Paragraph("0", table_cell), Paragraph("<b>100.00%</b>", table_cell_bold)],
        [Paragraph("AI-Assisted Testing", table_cell_bold), Paragraph("5", table_cell), Paragraph("5", table_cell), Paragraph("0", table_cell), Paragraph("<b>100.00%</b>", table_cell_bold)],
        [Paragraph("<b>Total Composite</b>", table_cell_bold), Paragraph("<b>49</b>", table_cell_bold), Paragraph("<b>49</b>", table_cell_bold), Paragraph("<b>0</b>", table_cell_bold), Paragraph("<b>100.00%</b>", table_cell_bold)]
    ]
    t_res = Table(res_data, colWidths=[150, 75, 75, 75, 95])
    t_res.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1C4E79")),
        ("ALIGN", (1, 0), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CCCCCC")),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    story.append(t_res)
    story.append(Spacer(1, 4 * mm))

    story.append(Paragraph("8.3 Test Result Calculation", h2_style))
    story.append(Paragraph("The pass and fail percentages were calculated using standard mathematical formulas:", body_style))
    story.append(Paragraph("<b>Pass Percentage</b> = (Number of Passed Cases / Total Cases) × 100", center_bold))
    story.append(Spacer(1, 1 * mm))
    story.append(Paragraph("<b>Fail Percentage</b> = (Number of Failed Cases / Total Cases) × 100", center_bold))
    story.append(Spacer(1, 3 * mm))

    story.append(Paragraph("8.4 Pass Percentage Calculations", h2_style))
    story.append(Paragraph(
        "• <b>Manual Testing:</b> (39 / 39) × 100 = <b>100.00%</b><br/>"
        "• <b>Automation Testing:</b> (5 / 5) × 100 = <b>100.00%</b><br/>"
        "• <b>AI-Assisted Testing:</b> (5 / 5) × 100 = <b>100.00%</b><br/>"
        "• <b>Overall Composite Suite:</b> (49 / 49) × 100 = <b>100.00%</b>",
        body_style
    ))

    story.append(Paragraph("8.5 Failure Percentage Calculations", h2_style))
    story.append(Paragraph(
        "• <b>Manual Testing:</b> (0 / 39) × 100 = <b>0.00%</b><br/>"
        "• <b>Automation Testing:</b> (0 / 5) × 100 = <b>0.00%</b><br/>"
        "• <b>AI-Assisted Testing:</b> (0 / 5) × 100 = <b>0.00%</b><br/>"
        "• <b>Overall Composite Suite:</b> (0 / 49) × 100 = <b>0.00%</b>",
        body_style
    ))

    story.append(Paragraph("8.6 Percentage Summary", h2_style))
    story.append(Paragraph("Table 8.2 presents the finalized pass and fail percentages.", body_style))

    pct_data = [
        [Paragraph("<b>Testing Approach</b>", table_header), Paragraph("<b>Pass Percentage</b>", table_header), Paragraph("<b>Fail Percentage</b>", table_header)],
        [Paragraph("Manual Testing", table_cell_bold), Paragraph("100.00%", table_cell), Paragraph("0.00%", table_cell)],
        [Paragraph("Automation Testing", table_cell_bold), Paragraph("100.00%", table_cell), Paragraph("0.00%", table_cell)],
        [Paragraph("AI-Assisted Testing", table_cell_bold), Paragraph("100.00%", table_cell), Paragraph("0.00%", table_cell)],
        [Paragraph("<b>Overall Composite</b>", table_cell_bold), Paragraph("<b>100.00%</b>", table_cell_bold), Paragraph("<b>0.00%</b>", table_cell_bold)]
    ]
    t_pct = Table(pct_data, colWidths=[170, 150, 150])
    t_pct.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1C4E79")),
        ("ALIGN", (1, 0), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CCCCCC")),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    story.append(t_pct)
    story.append(Spacer(1, 4 * mm))

    story.append(Paragraph("8.7 Comparison of Testing Approaches", h2_style))
    story.append(Paragraph("Table 8.3 contrasts the operational characteristics of the three testing methodologies.", body_style))

    comp_data = [
        [Paragraph("<b>Parameter</b>", table_header), Paragraph("<b>Manual Testing</b>", table_header), Paragraph("<b>Automation Testing</b>", table_header), Paragraph("<b>AI-Assisted Testing</b>", table_header)],
        [Paragraph("Execution Speed", table_cell_bold), Paragraph("Slow (2-3 hrs)", table_cell), Paragraph("Fast (< 90 seconds)", table_cell), Paragraph("Fast (< 5 mins)", table_cell)],
        [Paragraph("Repeatability", table_cell_bold), Paragraph("Prone to fatigue", table_cell), Paragraph("100% deterministic", table_cell), Paragraph("Variable (probabilistic)", table_cell)],
        [Paragraph("Edge-Case Discovery", table_cell_bold), Paragraph("Limited to tester bias", table_cell), Paragraph("Scripted boundaries", table_cell), Paragraph("Broad and creative", table_cell)],
        [Paragraph("Setup Overhead", table_cell_bold), Paragraph("Minimal setup", table_cell), Paragraph("Requires scripting", table_cell), Paragraph("Prompt engineering", table_cell)],
        [Paragraph("Human Oversight", table_cell_bold), Paragraph("High", table_cell), Paragraph("Low (post-scripting)", table_cell), Paragraph("Critical (validation needed)", table_cell)]
    ]
    t_comp = Table(comp_data, colWidths=[100, 120, 125, 125])
    t_comp.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1C4E79")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CCCCCC")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8F9FA")]),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    story.append(t_comp)
    story.append(Spacer(1, 4 * mm))

    story.append(Paragraph("8.8 Overall Test Results", h2_style))
    story.append(Paragraph("Table 8.4 summarizes overall software quality indicators.", body_style))

    qual_data = [
        [Paragraph("<b>Quality Metric</b>", table_header), Paragraph("<b>Observed Value</b>", table_header)],
        [Paragraph("Total Test Cases Executed", table_cell_bold), Paragraph("49 Test Cases", table_cell)],
        [Paragraph("Total Test Cases Passed", table_cell_bold), Paragraph("49 Test Cases (100% Pass Rate)", table_cell)],
        [Paragraph("Total Defects Identified", table_cell_bold), Paragraph("6 Major Defects", table_cell)],
        [Paragraph("Defect Remediation Rate", table_cell_bold), Paragraph("100% (6 / 6 Resolved and Verified)", table_cell)],
        [Paragraph("Automated E2E Regression Suite Runtime", table_cell_bold), Paragraph("71.06 seconds across 20 Playwright scenarios", table_cell)],
        [Paragraph("Remaining High/Critical Vulnerabilities", table_cell_bold), Paragraph("0 (Zero open defects)", table_cell)]
    ]
    t_qual = Table(qual_data, colWidths=[235, 235])
    t_qual.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1C4E79")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CCCCCC")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8F9FA")]),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    story.append(t_qual)

    story.append(PageBreak())

    # ============================================================
    # CHAPTER 9: CONCLUSION & FUTURE SCOPE
    # ============================================================
    story.append(Paragraph("Chapter 9", ParagraphStyle("ChPre9", parent=h1_style, fontSize=13, spaceAfter=2)))
    story.append(Paragraph("CONCLUSION", h1_style))
    story.append(Spacer(1, 4 * mm))

    story.append(Paragraph("9.1 Conclusion", h2_style))
    story.append(Paragraph(
        "The Software Testing and Quality Assurance (STQA) mini-project for <b>ParikshaVinyas – Smart Examination Hall "
        "and Seat Allocation Management System</b> was completed successfully. Through a multi-tiered testing strategy combining "
        "manual black-box techniques, Playwright browser automation, and AI-assisted scenario derivation, the software "
        "application was comprehensively tested and verified.",
        body_style
    ))
    story.append(Paragraph(
        "The testing process evaluated critical operational requirements, including user authentication, student data ingestion, "
        "hall dimensioning, desk blocking, timetable collision prevention, multi-strategy seat allocation, interactive visual grids, "
        "and ReportLab PDF streaming. Applying Boundary Value Analysis and Equivalence Partitioning uncovered critical edge-case defects, "
        "such as capacity shortage transaction rollbacks, timetable scheduling overlaps, and unauthorized direct object references.",
        body_style
    ))
    story.append(Paragraph(
        "All six identified defects were systematically analyzed, resolved in source code, and validated through automated "
        "regression test suites. The finalized application achieved a 100% test pass rate, demonstrating exceptional architectural "
        "resilience, database consistency, and adherence to software engineering standards.",
        body_style
    ))

    story.append(Paragraph("9.2 Future Scope / Enhancements", h2_style))
    story.append(Paragraph(
        "Future quality assurance and engineering efforts can expand ParikshaVinyas in several key areas:",
        body_style
    ))
    story.append(Paragraph(
        "• <b>Biometric Candidate Verification:</b> Integrating facial recognition or fingerprint verification at examination hall entry doors.<br/>"
        "• <b>Dynamic QR Code Desk Slips:</b> Printing individualized QR codes on seating slips for instant attendance marking by invigilators via mobile cameras.<br/>"
        "• <b>Multi-Campus Distributed Allocation:</b> Enhancing the allocation engine to balance candidate cohorts across geographically separated campus buildings with transit time buffers.<br/>"
        "• <b>Continuous Integration (CI) Pipeline Integration:</b> Embedding Playwright and pytest regression suites into GitHub Actions for automated pull request verification.",
        body_style
    ))

    story.append(Spacer(1, 6 * mm))
    story.append(Paragraph("REFERENCES", h1_style))
    story.append(Spacer(1, 2 * mm))
    refs = [
        "[1] Microsoft Corporation, “Playwright for Python Documentation,” [Online]. Available: https://playwright.dev/python/",
        "[2] pytest Development Team, “pytest: helps you write better programs,” [Online]. Available: https://docs.pytest.org/",
        "[3] Pallets Projects, “Flask Documentation (v3.0),” [Online]. Available: https://flask.palletsprojects.com/",
        "[4] SQLAlchemy Authors, “SQLAlchemy 2.0 Documentation,” [Online]. Available: https://docs.sqlalchemy.org/",
        "[5] ReportLab Europe Ltd., “ReportLab PDF Generation User Guide,” [Online]. Available: https://www.reportlab.com/docs/reportlab-userguide.pdf",
        "[6] International Software Testing Qualifications Board (ISTQB), “Certified Tester Foundation Level Syllabus v4.0,” [Online]. Available: https://www.istqb.org/",
        "[7] G. J. Myers, C. Sandler, and T. Badgett, The Art of Software Testing, 3rd ed. Hoboken, NJ, USA: John Wiley & Sons, 2011.",
        "[8] Google DeepMind, “Gemini: A Family of Highly Capable Multimodal Models,” [Online]. Available: https://gemini.google.com/",
        "[9] Anthropic, “The Claude 3 Model Family: Opus, Sonnet, Haiku,” [Online]. Available: https://www.anthropic.com/claude",
        "[10] Google Labs, “NotebookLM: Personalized AI Research Assistant,” [Online]. Available: https://notebooklm.google.com/"
    ]
    for r in refs:
        story.append(Paragraph(r, ParagraphStyle("RefStyle", parent=body_style, fontSize=8, leading=11, spaceAfter=2)))

    story.append(PageBreak())

    # ============================================================
    # ABBREVIATIONS & APPENDIX
    # ============================================================
    story.append(Paragraph("ABBREVIATIONS", h1_style))
    story.append(Spacer(1, 3 * mm))
    abbr_data = [
        [Paragraph("<b>Abbreviation</b>", table_header), Paragraph("<b>Full Form</b>", table_header)],
        [Paragraph("AI", table_cell_bold), Paragraph("Artificial Intelligence", table_cell)],
        [Paragraph("API", table_cell_bold), Paragraph("Application Programming Interface", table_cell)],
        [Paragraph("AUT", table_cell_bold), Paragraph("Application Under Test", table_cell)],
        [Paragraph("BVA", table_cell_bold), Paragraph("Boundary Value Analysis", table_cell)],
        [Paragraph("CRUD", table_cell_bold), Paragraph("Create, Read, Update, Delete", table_cell)],
        [Paragraph("CSRF", table_cell_bold), Paragraph("Cross-Site Request Forgery", table_cell)],
        [Paragraph("DOM", table_cell_bold), Paragraph("Document Object Model", table_cell)],
        [Paragraph("E2E", table_cell_bold), Paragraph("End-to-End Browser Testing", table_cell)],
        [Paragraph("EP", table_cell_bold), Paragraph("Equivalence Partitioning", table_cell)],
        [Paragraph("HTML", table_cell_bold), Paragraph("HyperText Markup Language", table_cell)],
        [Paragraph("HTTP", table_cell_bold), Paragraph("HyperText Transfer Protocol", table_cell)],
        [Paragraph("IDOR", table_cell_bold), Paragraph("Insecure Direct Object Reference", table_cell)],
        [Paragraph("ISTQB", table_cell_bold), Paragraph("International Software Testing Qualifications Board", table_cell)],
        [Paragraph("ORM", table_cell_bold), Paragraph("Object-Relational Mapping", table_cell)],
        [Paragraph("PDF", table_cell_bold), Paragraph("Portable Document Format", table_cell)],
        [Paragraph("QA", table_cell_bold), Paragraph("Quality Assurance", table_cell)],
        [Paragraph("RBAC", table_cell_bold), Paragraph("Role-Based Access Control", table_cell)],
        [Paragraph("SDLC", table_cell_bold), Paragraph("Software Development Life Cycle", table_cell)],
        [Paragraph("SQL", table_cell_bold), Paragraph("Structured Query Language", table_cell)],
        [Paragraph("STQA", table_cell_bold), Paragraph("Software Testing and Quality Assurance", table_cell)],
        [Paragraph("TC", table_cell_bold), Paragraph("Test Case", table_cell)],
        [Paragraph("UI / UX", table_cell_bold), Paragraph("User Interface / User Experience", table_cell)]
    ]
    t_abbr = Table(abbr_data, colWidths=[120, 350])
    t_abbr.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1C4E79")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CCCCCC")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8F9FA")]),
        ("TOPPADDING", (0, 0), (-1, -1), 1.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1.5),
    ]))
    story.append(t_abbr)

    story.append(Spacer(1, 8 * mm))
    story.append(Paragraph("APPENDIX", h1_style))
    story.append(Spacer(1, 2 * mm))
    story.append(Paragraph("<b>Photographic Evidence of Practical STQA Execution</b>", h3_style))
    story.append(Paragraph(
        "The screenshot below provides verified photographic evidence of the live test execution, automated browser test suite, "
        "and defect tracking matrix during testing of the ParikshaVinyas examination system.",
        body_style
    ))
    add_fig("fig_appendix_testing.png", "Figure A.1: STQA Test Execution Matrix and Defect Tracking Session in Progress", width=420, height=220)

    doc.build(story, canvasmaker=NumberedCanvas)
    print("Successfully built PDF:", PDF_PATH)

if __name__ == "__main__":
    build_pdf()
