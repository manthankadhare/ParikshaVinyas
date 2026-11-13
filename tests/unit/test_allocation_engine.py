import pytest
from datetime import date, time
from app import db
from app.models.exam import Examination, EligibleStudent
from app.models.student import Student
from app.models.hall import ExaminationHall, BlockedSeat
from app.models.academic import Course, Subject
from app.models.allocation import SeatAllocation
from app.services.allocation_engine import AllocationEngine


@pytest.fixture
def allocation_setup(test_db):
    """Sets up an examination with 10 students and a hall of 12 usable seats."""
    course = Course.query.filter_by(code='CS').first()
    subject = Subject.query.filter_by(code='CS601').first()
    hall = ExaminationHall.query.filter_by(hall_code='H-101').first()

    # Create exam
    exam = Examination(
        exam_code='EX-TEST-101',
        exam_name='Unit Test Exam',
        subject_id=subject.id,
        course_id=course.id,
        semester=6,
        exam_date=date(2026, 12, 1),
        start_time=time(10, 0),
        end_time=time(13, 0),
        duration_minutes=180,
        status='Scheduled'
    )
    db.session.add(exam)
    db.session.flush()

    # Create 10 students (5 Div A, 5 Div B)
    students = []
    for i in range(1, 11):
        div = 'A' if i <= 5 else 'B'
        st = Student(
            enrollment_no=f'EN_UT_{i:03d}',
            full_name=f'UT Student {i}',
            email=f'ut{i}@test.com',
            mobile=f'98000000{i:02d}',
            course_id=course.id,
            branch='CS',
            semester=6,
            division=div,
            status='Active'
        )
        db.session.add(st)
        db.session.flush()
        students.append(st)

        # Enroll in exam
        el = EligibleStudent(examination_id=exam.id, student_id=st.id)
        db.session.add(el)

    db.session.commit()
    return exam, hall, students


def test_sequential_allocation(allocation_setup):
    exam, hall, students = allocation_setup
    result = AllocationEngine.allocate_examination(exam.id, strategy='Sequential', hall_ids=[hall.id])

    assert result.success is True
    assert result.summary['total_allocated'] == 10
    assert result.summary['total_unallocated'] == 0

    # Verify allocations in database
    allocs = SeatAllocation.query.filter_by(examination_id=exam.id).all()
    assert len(allocs) == 10

    # Verify blocked seat R1-C1 was skipped
    blocked_alloc = SeatAllocation.query.filter_by(examination_id=exam.id, hall_id=hall.id, row_num=1, col_num=1).first()
    assert blocked_alloc is None


def test_random_allocation_reproducibility(allocation_setup):
    exam, hall, students = allocation_setup
    # Run with seed 42
    result1 = AllocationEngine.allocate_examination(exam.id, strategy='Random', hall_ids=[hall.id], seed=42, force_reallocate=True)
    assert result1.success is True

    seats_run1 = [a.seat_identifier for a in SeatAllocation.query.filter_by(examination_id=exam.id).order_by(SeatAllocation.student_id).all()]

    # Re-run with same seed
    result2 = AllocationEngine.allocate_examination(exam.id, strategy='Random', hall_ids=[hall.id], seed=42, force_reallocate=True)
    assert result2.success is True

    seats_run2 = [a.seat_identifier for a in SeatAllocation.query.filter_by(examination_id=exam.id).order_by(SeatAllocation.student_id).all()]

    assert seats_run1 == seats_run2


def test_capacity_overflow_boundary_rejection(allocation_setup):
    exam, hall, students = allocation_setup

    # Create a tiny hall with capacity of only 3 seats
    tiny_hall = ExaminationHall(
        hall_code='TINY-1',
        hall_name='Tiny Hall',
        building='East',
        floor='1',
        num_rows=1,
        num_cols=3,
        total_capacity=3,
        status='Active'
    )
    db.session.add(tiny_hall)
    db.session.commit()

    # Attempt allocation of 10 students into 3 seats
    result = AllocationEngine.allocate_examination(exam.id, strategy='Sequential', hall_ids=[tiny_hall.id])

    assert result.success is False
    assert "Insufficient seat capacity" in result.message
    assert result.summary['shortage'] == 7

    # Ensure atomic rollback: 0 allocations saved
    allocs = SeatAllocation.query.filter_by(examination_id=exam.id).count()
    assert allocs == 0


def test_manual_allocation_and_swap(allocation_setup):
    exam, hall, students = allocation_setup
    s1 = students[0]
    s2 = students[1]

    # Assign S1 to Row 2, Col 2
    res1 = AllocationEngine.manual_assign_or_swap(exam.id, s1.id, hall.id, 2, 2)
    assert res1.success is True

    # Assign S2 to Row 2, Col 3
    res2 = AllocationEngine.manual_assign_or_swap(exam.id, s2.id, hall.id, 2, 3)
    assert res2.success is True

    # Now assign S1 to Row 2, Col 3 (where S2 currently sits) -> Should perform automatic swap!
    res_swap = AllocationEngine.manual_assign_or_swap(exam.id, s1.id, hall.id, 2, 3)
    assert res_swap.success is True
    assert "Swapped seats" in res_swap.message

    # Verify S1 is now at R2C3, and S2 is now at R2C2
    alloc_s1 = SeatAllocation.query.filter_by(examination_id=exam.id, student_id=s1.id).first()
    alloc_s2 = SeatAllocation.query.filter_by(examination_id=exam.id, student_id=s2.id).first()

    assert alloc_s1.row_num == 2 and alloc_s1.col_num == 3
    assert alloc_s2.row_num == 2 and alloc_s2.col_num == 2

