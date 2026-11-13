from flask import Blueprint, render_template, redirect, url_for, flash, request
from app import db
from app.models.academic import Course, Subject, Department
from app.utils.decorators import admin_required
from app.services.audit_service import log_activity

academic_bp = Blueprint('academic', __name__)


@academic_bp.route('/courses', methods=['GET', 'POST'])
@admin_required
def courses():
    if request.method == 'POST':
        code = request.form.get('code', '').strip().upper()
        name = request.form.get('name', '').strip()
        department = request.form.get('department', '').strip()
        total_semesters = request.form.get('total_semesters', type=int) or 8

        if not code or not name or not department:
            flash('All course fields are required.', 'danger')
            return redirect(url_for('academic.courses'))

        existing = Course.query.filter_by(code=code).first()
        if existing:
            flash(f"Course code '{code}' already exists.", 'danger')
            return redirect(url_for('academic.courses'))

        c = Course(code=code, name=name, department=department, total_semesters=total_semesters)
        db.session.add(c)
        db.session.commit()
        log_activity('Add Course', 'Academic Management', f"Created course {c.code}: {c.name}")
        flash(f"Course '{c.name}' added successfully.", 'success')
        return redirect(url_for('academic.courses'))

    all_courses = Course.query.order_by(Course.code).all()
    return render_template('academic/courses.html', courses=all_courses)


@academic_bp.route('/courses/<int:course_id>/delete', methods=['POST'])
@admin_required
def delete_course(course_id):
    course = Course.query.get_or_404(course_id)
    if course.students.count() > 0:
        flash(f"Cannot delete course '{course.code}': {course.students.count()} students are enrolled.", 'danger')
        return redirect(url_for('academic.courses'))

    if course.examinations.count() > 0:
        flash(f"Cannot delete course '{course.code}': {course.examinations.count()} examinations are linked to this course.", 'danger')
        return redirect(url_for('academic.courses'))

    for subj in course.subjects:
        if subj.examinations.count() > 0:
            flash(f"Cannot delete course '{course.code}': Subject '{subj.code}' has scheduled examinations.", 'danger')
            return redirect(url_for('academic.courses'))

    code = course.code
    db.session.delete(course)
    db.session.commit()
    log_activity('Delete Course', 'Academic Management', f"Deleted course {code}")
    flash(f"Course '{code}' deleted.", 'warning')
    return redirect(url_for('academic.courses'))


