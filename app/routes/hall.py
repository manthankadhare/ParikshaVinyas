from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from app import db
from app.models.hall import ExaminationHall, BlockedSeat
from app.models.allocation import SeatAllocation
from app.models.exam import Examination
from app.forms.hall_forms import HallForm, BlockSeatForm
from app.utils.decorators import admin_required
from app.services.audit_service import log_activity

hall_bp = Blueprint('hall', __name__)


@hall_bp.route('/')
@admin_required
def index():
    halls = ExaminationHall.query.order_by(ExaminationHall.hall_code).all()
    total_capacity = sum(h.total_capacity for h in halls)
    total_blocked = sum(h.blocked_count for h in halls)
    total_usable = sum(h.usable_capacity for h in halls)

    return render_template(
        'halls/index.html',
        halls=halls,
        total_capacity=total_capacity,
        total_blocked=total_blocked,
        total_usable=total_usable
    )


@hall_bp.route('/add', methods=['GET', 'POST'])
@admin_required
def add():
    form = HallForm()
    if form.validate_on_submit():
        code = form.hall_code.data.strip().upper()
        if ExaminationHall.query.filter_by(hall_code=code).first():
            flash(f"Hall code '{code}' already exists.", 'danger')
            return render_template('halls/form.html', form=form, title='Add Examination Hall')

        rows = form.num_rows.data
        cols = form.num_cols.data
        total_capacity = rows * cols

        hall = ExaminationHall(
            hall_code=code,
            hall_name=form.hall_name.data.strip(),
            building=form.building.data.strip(),
            floor=form.floor.data.strip(),
            num_rows=rows,
            num_cols=cols,
            total_capacity=total_capacity,
            status=form.status.data
        )
        db.session.add(hall)
        db.session.commit()
        log_activity('Add Hall', 'Hall Management', f"Created hall {hall.hall_code} ({hall.total_capacity} seats)")
        flash(f"Examination Hall '{hall.hall_code}' created with {total_capacity} seats capacity.", 'success')
        return redirect(url_for('hall.index'))

    return render_template('halls/form.html', form=form, title='Add Examination Hall')


