import pytest
from datetime import date, time
from app.models.exam import Examination, EligibleStudent
from app.models.student import Student
from app.models.academic import Course, Subject
from app.models.hall import ExaminationHall
from app.services.allocation_engine import AllocationEngine
from app import db


@pytest.fixture
def auth_client(client, test_db):
    client.post('/login', data={'username': 'admin', 'password': 'Admin@2026'}, follow_redirects=True)
    return client


def test_pdf_report_generation(auth_client, test_db):
    course = Course.query.filter_by(code='CS').first()
    subject = Subject.query.filter_by(code='CS601').first()
    hall = ExaminationHall.query.filter_by(hall_code='H-101').first()

    exam = Examination(
        exam_code='EX-PDF-01',
        exam_name='PDF Test Exam',
        subject_id=subject.id,
        course_id=course.id,
        semester=6,
        exam_date=date(2026, 12, 5),
        start_time=time(10, 0),
        end_time=time(13, 0),
        duration_minutes=180,
        status='Scheduled'
    )
    db.session.add(exam)
    db.session.flush()

    student = Student(
        enrollment_no='EN_PDF_001',
        full_name='PDF Test Candidate',
        email='pdfcand@test.com',
        mobile='9822998877',
        course_id=course.id,
        branch='CS',
        semester=6,
        division='A'
    )
    db.session.add(student)
    db.session.flush()

    el = EligibleStudent(examination_id=exam.id, student_id=student.id)
    db.session.add(el)
    db.session.commit()

    # Allocate seat
    AllocationEngine.allocate_examination(exam.id, strategy='Sequential', hall_ids=[hall.id])

    # 1. Exam Allocation PDF
    resp1 = auth_client.get(f'/admin/reports/exam/{exam.id}/pdf')
    assert resp1.status_code == 200
    assert resp1.mimetype == 'application/pdf'
    assert resp1.data.startswith(b'%PDF')

    # 2. Student Seating Slip PDF
    resp2 = auth_client.get(f'/admin/reports/student/{student.id}/pdf')
    assert resp2.status_code == 200
    assert resp2.mimetype == 'application/pdf'
    assert resp2.data.startswith(b'%PDF')

    # 3. CSV Export
    resp3 = auth_client.get(f'/admin/reports/exam/{exam.id}/csv')
    assert resp3.status_code == 200
    assert resp3.mimetype == 'text/csv'
    assert b"Examination Code,Examination Name" in resp3.data

