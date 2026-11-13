import csv
import io
from flask import Blueprint, render_template, redirect, url_for, flash, request, Response
from werkzeug.utils import secure_filename
from app import db
from app.models.student import Student
from app.models.user import User
from app.models.academic import Course
from app.forms.student_forms import StudentForm, StudentCSVUploadForm
from app.utils.decorators import admin_required
from app.services.audit_service import log_activity
from app.services.report_service import ReportService

student_bp = Blueprint('student', __name__)


@student_bp.route('/')
@admin_required
def index():
    search_query = request.args.get('q', '').strip()
    course_filter = request.args.get('course_id', type=int)
    semester_filter = request.args.get('semester', type=int)
    division_filter = request.args.get('division', '').strip()
    page = request.args.get('page', 1, type=int)

    query = Student.query.join(Course)

    if search_query:
        query = query.filter(
            (Student.enrollment_no.ilike(f"%{search_query}%")) |
            (Student.full_name.ilike(f"%{search_query}%")) |
            (Student.email.ilike(f"%{search_query}%"))
        )
    if course_filter:
        query = query.filter(Student.course_id == course_filter)
    if semester_filter:
        query = query.filter(Student.semester == semester_filter)
    if division_filter:
        query = query.filter(Student.division == division_filter)

    students = query.order_by(Student.enrollment_no).paginate(page=page, per_page=15, error_out=False)
    courses = Course.query.order_by(Course.code).all()

    return render_template(
        'students/index.html',
        students=students,
        courses=courses,
        search_query=search_query,
        course_filter=course_filter,
        semester_filter=semester_filter,
        division_filter=division_filter
    )


@student_bp.route('/add', methods=['GET', 'POST'])
@admin_required
def add():
    form = StudentForm()
    form.course_id.choices = [(c.id, f"{c.code} - {c.name}") for c in Course.query.order_by(Course.code).all()]

    if form.validate_on_submit():
        # Validate unique enrollment
        existing = Student.query.filter_by(enrollment_no=form.enrollment_no.data.strip()).first()
        if existing:
            flash(f"Error: A student with enrollment number '{form.enrollment_no.data}' already exists.", 'danger')
            return render_template('students/form.html', form=form, title='Add Student')

        # Check unique email
        existing_email = Student.query.filter_by(email=form.email.data.strip().lower()).first()
        if existing_email:
            flash(f"Error: Email address '{form.email.data}' is already registered to another student.", 'danger')
            return render_template('students/form.html', form=form, title='Add Student')

        # Create student user account for login
        username = form.enrollment_no.data.strip().lower()
        user = User.query.filter_by(username=username).first()
        if not user:
            user = User(
                username=username,
                email=form.email.data.strip().lower(),
                role='student'
            )
            # Default password format: Student@<Last4OfEnrollment>
            last4 = form.enrollment_no.data.strip()[-4:] if len(form.enrollment_no.data.strip()) >= 4 else "1234"
            user.set_password(f"Student@{last4}")
            db.session.add(user)
            db.session.flush()

        student = Student(
            user_id=user.id,
            enrollment_no=form.enrollment_no.data.strip().upper(),
            full_name=form.full_name.data.strip(),
            email=form.email.data.strip().lower(),
            mobile=form.mobile.data.strip(),
            course_id=form.course_id.data,
            branch=form.branch.data.strip(),
            semester=form.semester.data,
            division=form.division.data.strip().upper(),
            academic_year=form.academic_year.data.strip(),
            status=form.status.data
        )
        db.session.add(student)
        db.session.commit()

        log_activity('Add Student', 'Student Management', f"Created student {student.enrollment_no} ({student.full_name})")
        flash(f"Student {student.full_name} ({student.enrollment_no}) successfully added! Default login password: Student@{last4}", 'success')
        return redirect(url_for('student.index'))

    return render_template('students/form.html', form=form, title='Add Student')


