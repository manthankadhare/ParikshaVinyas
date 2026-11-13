from flask import Blueprint, render_template, send_file, flash, redirect, url_for
from flask_login import current_user
from app.models.student import Student
from app.models.allocation import SeatAllocation
from app.models.exam import Examination, EligibleStudent
from app.services.report_service import ReportService
from app.utils.decorators import student_required

student_portal_bp = Blueprint('student_portal', __name__)


@student_portal_bp.route('/dashboard')
@student_required
def dashboard():
    student = current_user.student_profile
    if not student:
        flash("No student profile linked to this user account.", "warning")
        return render_template('student_portal/empty.html')

    # Fetch all examinations the student is eligible for
    eligible_records = EligibleStudent.query.filter_by(student_id=student.id).all()
    exam_ids = [e.examination_id for e in eligible_records]

    exams = Examination.query.filter(Examination.id.in_(exam_ids)).order_by(Examination.exam_date, Examination.start_time).all() if exam_ids else []

    # Map allocations
    allocations = SeatAllocation.query.filter_by(student_id=student.id).all()
    alloc_map = {a.examination_id: a for a in allocations}

    return render_template(
        'student_portal/dashboard.html',
        student=student,
        exams=exams,
        alloc_map=alloc_map
    )


@student_portal_bp.route('/slip/pdf')
@student_required
def download_slip():
    student = current_user.student_profile
    if not student:
        flash("No student profile found.", "danger")
        return redirect(url_for('student_portal.dashboard'))

    buffer = ReportService.generate_student_seating_slip_pdf(student.id)
    return send_file(
        buffer,
        as_attachment=True,
        download_name=f"Examination_Seating_Slip_{student.enrollment_no}.pdf",
        mimetype='application/pdf'
    )

