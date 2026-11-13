from flask import Blueprint, render_template, send_file, flash, redirect, url_for, abort
from flask_login import current_user
from app.models.invigilator import Invigilator, InvigilatorAssignment
from app.models.exam import Examination
from app.models.hall import ExaminationHall
from app.models.allocation import SeatAllocation
from app.services.report_service import ReportService
from app.utils.decorators import invigilator_required

invigilator_bp = Blueprint('invigilator', __name__)


@invigilator_bp.route('/dashboard')
@invigilator_required
def dashboard():
    invigilator = current_user.invigilator_profile

    assignments = []
    if invigilator:
        assignments = InvigilatorAssignment.query.filter_by(
            invigilator_id=invigilator.id
        ).join(Examination).order_by(Examination.exam_date, Examination.start_time).all()
    else:
        # If admin is testing invigilator view
        assignments = InvigilatorAssignment.query.join(Examination).order_by(Examination.exam_date).all()

    return render_template('invigilator/dashboard.html', invigilator=invigilator, assignments=assignments)


@invigilator_bp.route('/hall/<int:hall_id>/exam/<int:exam_id>')
@invigilator_required
def hall_roster(hall_id, exam_id):
    exam = Examination.query.get_or_404(exam_id)
    hall = ExaminationHall.query.get_or_404(hall_id)

    # Authorization Check: Prevent IDOR / BOLA
    if not current_user.is_admin():
        inv = current_user.invigilator_profile
        if not inv:
            abort(403)
        assigned = InvigilatorAssignment.query.filter_by(
            invigilator_id=inv.id,
            hall_id=hall.id,
            examination_id=exam.id
        ).first()
        if not assigned:
            abort(403)

    allocations = SeatAllocation.query.filter_by(
        examination_id=exam.id,
        hall_id=hall.id
    ).order_by(SeatAllocation.row_num, SeatAllocation.col_num).all()

    return render_template('invigilator/roster.html', exam=exam, hall=hall, allocations=allocations)


@invigilator_bp.route('/hall/<int:hall_id>/exam/<int:exam_id>/pdf')
@invigilator_required
def download_roster_pdf(hall_id, exam_id):
    exam = Examination.query.get_or_404(exam_id)
    hall = ExaminationHall.query.get_or_404(hall_id)

    # Authorization Check: Prevent IDOR / BOLA
    if not current_user.is_admin():
        inv = current_user.invigilator_profile
        if not inv:
            abort(403)
        assigned = InvigilatorAssignment.query.filter_by(
            invigilator_id=inv.id,
            hall_id=hall.id,
            examination_id=exam.id
        ).first()
        if not assigned:
            abort(403)

    buffer = ReportService.generate_hall_seating_pdf(exam_id, hall_id)
    return send_file(
        buffer,
        as_attachment=True,
        download_name=f"Attendance_Sheet_{hall.hall_code}_{exam.exam_code}.pdf",
        mimetype='application/pdf'
    )