@hall_bp.route('/<int:hall_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit(hall_id):
    hall = ExaminationHall.query.get_or_404(hall_id)
    form = HallForm(obj=hall)

    if form.validate_on_submit():
        code = form.hall_code.data.strip().upper()
        dup = ExaminationHall.query.filter(ExaminationHall.hall_code == code, ExaminationHall.id != hall.id).first()
        if dup:
            flash(f"Hall code '{code}' already exists.", 'danger')
            return render_template('halls/form.html', form=form, title='Edit Examination Hall', hall=hall)

        new_rows = form.num_rows.data
        new_cols = form.num_cols.data

        # Check if any existing blocked seats fall outside new dimensions
        invalid_blocked = hall.blocked_seats.filter(
            (BlockedSeat.row_num > new_rows) | (BlockedSeat.col_num > new_cols)
        ).first()
        if invalid_blocked:
            flash(f"Cannot resize hall to {new_rows}x{new_cols}: Blocked seat {invalid_blocked.seat_identifier} falls outside new dimensions.", 'danger')
            return render_template('halls/form.html', form=form, title='Edit Examination Hall', hall=hall)

        # Check if any existing seat allocations fall outside new dimensions
        invalid_alloc = hall.allocations.filter(
            (SeatAllocation.row_num > new_rows) | (SeatAllocation.col_num > new_cols)
        ).first()
        if invalid_alloc:
            flash(f"Cannot resize hall to {new_rows}x{new_cols}: Active seat allocation {invalid_alloc.seat_identifier} for exam '{invalid_alloc.examination.exam_code}' falls outside new dimensions.", 'danger')
            return render_template('halls/form.html', form=form, title='Edit Examination Hall', hall=hall)

        hall.hall_code = code
        hall.hall_name = form.hall_name.data.strip()
        hall.building = form.building.data.strip()
        hall.floor = form.floor.data.strip()
        hall.num_rows = new_rows
        hall.num_cols = new_cols
        hall.total_capacity = new_rows * new_cols
        hall.status = form.status.data

        db.session.commit()
        log_activity('Edit Hall', 'Hall Management', f"Updated hall {hall.hall_code} (Capacity: {hall.total_capacity})")
        flash(f"Hall '{hall.hall_code}' updated successfully.", 'success')
        return redirect(url_for('hall.index'))

    return render_template('halls/form.html', form=form, title='Edit Examination Hall', hall=hall)


@hall_bp.route('/<int:hall_id>/delete', methods=['POST'])
@admin_required
def delete(hall_id):
    hall = ExaminationHall.query.get_or_404(hall_id)
    if hall.allocations.count() > 0:
        flash(f"Cannot delete hall '{hall.hall_code}': Active examination allocations exist.", 'danger')
        return redirect(url_for('hall.index'))

    code = hall.hall_code
    db.session.delete(hall)
    db.session.commit()
    log_activity('Delete Hall', 'Hall Management', f"Deleted hall {code}")
    flash(f"Examination Hall '{code}' deleted.", 'warning')
    return redirect(url_for('hall.index'))


@hall_bp.route('/<int:hall_id>/layout')
@admin_required
def layout(hall_id):
    hall = ExaminationHall.query.get_or_404(hall_id)
    block_form = BlockSeatForm()
    blocked_seats_map = {(b.row_num, b.col_num): b for b in hall.blocked_seats.all()}

    return render_template(
        'halls/layout.html',
        hall=hall,
        block_form=block_form,
        blocked_seats_map=blocked_seats_map
    )


@hall_bp.route('/<int:hall_id>/toggle-seat', methods=['POST'])
@admin_required
def toggle_seat(hall_id):
    """API endpoint to block/unblock a seat in a hall."""
    hall = ExaminationHall.query.get_or_404(hall_id)
    data = request.get_json(silent=True) or {}

    if data:
        row = int(data.get('row', 0))
        col = int(data.get('col', 0))
        reason = data.get('reason') or 'Damaged desk / Maintenance'
    else:
        row = request.form.get('row_num', type=int)
        col = request.form.get('col_num', type=int)
        reason = request.form.get('reason') or 'Damaged desk / Maintenance'

    if not row or not col or row < 1 or row > hall.num_rows or col < 1 or col > hall.num_cols:
        if request.is_json:
            return jsonify({'success': False, 'message': 'Invalid row or column position.'}), 400
        flash('Invalid seat position.', 'danger')
        return redirect(url_for('hall.layout', hall_id=hall.id))

    ident = f"{hall.hall_code}-R{row:02d}-C{col:02d}"

    # Check if seat is currently allocated in an active upcoming examination
    active_alloc = SeatAllocation.query.join(Examination).filter(
        SeatAllocation.hall_id == hall.id,
        SeatAllocation.row_num == row,
        SeatAllocation.col_num == col,
        Examination.status.in_(['Scheduled', 'Allocated', 'In Progress'])
    ).first()
    if active_alloc:
        msg = f"Cannot block seat {ident}: Currently assigned to student {active_alloc.student.enrollment_no} in exam {active_alloc.examination.exam_code}."
        if request.is_json:
            return jsonify({'success': False, 'message': msg}), 409
        flash(msg, 'danger')
        return redirect(url_for('hall.layout', hall_id=hall.id))

    existing_block = BlockedSeat.query.filter_by(hall_id=hall.id, row_num=row, col_num=col).first()
    if existing_block:
        db.session.delete(existing_block)
        db.session.commit()
        log_activity('Unblock Seat', 'Hall Management', f"Unblocked seat {ident}")
        if request.is_json:
            return jsonify({'success': True, 'action': 'unblocked', 'message': f"Seat {ident} is now available."})
        flash(f"Seat {ident} unblocked.", 'success')
    else:
        new_block = BlockedSeat(hall_id=hall.id, row_num=row, col_num=col, seat_identifier=ident, reason=reason)
        db.session.add(new_block)
        db.session.commit()
        log_activity('Block Seat', 'Hall Management', f"Blocked seat {ident} (Reason: {reason})")
        if request.is_json:
            return jsonify({'success': True, 'action': 'blocked', 'message': f"Seat {ident} blocked."})
        flash(f"Seat {ident} blocked successfully.", 'warning')

    return redirect(url_for('hall.layout', hall_id=hall.id))