@student_bp.route('/<int:student_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit(student_id):
    student = Student.query.get_or_404(student_id)
    form = StudentForm(obj=student)
    form.course_id.choices = [(c.id, f"{c.code} - {c.name}") for c in Course.query.order_by(Course.code).all()]

    if form.validate_on_submit():
        # Validate unique enrollment
        dup = Student.query.filter(Student.enrollment_no == form.enrollment_no.data.strip(), Student.id != student.id).first()
        if dup:
            flash(f"Error: Enrollment number '{form.enrollment_no.data}' is already used by another student.", 'danger')
            return render_template('students/form.html', form=form, title='Edit Student', student=student)

        # Validate unique email
        dup_email = Student.query.filter(Student.email == form.email.data.strip().lower(), Student.id != student.id).first()
        if dup_email:
            flash(f"Error: Email address '{form.email.data}' is already used by another student.", 'danger')
            return render_template('students/form.html', form=form, title='Edit Student', student=student)

        student.enrollment_no = form.enrollment_no.data.strip().upper()
        student.full_name = form.full_name.data.strip()
        student.email = form.email.data.strip().lower()
        student.mobile = form.mobile.data.strip()
        student.course_id = form.course_id.data
        student.branch = form.branch.data.strip()
        student.semester = form.semester.data
        student.division = form.division.data.strip().upper()
        student.academic_year = form.academic_year.data.strip()
        student.status = form.status.data

        # Update linked user email
        if student.user:
            student.user.email = student.email

        db.session.commit()
        log_activity('Edit Student', 'Student Management', f"Updated details for student {student.enrollment_no}")
        flash(f"Student {student.full_name} updated successfully.", 'success')
        return redirect(url_for('student.index'))

    return render_template('students/form.html', form=form, title='Edit Student', student=student)


@student_bp.route('/<int:student_id>/delete', methods=['POST'])
@admin_required
def delete(student_id):
    student = Student.query.get_or_404(student_id)
    enrollment = student.enrollment_no
    name = student.full_name

    user = student.user
    db.session.delete(student)
    if user:
        db.session.delete(user)
    db.session.commit()

    log_activity('Delete Student', 'Student Management', f"Deleted student {enrollment} ({name})")
    flash(f"Student {name} ({enrollment}) has been permanently deleted.", 'warning')
    return redirect(url_for('student.index'))


@student_bp.route('/<int:student_id>')
@admin_required
def view_profile(student_id):
    student = Student.query.get_or_404(student_id)
    allocations = student.allocations.all()
    return render_template('students/profile.html', student=student, allocations=allocations)


@student_bp.route('/import', methods=['GET', 'POST'])
@admin_required
def import_csv():
    form = StudentCSVUploadForm()
    errors = []
    success_count = 0

    if form.validate_on_submit():
        csv_file = form.csv_file.data
        try:
            stream = io.StringIO(csv_file.stream.read().decode("UTF-8"), newline=None)
            reader = csv.DictReader(stream)

            # Check header
            required_cols = {'Enrollment Number', 'Full Name', 'Email', 'Course Code', 'Semester', 'Division'}
            headers = set(reader.fieldnames or [])
            if not required_cols.issubset(headers):
                flash(f"Invalid CSV Header format. Missing columns: {required_cols - headers}", 'danger')
                return render_template('students/import.html', form=form, errors=errors)

            seen_enrollments = set()
            seen_emails = set()

            for line_no, row in enumerate(reader, start=2):
                enrollment = (row.get('Enrollment Number') or '').strip().upper()
                name = (row.get('Full Name') or '').strip()
                email = (row.get('Email') or '').strip().lower()
                mobile = (row.get('Mobile') or '9876543210').strip()
                course_code = (row.get('Course Code') or '').strip().upper()
                sem_str = (row.get('Semester') or '').strip()
                division = (row.get('Division') or 'A').strip().upper()
                branch = (row.get('Branch') or 'Engineering').strip()
                acad = (row.get('Academic Year') or '2025-2026').strip()

                if not enrollment or not name or not email or not course_code or not sem_str:
                    errors.append(f"Row {line_no}: Missing required values for enrollment, name, email, or course.")
                    continue

                try:
                    sem = int(sem_str)
                    if sem < 1 or sem > 8:
                        errors.append(f"Row {line_no}: Semester '{sem_str}' is out of valid range (1-8).")
                        continue
                except ValueError:
                    errors.append(f"Row {line_no}: Semester '{sem_str}' is not a valid integer.")
                    continue

                course = Course.query.filter_by(code=course_code).first()
                if not course:
                    errors.append(f"Row {line_no}: Course code '{course_code}' does not exist.")
                    continue

                # In-batch duplicate validation
                if enrollment in seen_enrollments:
                    errors.append(f"Row {line_no}: Duplicate enrollment number '{enrollment}' within this CSV batch. Skipping.")
                    continue
                if email in seen_emails:
                    errors.append(f"Row {line_no}: Duplicate email address '{email}' within this CSV batch. Skipping.")
                    continue

                # Database duplicate validation
                if Student.query.filter_by(enrollment_no=enrollment).first():
                    errors.append(f"Row {line_no}: Duplicate enrollment number '{enrollment}' already exists in database. Skipping.")
                    continue

                if Student.query.filter_by(email=email).first() or User.query.filter_by(email=email).first():
                    errors.append(f"Row {line_no}: Duplicate email address '{email}' already registered in system. Skipping.")
                    continue

                seen_enrollments.add(enrollment)
                seen_emails.add(email)

                # Create user login
                username = enrollment.lower()
                user = User.query.filter_by(username=username).first()
                if not user:
                    user = User(username=username, email=email, role='student')
                    last4 = enrollment[-4:] if len(enrollment) >= 4 else "1234"
                    user.set_password(f"Student@{last4}")
                    db.session.add(user)
                    db.session.flush()

                new_student = Student(
                    user_id=user.id,
                    enrollment_no=enrollment,
                    full_name=name,
                    email=email,
                    mobile=mobile,
                    course_id=course.id,
                    branch=branch,
                    semester=sem,
                    division=division,
                    academic_year=acad,
                    status='Active'
                )
                db.session.add(new_student)
                success_count += 1

            db.session.commit()
            log_activity('Bulk CSV Import', 'Student Management', f"Imported {success_count} students via CSV ({len(errors)} errors)")
            flash(f"Bulk import completed: Successfully added {success_count} students.", 'success')

        except Exception as e:
            db.session.rollback()
            flash(f"Error parsing CSV file: {str(e)}", 'danger')

    return render_template('students/import.html', form=form, errors=errors, success_count=success_count)


@student_bp.route('/export')
@admin_required
def export_csv():
    csv_data = ReportService.export_students_csv()
    log_activity('Export Students', 'Student Management', 'Exported student roster as CSV')
    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=students_export.csv"}
    )

