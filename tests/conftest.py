import pytest
from app import create_app, db
from config import TestConfig
from app.models.user import User
from app.models.academic import Course, Subject
from app.models.student import Student
from app.models.hall import ExaminationHall, BlockedSeat
from app.models.exam import Examination, EligibleStudent
from datetime import date, time


@pytest.fixture
def app():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


@pytest.fixture
def test_db(app):
    """Provides a fresh database session for unit tests."""
    # Seed essential records for testing
    admin = User(username='admin', email='admin@test.com', role='admin')
    admin.set_password('Admin@2026')
    db.session.add(admin)

    course = Course(code='CS', name='Computer Science', department='Dept of CS', total_semesters=8)
    db.session.add(course)
    db.session.flush()

    subject = Subject(code='CS601', name='Software Testing', course_id=course.id, semester=6, credits=4)
    db.session.add(subject)

    hall = ExaminationHall(
        hall_code='H-101', hall_name='Test Hall 101', building='Science Block', floor='1st',
        num_rows=5, num_cols=6, total_capacity=30, status='Active'
    )
    db.session.add(hall)
    db.session.flush()

    # Block 1 seat
    blocked = BlockedSeat(hall_id=hall.id, row_num=1, col_num=1, seat_identifier='H-101-R01-C01', reason='Damaged')
    db.session.add(blocked)

    db.session.commit()
    return db

