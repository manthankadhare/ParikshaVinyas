import pytest
from app.models.user import User
from app.models.student import Student
from app.models.academic import Course
from app import db


def test_admin_login_success(client, test_db):
    response = client.post('/login', data={
        'username': 'admin',
        'password': 'Admin@2026'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Welcome back, admin!" in response.data
    assert b"Examination Operations Overview" in response.data


def test_invalid_login_rejection(client, test_db):
    response = client.post('/login', data={
        'username': 'admin',
        'password': 'WrongPassword123'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Invalid username/enrollment number or password." in response.data


def test_student_login_and_portal_access(client, test_db):
    # Create student with user
    course = Course.query.filter_by(code='CS').first()
    user = User(username='en2026999', email='student999@test.com', role='student')
    user.set_password('Student@6999')
    db.session.add(user)
    db.session.flush()

    student = Student(
        user_id=user.id,
        enrollment_no='EN2026999',
        full_name='Portal Test Student',
        email='student999@test.com',
        mobile='9822123456',
        course_id=course.id,
        branch='CS',
        semester=6,
        division='A'
    )
    db.session.add(student)
    db.session.commit()

    # Log in using uppercase enrollment number
    response = client.post('/login', data={
        'username': 'EN2026999',
        'password': 'Student@6999'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Portal Test Student" in response.data
    assert b"My Examination Schedule" in response.data


def test_rbac_student_blocked_from_admin_dashboard(client, test_db):
    # Log in as student
    user = User(username='en_student', email='student@test.com', role='student')
    user.set_password('Pass@123')
    db.session.add(user)
    db.session.commit()

    client.post('/login', data={'username': 'en_student', 'password': 'Pass@123'}, follow_redirects=True)

    # Attempt to access admin dashboard
    response = client.get('/admin/dashboard')
    # Should be 403 Forbidden
    assert response.status_code == 403
