from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from app import db
from app.models.exam import Examination, EligibleStudent
from app.models.hall import ExaminationHall, BlockedSeat
from app.models.student import Student
from app.models.allocation import SeatAllocation, AllocationHistory
from app.forms.exam_forms import AllocationWizardForm, ManualAllocationForm
from app.services.allocation_engine import AllocationEngine
from app.utils.decorators import admin_required
from app.services.audit_service import log_activity
from flask_login import current_user

allocation_bp = Blueprint('allocation', __name__)


@allocation_bp.route('/')
@admin_required
def index():
    exams = Examination.query.order_by(Examination.exam_date.desc()).all()
    recent_history = AllocationHistory.query.order_by(AllocationHistory.timestamp.desc()).limit(15).all()
    return render_template('allocation/index.html', exams=exams, history=recent_history)


@allocation_bp.route('/wizard', methods=['GET', 'POST'])
@admin_required
def wizard():
    form = AllocationWizardForm()
    exams = Examination.query.filter(Examination.status != 'Cancelled').order_by(Examination.exam_date.desc()).all()
    halls = ExaminationHall.query.filter_by(status='Active').order_by(ExaminationHall.hall_code).all()

    form.examination_id.choices = [(e.id, f"{e.exam_code} - {e.exam_name} ({e.eligible_count} students)") for e in exams]
    form.hall_ids.choices = [(h.id, f"{h.hall_code} ({h.usable_capacity}/{h.total_capacity} seats) - {h.building}") for h in halls]

    if form.validate_on_submit():
        exam_id = form.examination_id.data
        strategy = form.strategy.data
        hall_ids = form.hall_ids.data or None
        seed = form.random_seed.data if strategy == 'Random' else None
        force_realloc = form.force_reallocate.data

        result = AllocationEngine.allocate_examination(
            examination_id=exam_id,
            strategy=strategy,
            hall_ids=hall_ids,
            seed=seed,
            user_id=current_user.id,
            force_reallocate=force_realloc
        )

        if result.success:
            flash(result.message, 'success')
            log_activity('Auto Seat Allocation', 'Allocation Engine', f"Ran {strategy} allocation for exam ID {exam_id}")
            return render_template('allocation/summary.html', result=result, exam=Examination.query.get(exam_id))
        else:
            flash(result.message, 'danger')
            return render_template('allocation/wizard.html', form=form, exams=exams, halls=halls, error_summary=result.summary)

    # Pre-select exam if passed via query string
    pre_exam_id = request.args.get('exam_id', type=int)
    if pre_exam_id:
        form.examination_id.data = pre_exam_id

    return render_template('allocation/wizard.html', form=form, exams=exams, halls=halls)


@allocation_bp.route('/manual', methods=['GET', 'POST'])
@admin_required
def manual():
    form = ManualAllocationForm()
    exams = Examination.query.order_by(Examination.exam_date.desc()).all()
    halls = ExaminationHall.query.filter_by(status='Active').order_by(ExaminationHall.hall_code).all()

    form.examination_id.choices = [(e.id, f"{e.exam_code} - {e.exam_name}") for e in exams]
    form.hall_id.choices = [(h.id, f"{h.hall_code} ({h.hall_name})") for h in halls]

    selected_exam_id = (
        request.form.get('examination_id', type=int)
        or request.args.get('exam_id', type=int)
        or (exams[0].id if exams else None)
    )
    if selected_exam_id:
        exam = Examination.query.get(selected_exam_id)
        if exam:
            eligible_ids = [el.student_id for el in exam.eligible_students.all()]
            students = Student.query.filter(Student.id.in_(eligible_ids)).order_by(Student.enrollment_no).all()
            form.student_id.choices = [(s.id, f"{s.enrollment_no} - {s.full_name}") for s in students]
        else:
            form.student_id.choices = []
    else:
        form.student_id.choices = []

    if form.validate_on_submit():
        result = AllocationEngine.manual_assign_or_swap(
            examination_id=form.examination_id.data,
            student_id=form.student_id.data,
            target_hall_id=form.hall_id.data,
            target_row=form.row_num.data,
            target_col=form.col_num.data,
            user_id=current_user.id
        )
        if result.success:
            flash(result.message, 'success')
            log_activity('Manual Seat Allocation', 'Allocation Engine', result.message)
            return redirect(url_for('allocation.visual_grid', exam_id=form.examination_id.data, hall_id=form.hall_id.data))
        else:
            flash(result.message, 'danger')

    return render_template('allocation/manual.html', form=form, exams=exams, halls=halls, selected_exam_id=selected_exam_id)


