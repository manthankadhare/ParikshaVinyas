import pytest
from app.models.user import User
from app.models.student import Student
from app.models.hall import ExaminationHall
from app.models.academic import Course, Subject
from app import db


@pytest.fixture
def auth_client(client, test_db):
    """Client authenticated as administrator."""
    client.post('/login', data={'username': 'admin', 'password': 'Admin@2026'}, follow_redirects=True)
    return client


def test_student_creation_and_duplicate_validation(auth_client, test_db):
    course = Course.query.filter_by(code='CS').first()

    # Add student
    resp = auth_client.post('/admin/students/add', data={
        'enrollment_no': 'EN_TEST_001',
        'full_name': 'Candidate One',
        'email': 'cand1@test.com',
        'mobile': '9876543210',
        'course_id': course.id,
        'branch': 'Computer Science',
        'semester': 6,
        'division': 'A',
        'academic_year': '2025-2026',
        'status': 'Active'
    }, follow_redirects=True)

    assert resp.status_code == 200
    assert b"successfully added" in resp.data

    # Attempt duplicate enrollment
    resp_dup = auth_client.post('/admin/students/add', data={
        'enrollment_no': 'EN_TEST_001',
        'full_name': 'Candidate Duplicate',
        'email': 'cand_dup@test.com',
        'mobile': '9876543211',
        'course_id': course.id,
        'branch': 'Computer Science',
        'semester': 6,
        'division': 'A',
        'academic_year': '2025-2026',
        'status': 'Active'
    }, follow_redirects=True)

    assert b"already exists" in resp_dup.data


def test_hall_creation_and_blocking_seat(auth_client, test_db):
    resp = auth_client.post('/admin/halls/add', data={
        'hall_code': 'H-NEW-202',
        'hall_name': 'New Testing Hall',
        'building': 'Block D',
        'floor': '2nd',
        'num_rows': 4,
        'num_cols': 5,
        'status': 'Active'
    }, follow_redirects=True)

    assert resp.status_code == 200
    hall = ExaminationHall.query.filter_by(hall_code='H-NEW-202').first()
    assert hall is not None
    assert hall.total_capacity == 20

    # Toggle block seat
    resp_block = auth_client.post(f'/admin/halls/{hall.id}/toggle-seat', data={
        'row_num': 1,
        'col_num': 2,
        'reason': 'Broken desk leg'
    }, follow_redirects=True)

    assert resp_block.status_code == 200
    db.session.refresh(hall)
    assert hall.blocked_count == 1
    assert hall.usable_capacity == 19
