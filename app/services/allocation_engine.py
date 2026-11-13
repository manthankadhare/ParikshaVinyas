import random
from datetime import datetime
from sqlalchemy import and_, or_
from app import db
from app.models.exam import Examination, EligibleStudent
from app.models.hall import ExaminationHall, BlockedSeat
from app.models.student import Student
from app.models.allocation import SeatAllocation, AllocationHistory


class AllocationEngineError(Exception):
    """Custom exception raised when allocation encounters business rule violations."""
    pass


class AllocationResult:
    def __init__(self, success, message, summary=None, details=None):
        self.success = success
        self.message = message
        self.summary = summary or {}
        self.details = details or []


class AllocationEngine:
    """
    Intelligent Seat Allocation Engine for ParikshaVinyas.
    Supports:
      1. Sequential Allocation (by enrollment number)
      2. Random Allocation (with reproducible seed support)
      3. Mixed Course / Division Interleaved Allocation
    """

    @staticmethod
    def get_available_seats_for_hall(hall_id, exam, exclude_occupied_in_overlapping_exams=True):
        """
        Calculates all physically available, unblocked, and conflict-free seats for a given hall.
        Returns list of seat dicts: [{'row': r, 'col': c, 'identifier': '...'}]
        """
        hall = ExaminationHall.query.get(hall_id)
        if not hall or hall.status != 'Active':
            return []

        # Get blocked seats for this hall
        blocked = BlockedSeat.query.filter_by(hall_id=hall_id).all()
        blocked_set = {(b.row_num, b.col_num) for b in blocked}

        # Check for overlapping examinations in the same hall on the same date/time
        occupied_seats = set()
        if exclude_occupied_in_overlapping_exams:
            # Overlapping exams: same date, and (start_time < exam.end_time and end_time > exam.start_time)
            overlapping_allocs = db.session.query(
                SeatAllocation.row_num, SeatAllocation.col_num
            ).join(Examination).filter(
                Examination.id != exam.id,
                Examination.exam_date == exam.exam_date,
                Examination.status != 'Cancelled',
                SeatAllocation.hall_id == hall_id,
                and_(
                    Examination.start_time < exam.end_time,
                    Examination.end_time > exam.start_time
                )
            ).all()
            for r, c in overlapping_allocs:
                occupied_seats.add((r, c))

        available = []
        for r in range(1, hall.num_rows + 1):
            for c in range(1, hall.num_cols + 1):
                if (r, c) not in blocked_set and (r, c) not in occupied_seats:
                    available.append({
                        'hall_id': hall.id,
                        'hall_code': hall.hall_code,
                        'hall_name': hall.hall_name,
                        'row': r,
                        'col': c,
                        'seat_identifier': f"{hall.hall_code}-R{r:02d}-C{c:02d}"
                    })
        return available

    @classmethod
    def allocate_examination(cls, examination_id, strategy='Sequential', hall_ids=None, seed=None, user_id=None, force_reallocate=False):
        """
        Executes atomic seat allocation for an examination.
        """
        exam = Examination.query.get(examination_id)
        if not exam:
            return AllocationResult(False, f"Examination with ID {examination_id} does not exist.")

        if exam.status == 'Cancelled':
            return AllocationResult(False, "Cannot allocate seats for a cancelled examination.")

        # Check existing allocations
        existing_allocations_count = SeatAllocation.query.filter_by(examination_id=exam.id).count()
        if existing_allocations_count > 0 and not force_reallocate:
            return AllocationResult(
                False,
                f"Examination already has {existing_allocations_count} seat allocations. "
                "Confirm regeneration to clear and re-allocate."
            )

        # Fetch eligible students
        eligible_entries = EligibleStudent.query.filter_by(examination_id=exam.id).all()
        student_ids = [e.student_id for e in eligible_entries]

        if not student_ids:
            return AllocationResult(False, "No eligible students registered for this examination.")

        students = Student.query.filter(Student.id.in_(student_ids), Student.status == 'Active').all()
        if len(students) < len(student_ids):
            inactive_diff = len(student_ids) - len(students)
            # Some students are inactive or detained
            pass

        if not students:
            return AllocationResult(False, "All registered students for this examination are inactive or detained.")

        # Determine target halls
        if hall_ids:
            halls = ExaminationHall.query.filter(
                ExaminationHall.id.in_(hall_ids),
                ExaminationHall.status == 'Active'
            ).order_by(ExaminationHall.hall_code).all()
        else:
            halls = ExaminationHall.query.filter_by(status='Active').order_by(ExaminationHall.hall_code).all()

        if not halls:
            return AllocationResult(False, "No active examination halls are available for allocation.")

        # Gather all usable seats across specified halls
        all_usable_seats = []
        for hall in halls:
            hall_seats = cls.get_available_seats_for_hall(hall.id, exam)
            all_usable_seats.extend(hall_seats)

        total_students = len(students)
        total_usable_capacity = len(all_usable_seats)

        if total_usable_capacity < total_students:
            return AllocationResult(
                False,
                f"Insufficient seat capacity: Required {total_students} seats, but only {total_usable_capacity} "
                f"available across {len(halls)} selected hall(s). Please select more halls or unblock seats.",
                summary={
                    'required_seats': total_students,
                    'available_seats': total_usable_capacity,
                    'shortage': total_students - total_usable_capacity,
                    'halls_considered': len(halls)
                }
            )

        # Clear existing allocations only AFTER validating capacity
        if existing_allocations_count > 0 and force_reallocate:
            SeatAllocation.query.filter_by(examination_id=exam.id).delete()
            hist = AllocationHistory(
                examination_id=exam.id,
                action='Reset & Clear',
                details=f"Cleared {existing_allocations_count} previous allocations before re-running {strategy} allocation.",
                performed_by_id=user_id
            )
            db.session.add(hist)
            db.session.flush()

        # Apply Allocation Strategy
        allocated_records = []
        student_seat_pairs = []

        try:
            if strategy == 'Sequential':
                student_seat_pairs = cls._apply_sequential(students, all_usable_seats)
            elif strategy == 'Random':
                student_seat_pairs = cls._apply_random(students, all_usable_seats, seed=seed)
            elif strategy == 'Mixed Course':
                student_seat_pairs = cls._apply_mixed_course(students, all_usable_seats)
            else:
                return AllocationResult(False, f"Unsupported allocation strategy: {strategy}")

            # Persist allocations inside transaction
            now = datetime.utcnow()
            for student, seat in student_seat_pairs:
                alloc = SeatAllocation(
                    examination_id=exam.id,
                    student_id=student.id,
                    hall_id=seat['hall_id'],
                    row_num=seat['row'],
                    col_num=seat['col'],
                    seat_identifier=seat['seat_identifier'],
                    strategy_used=strategy,
                    allocated_at=now,
                    allocated_by_id=user_id
                )
                db.session.add(alloc)
                allocated_records.append(alloc)

            exam.status = 'Allocated'

            # Record history
            halls_used_set = {seat['hall_id'] for _, seat in student_seat_pairs}
            hist = AllocationHistory(
                examination_id=exam.id,
                action='Auto-Allocated',
                details=f"Successfully allocated {len(student_seat_pairs)} students across {len(halls_used_set)} halls using '{strategy}' strategy.",
                performed_by_id=user_id,
                timestamp=now
            )
            db.session.add(hist)
            db.session.commit()

            summary = {
                'total_eligible': total_students,
                'total_allocated': len(student_seat_pairs),
                'total_unallocated': 0,
                'halls_used': len(halls_used_set),
                'total_capacity_available': total_usable_capacity,
                'remaining_seats': total_usable_capacity - len(student_seat_pairs),
                'strategy': strategy,
                'timestamp': now.strftime('%Y-%m-%d %H:%M:%S')
            }

            return AllocationResult(
                True,
                f"Successfully allocated {len(student_seat_pairs)} students using {strategy} strategy.",
                summary=summary
            )

        except Exception as e:
            db.session.rollback()
            return AllocationResult(False, f"Database transaction failed during seat allocation: {str(e)}")

    @staticmethod
    def _apply_sequential(students, seats):
        """
        Sort students by enrollment number and assign sequentially to ordered seats.
        """
        sorted_students = sorted(students, key=lambda s: s.enrollment_no)
        pairs = []
        for idx, student in enumerate(sorted_students):
            pairs.append((student, seats[idx]))
        return pairs

    @staticmethod
    def _apply_random(students, seats, seed=None):
        """
        Shuffle students randomly using reproducible seed if provided and assign to seats.
        """
        shuffled_students = list(students)
        rng = random.Random(seed) if seed is not None else random.Random()
        rng.shuffle(shuffled_students)

        pairs = []
        for idx, student in enumerate(shuffled_students):
            pairs.append((student, seats[idx]))
        return pairs

    @classmethod
    def _apply_mixed_course(cls, students, seats):
        """
        Groups students by (course_id, division, branch), and distributes them in round-robin /
        checkerboard fashion across adjacent seats to avoid seating peers together.
        """
        from collections import defaultdict
        groups = defaultdict(list)
        for s in students:
            # Group key based on course & division
            key = (s.course_id, s.division)
            groups[key].append(s)

        # Sort each group by enrollment
        for k in groups:
            groups[k].sort(key=lambda s: s.enrollment_no)

        group_keys = list(groups.keys())
        # Interleave groups round-robin
        interleaved_students = []
        max_group_size = max(len(grp) for grp in groups.values()) if groups else 0

        for i in range(max_group_size):
            for k in group_keys:
                if i < len(groups[k]):
                    interleaved_students.append(groups[k][i])

        pairs = []
        for idx, student in enumerate(interleaved_students):
            pairs.append((student, seats[idx]))
        return pairs

    @classmethod
    def manual_assign_or_swap(cls, examination_id, student_id, target_hall_id, target_row, target_col, user_id=None):
        """
        Manually assign a student to a specific seat, or reassign/swap if already assigned.
        Strictly validates:
          - Target seat is not blocked
          - Student belongs to eligible list for this exam
          - If target seat is occupied, handles swap or error
        """
        exam = Examination.query.get(examination_id)
        if not exam:
            return AllocationResult(False, "Examination does not exist.")

        student = Student.query.get(student_id)
        if not student or student.status != 'Active':
            return AllocationResult(False, "Invalid or inactive student.")

        # Check student eligibility
        is_eligible = EligibleStudent.query.filter_by(examination_id=exam.id, student_id=student.id).first()
        if not is_eligible:
            return AllocationResult(False, f"Student {student.enrollment_no} is not eligible for examination {exam.exam_code}.")

        hall = ExaminationHall.query.get(target_hall_id)
        if not hall or hall.status != 'Active':
            return AllocationResult(False, "Target examination hall is invalid or inactive.")

        # Validate row & col boundaries
        if target_row < 1 or target_row > hall.num_rows or target_col < 1 or target_col > hall.num_cols:
            return AllocationResult(False, f"Seat position R{target_row}-C{target_col} is out of hall bounds ({hall.num_rows}x{hall.num_cols}).")

        # Validate blocked seat
        if hall.is_seat_blocked(target_row, target_col):
            return AllocationResult(False, f"Seat R{target_row}-C{target_col} in Hall {hall.hall_code} is blocked / damaged.")

        # Check overlapping exam seat conflict
        overlap_conflict = db.session.query(SeatAllocation).join(Examination).filter(
            Examination.id != exam.id,
            Examination.exam_date == exam.exam_date,
            Examination.status != 'Cancelled',
            SeatAllocation.hall_id == target_hall_id,
            SeatAllocation.row_num == target_row,
            SeatAllocation.col_num == target_col,
            and_(
                Examination.start_time < exam.end_time,
                Examination.end_time > exam.start_time
            )
        ).first()
        if overlap_conflict:
            return AllocationResult(False, f"Seat R{target_row}-C{target_col} is already in use by overlapping exam '{overlap_conflict.examination.exam_name}'.")

        target_identifier = f"{hall.hall_code}-R{target_row:02d}-C{target_col:02d}"

        try:
            # Check if student currently has an allocation in this exam
            current_student_alloc = SeatAllocation.query.filter_by(examination_id=exam.id, student_id=student.id).first()

            # Check if target seat is currently occupied in this exam
            target_seat_alloc = SeatAllocation.query.filter_by(
                examination_id=exam.id,
                hall_id=target_hall_id,
                row_num=target_row,
                col_num=target_col
            ).first()

            now = datetime.utcnow()

            if target_seat_alloc and target_seat_alloc.student_id == student.id:
                return AllocationResult(True, "Student is already assigned to this seat.", summary={'action': 'None'})

            if target_seat_alloc:
                # Seat is occupied by another student! Perform SWAP if current student has a seat
                other_student = target_seat_alloc.student
                if current_student_alloc:
                    # Both students have seats: Swap their seats!
                    old_hall_id = current_student_alloc.hall_id
                    old_row = current_student_alloc.row_num
                    old_col = current_student_alloc.col_num
                    old_ident = current_student_alloc.seat_identifier

                    # Temporarily vacate target seat to avoid unique constraint collision
                    target_seat_alloc.row_num = -target_seat_alloc.id
                    db.session.flush()

                    current_student_alloc.hall_id = target_hall_id
                    current_student_alloc.row_num = target_row
                    current_student_alloc.col_num = target_col
                    current_student_alloc.seat_identifier = target_identifier
                    current_student_alloc.strategy_used = 'Manual Swap'
                    current_student_alloc.allocated_by_id = user_id
                    current_student_alloc.allocated_at = now
                    db.session.flush()

                    target_seat_alloc.hall_id = old_hall_id
                    target_seat_alloc.row_num = old_row
                    target_seat_alloc.col_num = old_col
                    target_seat_alloc.seat_identifier = old_ident
                    target_seat_alloc.strategy_used = 'Manual Swap'
                    target_seat_alloc.allocated_by_id = user_id
                    target_seat_alloc.allocated_at = now

                    hist = AllocationHistory(
                        examination_id=exam.id,
                        student_id=student.id,
                        action='Manual Seat Swap',
                        details=f"Swapped seats between {student.enrollment_no} ({target_identifier}) and {other_student.enrollment_no} ({old_ident}).",
                        performed_by_id=user_id,
                        timestamp=now
                    )
                    db.session.add(hist)
                    db.session.commit()
                    return AllocationResult(True, f"Swapped seats between {student.full_name} and {other_student.full_name}.")
                else:
                    return AllocationResult(False, f"Seat {target_identifier} is currently occupied by {other_student.enrollment_no}. Please clear or reassign that student first.")

            # Target seat is free!
            if current_student_alloc:
                # Move current student
                old_ident = current_student_alloc.seat_identifier
                current_student_alloc.hall_id = target_hall_id
                current_student_alloc.row_num = target_row
                current_student_alloc.col_num = target_col
                current_student_alloc.seat_identifier = target_identifier
                current_student_alloc.strategy_used = 'Manual Reassign'
                current_student_alloc.allocated_by_id = user_id
                current_student_alloc.allocated_at = now

                hist = AllocationHistory(
                    examination_id=exam.id,
                    student_id=student.id,
                    action='Manual Reassignment',
                    details=f"Moved student {student.enrollment_no} from {old_ident} to {target_identifier}.",
                    performed_by_id=user_id,
                    timestamp=now
                )
                db.session.add(hist)
            else:
                # Fresh manual allocation
                new_alloc = SeatAllocation(
                    examination_id=exam.id,
                    student_id=student.id,
                    hall_id=target_hall_id,
                    row_num=target_row,
                    col_num=target_col,
                    seat_identifier=target_identifier,
                    strategy_used='Manual',
                    allocated_at=now,
                    allocated_by_id=user_id
                )
                db.session.add(new_alloc)
                hist = AllocationHistory(
                    examination_id=exam.id,
                    student_id=student.id,
                    action='Manual Allocation',
                    details=f"Manually assigned {student.enrollment_no} to {target_identifier}.",
                    performed_by_id=user_id,
                    timestamp=now
                )
                db.session.add(hist)

            if exam.status == 'Scheduled':
                exam.status = 'Allocated'

            db.session.commit()
            return AllocationResult(True, f"Assigned {student.full_name} ({student.enrollment_no}) to seat {target_identifier}.")

        except Exception as e:
            db.session.rollback()
            return AllocationResult(False, f"Error updating seat allocation: {str(e)}")

    @classmethod
    def remove_allocation(cls, examination_id, student_id, user_id=None):
        """Remove a student's seat allocation."""
        alloc = SeatAllocation.query.filter_by(examination_id=examination_id, student_id=student_id).first()
        if not alloc:
            return AllocationResult(False, "Allocation not found.")

        try:
            ident = alloc.seat_identifier
            enrollment = alloc.student.enrollment_no
            db.session.delete(alloc)
            db.session.flush()

            # If no allocations remain for this exam, reset status to Scheduled
            remaining = SeatAllocation.query.filter_by(examination_id=examination_id).count()
            if remaining == 0:
                exam = Examination.query.get(examination_id)
                if exam and exam.status == 'Allocated':
                    exam.status = 'Scheduled'

            hist = AllocationHistory(
                examination_id=examination_id,
                student_id=student_id,
                action='Manual Removal',
                details=f"Removed allocation {ident} for student {enrollment}.",
                performed_by_id=user_id
            )
            db.session.add(hist)
            db.session.commit()
            return AllocationResult(True, f"Successfully removed seat allocation {ident} for {enrollment}.")
        except Exception as e:
            db.session.rollback()
            return AllocationResult(False, f"Error deleting allocation: {str(e)}")
