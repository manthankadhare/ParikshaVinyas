from flask import Blueprint, render_template, redirect, url_for, flash, request
from datetime import datetime, timedelta
from app import db
from app.models.exam import Examination, EligibleStudent
from app.models.academic import Course, Subject
from app.models.student import Student
from app.forms.exam_forms import ExamForm
from app.utils.decorators import admin_required
from app.services.audit_service import log_activity

exam_bp = Blueprint('exam', __name__)


@exam_bp.route('/')
@admin_required
def index():
    status_filter = request.args.get('status', '')
    course_filter = request.args.get('course_id', type=int)

    query = Examination.query.join(Subject).join(Course)

    if status_filter:
        query = query.filter(Examination.status == status_filter)
    if course_filter:
        query = query.filter(Examination.course_id == course_filter)

    exams = query.order_by(Examination.exam_date.desc(), Examination.start_time).all()
    courses = Course.query.order_by(Course.code).all()

    return render_template('exams/index.html', exams=exams, courses=courses, status_filter=status_filter, course_filter=course_filter)


@exam_bp.route('/add', methods=['GET', 'POST'])
@admin_required
def add():
    form = ExamForm()
    form.course_id.choices = [(c.id, f"{c.code} - {c.name}") for c in Course.query.order_by(Course.code).all()]
    form.subject_id.choices = [(s.id, f"{s.code} - {s.name} (Sem {s.semester})") for s in Subject.query.order_by(Subject.code).all()]

    if form.validate_on_submit():
        code = form.exam_code.data.strip().upper()
        if Examination.query.filter_by(exam_code=code).first():
            flash(f"Examination code '{code}' already exists.", 'danger')
            return render_template('exams/form.html', form=form, title='Schedule Examination')

        start = form.start_time.data
        end = form.end_time.data
        if end <= start:
            flash("Validation Error: Examination end time must be later than start time.", 'danger')
            return render_template('exams/form.html', form=form, title='Schedule Examination')

        # Check for conflicting exam for same course and semester on same date & overlapping time
        conflict = Examination.query.filter(
            Examination.course_id == form.course_id.data,
            Examination.semester == form.semester.data,
            Examination.exam_date == form.exam_date.data,
            Examination.status != 'Cancelled',
            Examination.start_time < end,
            Examination.end_time > start
        ).first()

        if conflict:
            flash(f"Scheduling Conflict: Course {conflict.course.code} Sem {conflict.semester} already has exam '{conflict.exam_name}' scheduled at overlapping time ({conflict.start_time} - {conflict.end_time}).", 'danger')
            return render_template('exams/form.html', form=form, title='Schedule Examination')

        exam = Examination(
            exam_code=code,
            exam_name=form.exam_name.data.strip(),
            course_id=form.course_id.data,
            subject_id=form.subject_id.data,
            semester=form.semester.data,
            exam_date=form.exam_date.data,
            start_time=start,
            end_time=end,
            duration_minutes=form.duration_minutes.data,
            exam_type=form.exam_type.data,
            academic_year=form.academic_year.data.strip(),
            status=form.status.data
        )
        db.session.add(exam)
        db.session.flush()

        # Automatically enroll eligible active students matching this course and semester
        eligible_students = Student.query.filter_by(
            course_id=exam.course_id,
            semester=exam.semester,
            status='Active'
        ).all()

        for st in eligible_students:
            el = EligibleStudent(examination_id=exam.id, student_id=st.id)
            db.session.add(el)

        db.session.commit()
        log_activity('Schedule Exam', 'Exam Management', f"Created exam {exam.exam_code} with {len(eligible_students)} eligible candidates enrolled.")
        flash(f"Examination '{exam.exam_name}' scheduled successfully with {len(eligible_students)} eligible candidates.", 'success')
        return redirect(url_for('exam.index'))

    return render_template('exams/form.html', form=form, title='Schedule Examination')


@exam_bp.route('/<int:exam_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit(exam_id):
    exam = Examination.query.get_or_404(exam_id)
    form = ExamForm(obj=exam)
    form.course_id.choices = [(c.id, f"{c.code} - {c.name}") for c in Course.query.order_by(Course.code).all()]
    form.subject_id.choices = [(s.id, f"{s.code} - {s.name} (Sem {s.semester})") for s in Subject.query.order_by(Subject.code).all()]

    if form.validate_on_submit():
        code = form.exam_code.data.strip().upper()
        dup = Examination.query.filter(Examination.exam_code == code, Examination.id != exam.id).first()
        if dup:
            flash(f"Examination code '{code}' already in use.", 'danger')
            return render_template('exams/form.html', form=form, title='Edit Examination', exam=exam)

        start = form.start_time.data
        end = form.end_time.data
        if end <= start:
            flash("Validation Error: Examination end time must be later than start time.", 'danger')
            return render_template('exams/form.html', form=form, title='Edit Examination', exam=exam)

        # Check for conflicting exam for same course and semester on same date & overlapping time
        conflict = Examination.query.filter(
            Examination.id != exam.id,
            Examination.course_id == form.course_id.data,
            Examination.semester == form.semester.data,
            Examination.exam_date == form.exam_date.data,
            Examination.status != 'Cancelled',
            Examination.start_time < end,
            Examination.end_time > start
        ).first()

        if conflict:
            flash(f"Scheduling Conflict: Course {conflict.course.code} Sem {conflict.semester} already has exam '{conflict.exam_name}' scheduled at overlapping time ({conflict.start_time} - {conflict.end_time}).", 'danger')
            return render_template('exams/form.html', form=form, title='Edit Examination', exam=exam)

        exam.exam_code = code
        exam.exam_name = form.exam_name.data.strip()
        exam.course_id = form.course_id.data
        exam.subject_id = form.subject_id.data
        exam.semester = form.semester.data
        exam.exam_date = form.exam_date.data
        exam.start_time = start
        exam.end_time = end
        exam.duration_minutes = form.duration_minutes.data
        exam.exam_type = form.exam_type.data
        exam.academic_year = form.academic_year.data.strip()
        exam.status = form.status.data

        db.session.commit()
        log_activity('Edit Exam', 'Exam Management', f"Updated exam {exam.exam_code}")
        flash(f"Examination '{exam.exam_name}' updated successfully.", 'success')
        return redirect(url_for('exam.index'))

    return render_template('exams/form.html', form=form, title='Edit Examination', exam=exam)


@exam_bp.route('/<int:exam_id>/delete', methods=['POST'])
@admin_required
def delete(exam_id):
    exam = Examination.query.get_or_404(exam_id)
    code = exam.exam_code
    db.session.delete(exam)
    db.session.commit()
    log_activity('Delete Exam', 'Exam Management', f"Deleted exam {code}")
    flash(f"Examination '{code}' deleted.", 'warning')
    return redirect(url_for('exam.index'))


@exam_bp.route('/<int:exam_id>')
@admin_required
def details(exam_id):
    exam = Examination.query.get_or_404(exam_id)
    eligible = EligibleStudent.query.filter_by(examination_id=exam.id).join(Student).order_by(Student.enrollment_no).all()
    allocations = exam.allocations.join(Student).order_by(Student.enrollment_no).all()
    return render_template('exams/details.html', exam=exam, eligible=eligible, allocations=allocations)

