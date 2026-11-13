import io
import csv
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from flask import current_app
from app.models.academic import Course, Subject
from app.models.exam import Examination
from app.models.hall import ExaminationHall
from app.models.student import Student
from app.models.allocation import SeatAllocation
from app.models.invigilator import InvigilatorAssignment
from app.models.audit import SystemSetting


class ReportService:
    """Generates professional PDF and CSV reports for ParikshaVinyas."""

    @staticmethod
    def _get_institution_info():
        inst = SystemSetting.query.filter_by(key='college_name').first()
        college = inst.value if inst else current_app.config.get('COLLEGE_NAME', 'UPL University of Sustainable Technology')
        acad = SystemSetting.query.filter_by(key='academic_year').first()
        academic_year = acad.value if acad else current_app.config.get('ACADEMIC_YEAR', '2025-2026')
        return college, academic_year

    @classmethod
    def _build_header(cls, title, subtitle=None):
        college, academic_year = cls._get_institution_info()
        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(
            'HeaderTitle',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=16,
            leading=20,
            textColor=colors.HexColor('#0F172A'),
            alignment=1
        )
        sub_style = ParagraphStyle(
            'HeaderSub',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=11,
            leading=15,
            textColor=colors.HexColor('#2563EB'),
            alignment=1
        )
        doc_title_style = ParagraphStyle(
            'DocTitle',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=13,
            leading=17,
            textColor=colors.HexColor('#D97706'),
            alignment=1
        )
        meta_style = ParagraphStyle(
            'MetaStyle',
            parent=styles['Normal'],
            fontName='Helvetica-Oblique',
            fontSize=8,
            leading=10,
            textColor=colors.HexColor('#64748B'),
            alignment=2
        )

        elements = [
            Paragraph(f"<b>{college}</b>", title_style),
            Spacer(1, 3),
            Paragraph(f"Academic Examination Management System — AY {academic_year}", sub_style),
            Spacer(1, 4),
            Paragraph(f"<b>{title}</b>", doc_title_style),
        ]
        if subtitle:
            elements.append(Paragraph(subtitle, sub_style))
        elements.append(Spacer(1, 4))
        elements.append(Paragraph(f"Generated: {datetime.now().strftime('%d-%b-%Y %I:%M %p')} | ParikshaVinyas STQA Engine", meta_style))
        elements.append(Spacer(1, 10))
        return elements

    @classmethod
    def generate_exam_allocation_pdf(cls, examination_id):
        exam = Examination.query.get_or_404(examination_id)
        allocations = SeatAllocation.query.filter_by(examination_id=exam.id).join(Student).order_by(SeatAllocation.seat_identifier).all()

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=36,
            leftMargin=36,
            topMargin=36,
            bottomMargin=36
        )
        elements = cls._build_header(
            title=f"Examination Seating Chart: {exam.exam_code}",
            subtitle=f"{exam.exam_name} | {exam.subject.name} ({exam.course.code} Sem-{exam.semester})"
        )

        # Meta summary table
        styles = getSampleStyleSheet()
        meta_data = [
            [
                Paragraph("<b>Date:</b> " + exam.exam_date.strftime('%d-%b-%Y'), styles['Normal']),
                Paragraph("<b>Time:</b> " + f"{exam.start_time.strftime('%I:%M %p')} - {exam.end_time.strftime('%I:%M %p')}", styles['Normal']),
                Paragraph("<b>Total Allocated:</b> " + str(len(allocations)), styles['Normal']),
            ]
        ]
        meta_table = Table(meta_data, colWidths=[170, 180, 170])
        meta_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F1F5F9')),
            ('PADDING', (0, 0), (-1, -1), 6),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#CBD5E1')),
        ]))
        elements.append(meta_table)
        elements.append(Spacer(1, 12))

        # Main Table
        data = [
            ['#', 'Seat Identifier', 'Hall Code', 'Enrollment No', 'Student Name', 'Course / Div']
        ]
        for idx, a in enumerate(allocations, start=1):
            s = a.student
            data.append([
                str(idx),
                a.seat_identifier,
                a.hall.hall_code,
                s.enrollment_no,
                s.full_name,
                f"{s.branch} (Div {s.division})"
            ])

        table = Table(data, colWidths=[28, 95, 75, 95, 145, 84])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0F172A')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
            ('TOPPADDING', (0, 0), (-1, 0), 6),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 8.5),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')]),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
            ('ALIGN', (0, 0), (0, -1), 'CENTER'),
            ('ALIGN', (1, 0), (2, -1), 'CENTER'),
        ]))
        elements.append(table)

        doc.build(elements)
        buffer.seek(0)
        return buffer

    @classmethod
    def generate_hall_seating_pdf(cls, examination_id, hall_id):
        exam = Examination.query.get_or_404(examination_id)
        hall = ExaminationHall.query.get_or_404(hall_id)
        allocations = SeatAllocation.query.filter_by(
            examination_id=exam.id,
            hall_id=hall.id
        ).order_by(SeatAllocation.row_num, SeatAllocation.col_num).all()

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=36,
            leftMargin=36,
            topMargin=36,
            bottomMargin=36
        )
        elements = cls._build_header(
            title=f"Hall Seating Arrangement: {hall.hall_code} ({hall.hall_name})",
            subtitle=f"Building: {hall.building}, Floor: {hall.floor} | Exam: {exam.exam_code} ({exam.exam_name})"
        )

        data = [
            ['#', 'Seat No', 'Row', 'Col', 'Enrollment No', 'Student Name', 'Course & Sem', 'Signature']
        ]
        for idx, a in enumerate(allocations, start=1):
            s = a.student
            data.append([
                str(idx),
                a.seat_identifier,
                f"R-{a.row_num}",
                f"C-{a.col_num}",
                s.enrollment_no,
                s.full_name,
                f"{s.branch} S-{s.semester}",
                ""
            ])

        table = Table(data, colWidths=[24, 75, 40, 40, 85, 125, 75, 58])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E293B')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 8.5),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')]),
            ('ALIGN', (0, 0), (3, -1), 'CENTER'),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 5),
            ('TOPPADDING', (0, 1), (-1, -1), 5),
        ]))
        elements.append(table)

        doc.build(elements)
        buffer.seek(0)
        return buffer

    @classmethod
    def generate_student_seating_slip_pdf(cls, student_id):
        student = Student.query.get_or_404(student_id)
        allocations = SeatAllocation.query.filter_by(student_id=student.id).join(Examination).order_by(Examination.exam_date).all()

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=36,
            leftMargin=36,
            topMargin=36,
            bottomMargin=36
        )
        elements = cls._build_header(
            title="Official Student Examination Seating Slip / Admit Card",
            subtitle=f"Candidate: {student.full_name} | Enrollment No: {student.enrollment_no}"
        )

        styles = getSampleStyleSheet()
        info_data = [
            [
                Paragraph(f"<b>Enrollment:</b> {student.enrollment_no}", styles['Normal']),
                Paragraph(f"<b>Student Name:</b> {student.full_name}", styles['Normal']),
            ],
            [
                Paragraph(f"<b>Course:</b> {student.course.name} ({student.branch})", styles['Normal']),
                Paragraph(f"<b>Semester / Div:</b> Sem {student.semester} - Div {student.division}", styles['Normal']),
            ],
            [
                Paragraph(f"<b>Email:</b> {student.email}", styles['Normal']),
                Paragraph(f"<b>Mobile:</b> {student.mobile}", styles['Normal']),
            ]
        ]
        info_table = Table(info_data, colWidths=[260, 260])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8FAFC')),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#94A3B8')),
            ('PADDING', (0, 0), (-1, -1), 6),
        ]))
        elements.append(info_table)
        elements.append(Spacer(1, 14))

        elements.append(Paragraph("<b>Scheduled Examinations & Allocated Seats:</b>", styles['Heading4']))
        elements.append(Spacer(1, 6))

        data = [
            ['Exam Code', 'Subject', 'Date', 'Timing', 'Hall Code', 'Seat No']
        ]
        if not allocations:
            data.append(['No allocations generated yet.', '-', '-', '-', '-', '-'])
        else:
            for a in allocations:
                ex = a.examination
                data.append([
                    ex.exam_code,
                    f"{ex.subject.code} - {ex.subject.name}",
                    ex.exam_date.strftime('%d-%b-%Y'),
                    f"{ex.start_time.strftime('%I:%M %p')} - {ex.end_time.strftime('%I:%M %p')}",
                    f"{a.hall.hall_code} ({a.hall.building})",
                    a.seat_identifier
                ])

        table = Table(data, colWidths=[70, 150, 75, 105, 70, 50])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E3A8A')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 8.5),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')]),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('PADDING', (0, 0), (-1, -1), 5),
            ('ALIGN', (0, 0), (0, -1), 'CENTER'),
            ('ALIGN', (2, 0), (3, -1), 'CENTER'),
            ('ALIGN', (4, 0), (5, -1), 'CENTER'),
        ]))
        elements.append(table)
        elements.append(Spacer(1, 20))

        # Instructions
        inst_p = Paragraph(
            "<b>Instructions for Candidates:</b><br/>"
            "1. Candidates must occupy their designated seats at least 15 minutes prior to the exam.<br/>"
            "2. Valid Institute ID Card and this seating slip are mandatory for entry.<br/>"
            "3. Any unauthorized electronic devices or materials are strictly prohibited.<br/>"
            "4. Allocation verification is monitored under STQA automated integrity checks.",
            styles['Normal']
        )
        elements.append(inst_p)

        doc.build(elements)
        buffer.seek(0)
        return buffer

    @classmethod
    def generate_hall_utilization_pdf(cls):
        halls = ExaminationHall.query.order_by(ExaminationHall.hall_code).all()
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
        elements = cls._build_header(
            title="Examination Hall Capacity & Utilization Audit Report",
            subtitle="Complete inventory of active halls, blocked seats, and available seats"
        )

        data = [
            ['Hall Code', 'Hall Name', 'Building / Floor', 'Dimensions', 'Total Cap.', 'Blocked', 'Usable Cap.', 'Status']
        ]
        total_cap = 0
        total_blocked = 0
        total_usable = 0

        for h in halls:
            total_cap += h.total_capacity
            total_blocked += h.blocked_count
            total_usable += h.usable_capacity
            data.append([
                h.hall_code,
                h.hall_name,
                f"{h.building} ({h.floor})",
                f"{h.num_rows} x {h.num_cols}",
                str(h.total_capacity),
                str(h.blocked_count),
                str(h.usable_capacity),
                h.status
            ])

        data.append(['Total / Summary', '', '', '', str(total_cap), str(total_blocked), str(total_usable), 'Active'])

        table = Table(data, colWidths=[70, 110, 110, 65, 55, 45, 60, 45])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0F172A')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.white, colors.HexColor('#F8FAFC')]),
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#E2E8F0')),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('PADDING', (0, 0), (-1, -1), 5),
            ('ALIGN', (3, 0), (6, -1), 'CENTER'),
        ]))
        elements.append(table)

        doc.build(elements)
        buffer.seek(0)
        return buffer

    @classmethod
    def export_allocations_csv(cls, examination_id):
        exam = Examination.query.get_or_404(examination_id)
        allocations = SeatAllocation.query.filter_by(examination_id=exam.id).join(Student).order_by(SeatAllocation.seat_identifier).all()

        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['Examination Code', 'Examination Name', 'Exam Date', 'Seat Identifier', 'Hall Code', 'Hall Name', 'Row', 'Col', 'Enrollment Number', 'Student Name', 'Course', 'Branch', 'Semester', 'Division', 'Allocation Strategy', 'Allocated At'])

        for a in allocations:
            s = a.student
            h = a.hall
            writer.writerow([
                exam.exam_code,
                exam.exam_name,
                exam.exam_date.strftime('%Y-%m-%d'),
                a.seat_identifier,
                h.hall_code,
                h.hall_name,
                a.row_num,
                a.col_num,
                s.enrollment_no,
                s.full_name,
                s.course.name,
                s.branch,
                s.semester,
                s.division,
                a.strategy_used,
                a.allocated_at.strftime('%Y-%m-%d %H:%M:%S')
            ])

        output.seek(0)
        return output.getvalue()

    @classmethod
    def export_students_csv(cls):
        students = Student.query.order_by(Student.enrollment_no).all()
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['Enrollment Number', 'Full Name', 'Email', 'Mobile', 'Course Code', 'Branch', 'Semester', 'Division', 'Academic Year', 'Status'])

        for s in students:
            writer.writerow([
                s.enrollment_no,
                s.full_name,
                s.email,
                s.mobile,
                s.course.code,
                s.branch,
                s.semester,
                s.division,
                s.academic_year,
                s.status
            ])

        output.seek(0)
        return output.getvalue()

