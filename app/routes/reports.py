from flask import Blueprint, render_template, send_file, Response, request, flash, redirect, url_for
from app.models.exam import Examination, EligibleStudent
from app.models.hall import ExaminationHall
from app.models.student import Student
from app.models.allocation import SeatAllocation
from app.services.report_service import ReportService
from app.utils.decorators import admin_required

reports_bp = Blueprint('reports', __name__)


@reports_bp.route('/')
@admin_required
def index():
    exams = Examination.query.order_by(Examination.exam_date.desc()).all()
    halls = ExaminationHall.query.filter_by(status='Active').order_by(ExaminationHall.hall_code).all()
    students = Student.query.order_by(Student.enrollment_no).limit(100).all()
    return render_template('reports/index.html', exams=exams, halls=halls, students=students)


@reports_bp.route('/exam/<int:exam_id>/pdf')
@admin_required
def exam_pdf(exam_id):
    exam = Examination.query.get_or_404(exam_id)
    buffer = ReportService.generate_exam_allocation_pdf(exam.id)
    filename = f"Allocation_{exam.exam_code}.pdf"
    return send_file(
        buffer,
        as_attachment=True,
        download_name=filename,
        mimetype='application/pdf'
    )


@reports_bp.route('/hall/<int:hall_id>/exam/<int:exam_id>/pdf')
@admin_required
def hall_pdf(hall_id, exam_id):
    exam = Examination.query.get_or_404(exam_id)
    hall = ExaminationHall.query.get_or_404(hall_id)
    buffer = ReportService.generate_hall_seating_pdf(exam.id, hall.id)
    filename = f"Seating_{hall.hall_code}_{exam.exam_code}.pdf"
    return send_file(
        buffer,
        as_attachment=True,
        download_name=filename,
        mimetype='application/pdf'
    )


@reports_bp.route('/student/<int:student_id>/pdf')
@admin_required
def student_slip_pdf(student_id):
    student = Student.query.get_or_404(student_id)
    buffer = ReportService.generate_student_seating_slip_pdf(student.id)
    filename = f"SeatingSlip_{student.enrollment_no}.pdf"
    return send_file(
        buffer,
        as_attachment=True,
        download_name=filename,
        mimetype='application/pdf'
    )


@reports_bp.route('/hall-utilization/pdf')
@admin_required
def hall_utilization_pdf():
    buffer = ReportService.generate_hall_utilization_pdf()
    return send_file(
        buffer,
        as_attachment=True,
        download_name="Hall_Capacity_Utilization_Report.pdf",
        mimetype='application/pdf'
    )


@reports_bp.route('/unallocated')
@admin_required
def unallocated():
    exam_id = request.args.get('exam_id', type=int)
    exams = Examination.query.order_by(Examination.exam_date.desc()).all()

    unallocated_students = []
    selected_exam = None

    if exam_id:
        selected_exam = Examination.query.get(exam_id)
        if selected_exam:
            # Students eligible for exam who don't have an allocation in seat_allocations
            allocated_student_ids = [a.student_id for a in selected_exam.allocations.all()]
            eligible_entries = EligibleStudent.query.filter_by(examination_id=selected_exam.id).all()
            eligible_student_ids = [e.student_id for e in eligible_entries]

            unallocated_ids = set(eligible_student_ids) - set(allocated_student_ids)
            unallocated_students = Student.query.filter(Student.id.in_(unallocated_ids)).order_by(Student.enrollment_no).all()

    return render_template('reports/unallocated.html', exams=exams, selected_exam=selected_exam, unallocated_students=unallocated_students)


@reports_bp.route('/exam/<int:exam_id>/csv')
@admin_required
def exam_csv(exam_id):
    csv_str = ReportService.export_allocations_csv(exam_id)
    exam = Examination.query.get_or_404(exam_id)
    return Response(
        csv_str,
        mimetype="text/csv",
        headers={"Content-disposition": f"attachment; filename=allocations_{exam.exam_code}.csv"}
    )

