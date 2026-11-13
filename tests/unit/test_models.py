import pytest
from app.models.user import User
from app.models.hall import ExaminationHall, BlockedSeat
from app.models.student import Student
from app.models.academic import Course, Subject
from app import db


def test_user_password_hashing(test_db):
    user = User(username='test_student', email='test@upluniversity.ac.in', role='student')
    user.set_password('Secret@123')
    db.session.add(user)
    db.session.commit()

    assert user.check_password('Secret@123') is True
    assert user.check_password('WrongPass') is False
    assert user.is_student() is True
    assert user.is_admin() is False


def test_hall_capacity_and_usable_calculation(test_db):
    hall = ExaminationHall.query.filter_by(hall_code='H-101').first()
    assert hall is not None
    assert hall.total_capacity == 30  # 5 rows * 6 cols
    assert hall.blocked_count == 1   # We added 1 blocked seat in fixture
    assert hall.usable_capacity == 29
    assert hall.is_seat_blocked(1, 1) is True
    assert hall.is_seat_blocked(1, 2) is False


def test_student_model_creation(test_db):
    course = Course.query.filter_by(code='CS').first()
    student = Student(
        enrollment_no='EN999001',
        full_name='Test Candidate',
        email='candidate@test.com',
        mobile='9876543210',
        course_id=course.id,
        branch='Computer Science',
        semester=6,
        division='A'
    )
    db.session.add(student)
    db.session.commit()

    retrieved = Student.query.filter_by(enrollment_no='EN999001').first()
    assert retrieved is not None
    assert retrieved.full_name == 'Test Candidate'
    assert retrieved.status == 'Active'

