from flask import Blueprint, render_template, request
from sqlalchemy import func
from datetime import date
from app import db
from app.models.student import Student
from app.models.hall import ExaminationHall, BlockedSeat
from app.models.exam import Examination, EligibleStudent
from app.models.allocation import SeatAllocation
from app.models.academic import Course
from app.models.audit import ActivityLog
from app.utils.decorators import admin_required

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    # Counts
    total_students = Student.query.count()
    active_students = Student.query.filter_by(status='Active').count()
    total_halls = ExaminationHall.query.count()
    active_halls = ExaminationHall.query.filter_by(status='Active').all()

    total_gross_capacity = sum(h.total_capacity for h in active_halls)
    total_blocked_seats = sum(h.blocked_count for h in active_halls)
    total_usable_capacity = sum(h.usable_capacity for h in active_halls)

    total_exams = Examination.query.count()
    scheduled_exams = Examination.query.filter(Examination.status.in_(['Scheduled', 'Allocated'])).count()

    total_allocations = SeatAllocation.query.count()

    # Calculate overall allocation completion percentage
    total_eligible_slots = EligibleStudent.query.count()
    completion_percentage = round((total_allocations / total_eligible_slots * 100), 1) if total_eligible_slots > 0 else 0

    # Upcoming examinations
    upcoming_exams = Examination.query.filter(
        Examination.exam_date >= date.today()
    ).order_by(Examination.exam_date, Examination.start_time).limit(5).all()

    # Recent activity logs
    recent_activities = ActivityLog.query.order_by(ActivityLog.timestamp.desc()).limit(8).all()

    # Chart 1: Hall-wise seat utilization
    hall_labels = [h.hall_code for h in active_halls]
    hall_capacities = [h.total_capacity for h in active_halls]
    hall_usable = [h.usable_capacity for h in active_halls]
    hall_occupied = []
    for h in active_halls:
        occ = SeatAllocation.query.filter_by(hall_id=h.id).count()
        hall_occupied.append(occ)

    # Chart 2: Course-wise student distribution
    course_data = db.session.query(
        Course.code, func.count(Student.id)
    ).join(Student, Student.course_id == Course.id).group_by(Course.code).all()
    course_labels = [c[0] for c in course_data]
    course_counts = [c[1] for c in course_data]

    # Chart 3: Allocated vs Unallocated eligible students
    unallocated_count = max(0, total_eligible_slots - total_allocations)
    alloc_status_labels = ['Allocated Seats', 'Unallocated Candidates']
    alloc_status_values = [total_allocations, unallocated_count]

    return render_template(
        'dashboard/admin_dashboard.html',
        total_students=total_students,
        active_students=active_students,
        total_halls=total_halls,
        total_gross_capacity=total_gross_capacity,
        total_usable_capacity=total_usable_capacity,
        total_blocked_seats=total_blocked_seats,
        total_exams=total_exams,
        scheduled_exams=scheduled_exams,
        total_allocations=total_allocations,
        completion_percentage=completion_percentage,
        upcoming_exams=upcoming_exams,
        recent_activities=recent_activities,
        # Chart JSON-friendly data
        hall_labels=hall_labels,
        hall_capacities=hall_capacities,
        hall_usable=hall_usable,
        hall_occupied=hall_occupied,
        course_labels=course_labels,
        course_counts=course_counts,
        alloc_status_labels=alloc_status_labels,
        alloc_status_values=alloc_status_values
    )


@admin_bp.route('/activity-logs')
@admin_required
def activity_logs():
    page = request.args.get('page', 1, type=int)
    module_filter = request.args.get('module', '')

    query = ActivityLog.query
    if module_filter:
        query = query.filter_by(module=module_filter)

    logs_paginated = query.order_by(ActivityLog.timestamp.desc()).paginate(page=page, per_page=20, error_out=False)
    modules = db.session.query(ActivityLog.module).distinct().all()
    module_list = [m[0] for m in modules if m[0]]

    return render_template('dashboard/activity_logs.html', logs=logs_paginated, modules=module_list, selected_module=module_filter)