@academic_bp.route('/courses/<int:course_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_course(course_id):
    course = Course.query.get_or_404(course_id)
    if request.method == 'POST':
        code = request.form.get('code', '').strip().upper()
        name = request.form.get('name', '').strip()
        department = request.form.get('department', '').strip()
        total_semesters = request.form.get('total_semesters', type=int) or course.total_semesters

        if not code or not name or not department:
            flash('All course fields are required.', 'danger')
            return redirect(url_for('academic.courses'))

        dup = Course.query.filter(Course.code == code, Course.id != course.id).first()
        if dup:
            flash(f"Course code '{code}' is already in use by another course.", 'danger')
            return render_template('academic/course_edit.html', course=course)

        course.code = code
        course.name = name
        course.department = department
        course.total_semesters = total_semesters
        db.session.commit()
        log_activity('Edit Course', 'Academic Management', f"Updated course {course.code}: {course.name}")
        flash(f"Course '{course.name}' updated successfully.", 'success')
        return redirect(url_for('academic.courses'))

    return render_template('academic/course_edit.html', course=course)


@academic_bp.route('/subjects', methods=['GET', 'POST'])
@admin_required
def subjects():
    courses_list = Course.query.order_by(Course.code).all()

    if request.method == 'POST':
        code = request.form.get('code', '').strip().upper()
        name = request.form.get('name', '').strip()
        course_id = request.form.get('course_id', type=int)
        semester = request.form.get('semester', type=int)
        credits = request.form.get('credits', type=int) or 4
        academic_year = request.form.get('academic_year', '2025-2026').strip()

        if not code or not name or not course_id or not semester:
            flash('All subject fields are mandatory.', 'danger')
            return redirect(url_for('academic.subjects'))

        course = Course.query.get(course_id)
        if not course:
            flash('Selected course is invalid.', 'danger')
            return redirect(url_for('academic.subjects'))

        if semester < 1 or semester > course.total_semesters:
            flash(f"Semester {semester} is invalid for course {course.code} (max: {course.total_semesters}).", 'danger')
            return redirect(url_for('academic.subjects'))

        existing = Subject.query.filter_by(code=code).first()
        if existing:
            flash(f"Subject code '{code}' already exists.", 'danger')
            return redirect(url_for('academic.subjects'))

        sub = Subject(
            code=code,
            name=name,
            course_id=course_id,
            semester=semester,
            credits=credits,
            academic_year=academic_year
        )
        db.session.add(sub)
        db.session.commit()
        log_activity('Add Subject', 'Academic Management', f"Created subject {sub.code} ({sub.name})")
        flash(f"Subject '{sub.name}' added successfully.", 'success')
        return redirect(url_for('academic.subjects'))

    course_filter = request.args.get('course_id', type=int)
    semester_filter = request.args.get('semester', type=int)

    query = Subject.query
    if course_filter:
        query = query.filter_by(course_id=course_filter)
    if semester_filter:
        query = query.filter_by(semester=semester_filter)

    all_subjects = query.order_by(Subject.course_id, Subject.semester, Subject.code).all()
    return render_template(
        'academic/subjects.html',
        subjects=all_subjects,
        courses=courses_list,
        course_filter=course_filter,
        semester_filter=semester_filter
    )


@academic_bp.route('/subjects/<int:subject_id>/delete', methods=['POST'])
@admin_required
def delete_subject(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    if subject.examinations.count() > 0:
        flash(f"Cannot delete subject '{subject.code}': Examinations are linked to it.", 'danger')
        return redirect(url_for('academic.subjects'))

    code = subject.code
    db.session.delete(subject)
    db.session.commit()
    log_activity('Delete Subject', 'Academic Management', f"Deleted subject {code}")
    flash(f"Subject '{code}' deleted.", 'warning')
    return redirect(url_for('academic.subjects'))


@academic_bp.route('/subjects/<int:subject_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_subject(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    courses_list = Course.query.order_by(Course.code).all()

    if request.method == 'POST':
        code = request.form.get('code', '').strip().upper()
        name = request.form.get('name', '').strip()
        course_id = request.form.get('course_id', type=int)
        semester = request.form.get('semester', type=int)
        credits = request.form.get('credits', type=int) or subject.credits
        academic_year = request.form.get('academic_year', '2025-2026').strip()

        if not code or not name or not course_id or not semester:
            flash('All subject fields are mandatory.', 'danger')
            return redirect(url_for('academic.subjects'))

        course = Course.query.get(course_id)
        if not course:
            flash('Selected course is invalid.', 'danger')
            return redirect(url_for('academic.subjects'))

        if semester < 1 or semester > course.total_semesters:
            flash(f"Semester {semester} is invalid for course {course.code} (max: {course.total_semesters}).", 'danger')
            return render_template('academic/subject_edit.html', subject=subject, courses=courses_list)

        dup = Subject.query.filter(Subject.code == code, Subject.id != subject.id).first()
        if dup:
            flash(f"Subject code '{code}' already exists.", 'danger')
            return render_template('academic/subject_edit.html', subject=subject, courses=courses_list)

        subject.code = code
        subject.name = name
        subject.course_id = course_id
        subject.semester = semester
        subject.credits = credits
        subject.academic_year = academic_year
        db.session.commit()
        log_activity('Edit Subject', 'Academic Management', f"Updated subject {subject.code} ({subject.name})")
        flash(f"Subject '{subject.name}' updated successfully.", 'success')
        return redirect(url_for('academic.subjects'))

    return render_template('academic/subject_edit.html', subject=subject, courses=courses_list)