@allocation_bp.route('/visual-grid')
@admin_required
def visual_grid():
    exams = Examination.query.order_by(Examination.exam_date.desc()).all()
    halls = ExaminationHall.query.filter_by(status='Active').order_by(ExaminationHall.hall_code).all()

    exam_id = request.args.get('exam_id', type=int)
    hall_id = request.args.get('hall_id', type=int)

    selected_exam = Examination.query.get(exam_id) if exam_id else (exams[0] if exams else None)
    selected_hall = ExaminationHall.query.get(hall_id) if hall_id else (halls[0] if halls else None)

    grid_data = []
    blocked_count = 0
    allocated_count = 0
    available_count = 0

    if selected_hall:
        # Load blocked seats
        blocked_map = {(b.row_num, b.col_num): b.reason for b in selected_hall.blocked_seats.all()}

        # Load seat allocations for selected exam in this hall
        alloc_map = {}
        if selected_exam:
            allocs = SeatAllocation.query.filter_by(
                examination_id=selected_exam.id,
                hall_id=selected_hall.id
            ).all()
            for a in allocs:
                alloc_map[(a.row_num, a.col_num)] = a

        for r in range(1, selected_hall.num_rows + 1):
            row_cells = []
            for c in range(1, selected_hall.num_cols + 1):
                seat_ident = f"{selected_hall.hall_code}-R{r:02d}-C{c:02d}"
                if (r, c) in blocked_map:
                    blocked_count += 1
                    row_cells.append({
                        'row': r,
                        'col': c,
                        'ident': seat_ident,
                        'status': 'blocked',
                        'reason': blocked_map[(r, c)],
                        'student': None
                    })
                elif (r, c) in alloc_map:
                    allocated_count += 1
                    a = alloc_map[(r, c)]
                    row_cells.append({
                        'row': r,
                        'col': c,
                        'ident': seat_ident,
                        'status': 'allocated',
                        'strategy': a.strategy_used,
                        'student': {
                            'id': a.student.id,
                            'enrollment': a.student.enrollment_no,
                            'name': a.student.full_name,
                            'course': a.student.course.code,
                            'div': a.student.division
                        }
                    })
                else:
                    available_count += 1
                    row_cells.append({
                        'row': r,
                        'col': c,
                        'ident': seat_ident,
                        'status': 'available',
                        'student': None
                    })
            grid_data.append(row_cells)

    return render_template(
        'allocation/visual_grid.html',
        exams=exams,
        halls=halls,
        selected_exam=selected_exam,
        selected_hall=selected_hall,
        grid_data=grid_data,
        blocked_count=blocked_count,
        allocated_count=allocated_count,
        available_count=available_count
    )


@allocation_bp.route('/<int:exam_id>/clear', methods=['POST'])
@admin_required
def clear(exam_id):
    exam = Examination.query.get_or_404(exam_id)
    count = exam.allocations.count()
    if count == 0:
        flash("No allocations to clear for this examination.", 'info')
        return redirect(url_for('allocation.index'))

    exam.allocations.delete()
    exam.status = 'Scheduled'

    hist = AllocationHistory(
        examination_id=exam.id,
        action='Cleared',
        details=f"Cleared all {count} allocations for exam {exam.exam_code}.",
        performed_by_id=current_user.id
    )
    db.session.add(hist)
    db.session.commit()

    log_activity('Clear Allocations', 'Allocation Engine', f"Cleared {count} seat allocations for {exam.exam_code}")
    flash(f"Successfully cleared all {count} allocations for {exam.exam_name}.", 'warning')
    return redirect(url_for('allocation.index'))

