"""
STQA Defect Regression Test Suite — ParikshaVinyas
Comprehensive automated regression tests verifying all 12 identified, reproduced,
and remediated defects across business logic, security, database integrity, and UI workflows.
"""
import io
import pytest
from datetime import date, time, datetime
from flask import url_for
from app import db
from app.models.user import User
from app.models.academic import Course, Subject
from app.models.student import Student
from app.models.hall import ExaminationHall, BlockedSeat
from app.models.exam import Examination, EligibleStudent
from app.models.allocation import SeatAllocation
from app.models.invigilator import Invigilator, InvigilatorAssignment
from app.services.allocation_engine import AllocationEngine


def login_user_helper(client, username, password):
    return client.post('/login', data={'username': username, 'password': password}, follow_redirects=True)


# =========================================================================
# Defect 1: Scheduling Conflict on Exam Edit
# =========================================================================
def test_defect_1_exam_edit_schedule_conflict(client, test_db):
    login_user_helper(client, 'admin', 'Admin@2026')
    course = Course.query.filter_by(code='CS').first()
    subj = Subject.query.filter_by(code='CS601').first()

    # Exam 1: 10:00 to 12:00
    exam1 = Examination(
        exam_code='EX-REG-101', exam_name='Exam One', course_id=course.id, subject_id=subj.id,
        semester=6, exam_date=date(2026, 12, 10), start_time=time(10, 0), end_time=time(12, 0),
        duration_minutes=120, status='Scheduled'
    )
    # Exam 2: 14:00 to 16:00
    exam2 = Examination(
        exam_code='EX-REG-102', exam_name='Exam Two', course_id=course.id, subject_id=subj.id,
        semester=6, exam_date=date(2026, 12, 10), start_time=time(14, 0), end_time=time(16, 0),
        duration_minutes=120, status='Scheduled'
    )
    db.session.add_all([exam1, exam2])
    db.session.commit()

    # Attempt to edit Exam 2 to overlap with Exam 1 (11:00 to 13:00 on same date, course, sem)
    res = client.post(f'/admin/exams/{exam2.id}/edit', data={
        'exam_code': 'EX-REG-102',
        'exam_name': 'Exam Two',
        'course_id': course.id,
        'subject_id': subj.id,
        'semester': 6,
        'exam_date': '2026-12-10',
        'start_time': '11:00',
        'end_time': '13:00',
        'duration_minutes': 120,
        'exam_type': 'Regular',
        'academic_year': '2025-2026',
        'status': 'Scheduled'
    }, follow_redirects=True)

    assert b"Scheduling Conflict" in res.data
    # Verify exam2 start time was NOT updated in DB
    refreshed_exam2 = Examination.query.get(exam2.id)
    assert refreshed_exam2.start_time == time(14, 0)


# =========================================================================
# Defect 2: In-Batch Duplicate Enrollment & Email in CSV Import
# =========================================================================
def test_defect_2_csv_import_inbatch_duplicates(client, test_db):
    login_user_helper(client, 'admin', 'Admin@2026')
    course = Course.query.filter_by(code='CS').first()

    # CSV containing:
    # 1. Valid Student 1
    # 2. Duplicate Student 1 (same enrollment in batch)
    # 3. Duplicate email with different enrollment
    # 4. Valid Student 2
    csv_content = (
        "Enrollment Number,Full Name,Email,Mobile,Course Code,Semester,Division\n"
        "STQA-001,Student One,stqa1@test.com,9876543210,CS,6,A\n"
        "STQA-001,Student One Duplicate,stqa_dup@test.com,9876543211,CS,6,A\n"
        "STQA-002,Student Two,stqa1@test.com,9876543212,CS,6,A\n"
        "STQA-003,Student Three,stqa3@test.com,9876543213,CS,6,A\n"
    )

    data = {
        'csv_file': (io.BytesIO(csv_content.encode('utf-8')), 'test_students.csv')
    }
    res = client.post('/admin/students/import', data=data, content_type='multipart/form-data', follow_redirects=True)

    # Valid students 1 and 3 should be successfully imported
    assert b"Successfully added 2 students" in res.data
    assert Student.query.filter_by(enrollment_no='STQA-001').first() is not None
    assert Student.query.filter_by(enrollment_no='STQA-003').first() is not None
    # Duplicate enrollment STQA-001 and duplicate email stqa1@test.com should have been skipped
    assert Student.query.filter_by(enrollment_no='STQA-002').first() is None


# =========================================================================
# Defect 3: Hall Truncation Out-of-Bounds Allocation Protection
# =========================================================================
def test_defect_3_hall_edit_out_of_bounds_allocation(client, test_db):
    login_user_helper(client, 'admin', 'Admin@2026')
    hall = ExaminationHall.query.filter_by(hall_code='H-101').first()
    course = Course.query.filter_by(code='CS').first()
    subj = Subject.query.filter_by(code='CS601').first()

    exam = Examination(
        exam_code='EX-HALL-101', exam_name='Hall Test Exam', course_id=course.id, subject_id=subj.id,
        semester=6, exam_date=date(2026, 12, 12), start_time=time(10, 0), end_time=time(13, 0),
        duration_minutes=180, status='Allocated'
    )
    db.session.add(exam)
    db.session.flush()

    student = Student(
        enrollment_no='EN-HALL-01', full_name='Hall Student', email='hallst@test.com',
        mobile='9876543210', course_id=course.id, branch='CS', semester=6, division='A', status='Active'
    )
    db.session.add(student)
    db.session.flush()

    # Assign student to row 5, col 6
    alloc = SeatAllocation(
        examination_id=exam.id, student_id=student.id, hall_id=hall.id, row_num=5, col_num=6,
        seat_identifier='H-101-R05-C06', strategy_used='Manual'
    )
    db.session.add(alloc)
    db.session.commit()

    # Attempt to resize hall to 4 rows x 5 cols (truncating row 5 col 6)
    res = client.post(f'/admin/halls/{hall.id}/edit', data={
        'hall_code': 'H-101',
        'hall_name': hall.hall_name,
        'building': hall.building,
        'floor': hall.floor,
        'num_rows': 4,
        'num_cols': 5,
        'status': 'Active'
    }, follow_redirects=True)

    assert b"Cannot resize hall" in res.data
    assert b"Active seat allocation" in res.data
    # Verify hall dimensions were NOT truncated
    refreshed_hall = ExaminationHall.query.get(hall.id)
    assert refreshed_hall.num_rows == 5
    assert refreshed_hall.num_cols == 6


# =========================================================================
# Defect 4: Course Deletion Referential Integrity Protection
# =========================================================================
def test_defect_4_course_delete_with_linked_exams(client, test_db):
    login_user_helper(client, 'admin', 'Admin@2026')
    course = Course(code='EE', name='Electrical Engineering', department='EE Dept', total_semesters=8)
    db.session.add(course)
    db.session.flush()

    subj = Subject(code='EE201', name='Circuits', course_id=course.id, semester=2, credits=4)
    db.session.add(subj)
    db.session.flush()

    exam = Examination(
        exam_code='EX-EE-201', exam_name='Circuits Exam', course_id=course.id, subject_id=subj.id,
        semester=2, exam_date=date(2026, 12, 15), start_time=time(10, 0), end_time=time(13, 0),
        duration_minutes=180, status='Scheduled'
    )
    db.session.add(exam)
    db.session.commit()

    # Course has 0 students enrolled, but has scheduled examinations
    res = client.post(f'/admin/academic/courses/{course.id}/delete', follow_redirects=True)

    assert b"examinations are linked" in res.data or b"has scheduled examinations" in res.data
    # Verify course was NOT deleted
    assert Course.query.get(course.id) is not None


# =========================================================================
# Defect 5: Allocation Engine Capacity Failure Does Not Wipe Existing Allocations
# =========================================================================
def test_defect_5_allocation_data_loss_prevention(test_db):
    course = Course.query.filter_by(code='CS').first()
    subj = Subject.query.filter_by(code='CS601').first()
    hall = ExaminationHall.query.filter_by(hall_code='H-101').first()

    exam = Examination(
        exam_code='EX-SAFE-01', exam_name='Safe Realloc Exam', course_id=course.id, subject_id=subj.id,
        semester=6, exam_date=date(2026, 12, 20), start_time=time(9, 0), end_time=time(12, 0),
        duration_minutes=180, status='Scheduled'
    )
    db.session.add(exam)
    db.session.flush()

    # Create 5 students and eligible records
    students = []
    for i in range(1, 6):
        st = Student(
            enrollment_no=f'EN-SAFE-{i:03d}', full_name=f'Safe Student {i}', email=f'safe{i}@test.com',
            mobile=f'98111111{i:02d}', course_id=course.id, branch='CS', semester=6, division='A', status='Active'
        )
        db.session.add(st)
        db.session.flush()
        students.append(st)
        el = EligibleStudent(examination_id=exam.id, student_id=st.id)
        db.session.add(el)
    db.session.commit()

    # Run initial successful allocation
    res1 = AllocationEngine.allocate_examination(exam.id, strategy='Sequential', hall_ids=[hall.id])
    assert res1.success is True
    initial_alloc_count = SeatAllocation.query.filter_by(examination_id=exam.id).count()
    assert initial_alloc_count == 5

    # Now add a tiny dummy hall with capacity 2 and status Active
    tiny_hall = ExaminationHall(
        hall_code='H-TINY', hall_name='Tiny Room', building='Admin', floor='G',
        num_rows=1, num_cols=2, total_capacity=2, status='Active'
    )
    db.session.add(tiny_hall)
    db.session.commit()

    # Attempt to reallocate specifying only tiny_hall with force_reallocate=True
    # Capacity is 2, students are 5. Capacity validation should FAIL.
    res2 = AllocationEngine.allocate_examination(exam.id, strategy='Sequential', hall_ids=[tiny_hall.id], force_reallocate=True)
    assert res2.success is False
    assert "Insufficient seat capacity" in res2.message

    # Crucial assertion: Existing 5 allocations MUST NOT be destroyed!
    refreshed_alloc_count = SeatAllocation.query.filter_by(examination_id=exam.id).count()
    assert refreshed_alloc_count == 5


# =========================================================================
# Defect 6: Manual Allocation Dynamic Exam Choices on POST
# =========================================================================
def test_defect_6_manual_allocation_post_choice_validation(client, test_db):
    login_user_helper(client, 'admin', 'Admin@2026')
    course = Course.query.filter_by(code='CS').first()
    subj = Subject.query.filter_by(code='CS601').first()
    hall = ExaminationHall.query.filter_by(hall_code='H-101').first()

    exam1 = Examination(
        exam_code='EX-CHOICE-1', exam_name='Choice Exam 1', course_id=course.id, subject_id=subj.id,
        semester=6, exam_date=date(2026, 12, 21), start_time=time(9, 0), end_time=time(12, 0),
        duration_minutes=180, status='Scheduled'
    )
    exam2 = Examination(
        exam_code='EX-CHOICE-2', exam_name='Choice Exam 2', course_id=course.id, subject_id=subj.id,
        semester=6, exam_date=date(2026, 12, 22), start_time=time(9, 0), end_time=time(12, 0),
        duration_minutes=180, status='Scheduled'
    )
    db.session.add_all([exam1, exam2])
    db.session.flush()

    student2 = Student(
        enrollment_no='EN-CHOICE-02', full_name='Student for Exam 2', email='choice2@test.com',
        mobile='9822222222', course_id=course.id, branch='CS', semester=6, division='A', status='Active'
    )
    db.session.add(student2)
    db.session.flush()

    # Eligible ONLY for Exam 2
    el = EligibleStudent(examination_id=exam2.id, student_id=student2.id)
    db.session.add(el)
    db.session.commit()

    # POST to /admin/allocation/manual selecting Exam 2 and student2
    res = client.post('/admin/allocation/manual', data={
        'examination_id': exam2.id,
        'student_id': student2.id,
        'hall_id': hall.id,
        'row_num': 2,
        'col_num': 2
    }, follow_redirects=True)

    # Should succeed without WTForms "Not a valid choice" error
    assert b"Assigned Student for Exam 2" in res.data or b"Visual Seating Grid" in res.data
    alloc = SeatAllocation.query.filter_by(examination_id=exam2.id, student_id=student2.id).first()
    assert alloc is not None
    assert alloc.row_num == 2 and alloc.col_num == 2


# =========================================================================
# Defect 7: Invigilator IDOR / Authorization Enforcement
# =========================================================================
def test_defect_7_invigilator_idor_authorization(client, test_db):
    course = Course.query.filter_by(code='CS').first()
    subj = Subject.query.filter_by(code='CS601').first()
    hall1 = ExaminationHall.query.filter_by(hall_code='H-101').first()

    hall2 = ExaminationHall(
        hall_code='H-102', hall_name='Hall 102', building='East Block', floor='2nd',
        num_rows=4, num_cols=4, total_capacity=16, status='Active'
    )
    db.session.add(hall2)
    db.session.flush()

    exam = Examination(
        exam_code='EX-INV-101', exam_name='Invigilator Exam', course_id=course.id, subject_id=subj.id,
        semester=6, exam_date=date(2026, 12, 25), start_time=time(10, 0), end_time=time(13, 0),
        duration_minutes=180, status='Scheduled'
    )
    db.session.add(exam)
    db.session.flush()

    inv_user = User(username='inv_sharma', email='sharma@upluniversity.ac.in', role='invigilator')
    inv_user.set_password('Inv@1234')
    db.session.add(inv_user)
    db.session.flush()

    inv_profile = Invigilator(
        user_id=inv_user.id, faculty_id='FAC-101', full_name='Prof. Sharma',
        email='sharma@upluniversity.ac.in', phone='9833333333', department='CS'
    )
    db.session.add(inv_profile)
    db.session.flush()

    # Assign Prof. Sharma to Hall 101 ONLY
    assignment = InvigilatorAssignment(
        invigilator_id=inv_profile.id, examination_id=exam.id, hall_id=hall1.id
    )
    db.session.add(assignment)
    db.session.commit()

    # Log in as Prof. Sharma
    login_user_helper(client, 'inv_sharma', 'Inv@1234')

    # Access assigned hall (Hall 101) -> Should be 200 OK
    res_allowed = client.get(f'/invigilator/hall/{hall1.id}/exam/{exam.id}')
    assert res_allowed.status_code == 200

    # Attempt to access unassigned hall (Hall 102) -> Should be 403 Forbidden (IDOR prevented)
    res_forbidden = client.get(f'/invigilator/hall/{hall2.id}/exam/{exam.id}')
    assert res_forbidden.status_code == 403

    # Attempt to download unassigned hall PDF -> Should be 403 Forbidden
    res_pdf_forbidden = client.get(f'/invigilator/hall/{hall2.id}/exam/{exam.id}/pdf')
    assert res_pdf_forbidden.status_code == 403


# =========================================================================
# Defect 8: Safe Login Redirection (CWE-601 Open Redirect Prevention)
# =========================================================================
def test_defect_8_open_redirect_sanitization(client, test_db):
    # Attempt login with external next URL
    res = client.post('/login?next=https://attacker.evil.com', data={
        'username': 'admin',
        'password': 'Admin@2026'
    }, follow_redirects=False)

    # Redirection location MUST NOT be the attacker URL
    assert res.status_code == 302
    assert 'attacker.evil.com' not in res.headers['Location']
    assert res.headers['Location'].endswith('/admin/dashboard')

    # Attempt protocol-relative URL
    res2 = client.post('/login?next=//attacker.evil.com/path', data={
        'username': 'admin',
        'password': 'Admin@2026'
    }, follow_redirects=False)

    assert res2.status_code == 302
    assert '//attacker.evil.com' not in res2.headers['Location']


# =========================================================================
# Defect 9: Dashboard Capacity Metric Accuracy with Inactive Halls
# =========================================================================
def test_defect_9_dashboard_capacity_accuracy(client, test_db):
    login_user_helper(client, 'admin', 'Admin@2026')
    hall1 = ExaminationHall.query.filter_by(hall_code='H-101').first()
    # Hall 101: 30 total, 1 blocked -> 29 usable

    # Create an inactive hall with 10 blocked seats
    inactive_hall = ExaminationHall(
        hall_code='H-INACTIVE', hall_name='Decommissioned Hall', building='Old Block', floor='G',
        num_rows=5, num_cols=5, total_capacity=25, status='Inactive'
    )
    db.session.add(inactive_hall)
    db.session.flush()

    for r in range(1, 3):
        for c in range(1, 6):
            b = BlockedSeat(hall_id=inactive_hall.id, row_num=r, col_num=c, seat_identifier=f'H-INACTIVE-R{r}-C{c}')
            db.session.add(b)
    db.session.commit()

    # Active halls usable capacity should be exactly 29, NOT 29 - 10 = 19
    res = client.get('/admin/dashboard')
    assert res.status_code == 200
    # Context or response data should reflect 29 usable seats
    assert b"29" in res.data


# =========================================================================
# Defect 10: Security Response Headers (Defense-in-Depth)
# =========================================================================
def test_defect_10_security_response_headers(client, test_db):
    res = client.get('/login')
    assert res.status_code == 200
    assert res.headers.get('X-Frame-Options') == 'SAMEORIGIN'
    assert res.headers.get('X-Content-Type-Options') == 'nosniff'
    assert res.headers.get('Referrer-Policy') == 'strict-origin-when-cross-origin'


# =========================================================================
# Defect 11: Student Edit Email Collision Graceful Validation
# =========================================================================
def test_defect_11_student_edit_duplicate_email(client, test_db):
    login_user_helper(client, 'admin', 'Admin@2026')
    course = Course.query.filter_by(code='CS').first()

    st1 = Student(
        enrollment_no='EN-EDIT-1', full_name='Student One', email='st1@upluniversity.ac.in',
        mobile='9844444441', course_id=course.id, branch='CS', semester=6, division='A', status='Active'
    )
    st2 = Student(
        enrollment_no='EN-EDIT-2', full_name='Student Two', email='st2@upluniversity.ac.in',
        mobile='9844444442', course_id=course.id, branch='CS', semester=6, division='A', status='Active'
    )
    db.session.add_all([st1, st2])
    db.session.commit()

    # Attempt to edit st2 to use st1's email address
    res = client.post(f'/admin/students/{st2.id}/edit', data={
        'enrollment_no': 'EN-EDIT-2',
        'full_name': 'Student Two',
        'email': 'st1@upluniversity.ac.in',
        'mobile': '9844444442',
        'course_id': course.id,
        'branch': 'CS',
        'semester': 6,
        'division': 'A',
        'academic_year': '2025-2026',
        'status': 'Active'
    }, follow_redirects=True)

    # Should gracefully display flash error, NOT throw a 500 IntegrityError
    assert res.status_code == 200
    assert b"already used by another student" in res.data
    refreshed_st2 = Student.query.get(st2.id)
    assert refreshed_st2.email == 'st2@upluniversity.ac.in'


# =========================================================================
# Defect 12: Seat Blocking on Completed or Cancelled Exam
# =========================================================================
def test_defect_12_seat_blocking_filter_status(client, test_db):
    login_user_helper(client, 'admin', 'Admin@2026')
    course = Course.query.filter_by(code='CS').first()
    subj = Subject.query.filter_by(code='CS601').first()
    hall = ExaminationHall.query.filter_by(hall_code='H-101').first()

    cancelled_exam = Examination(
        exam_code='EX-CANCELLED', exam_name='Old Cancelled Exam', course_id=course.id, subject_id=subj.id,
        semester=6, exam_date=date(2026, 11, 1), start_time=time(10, 0), end_time=time(13, 0),
        duration_minutes=180, status='Cancelled'
    )
    db.session.add(cancelled_exam)
    db.session.flush()

    student = Student(
        enrollment_no='EN-OLD-01', full_name='Old Student', email='oldst@test.com',
        mobile='9855555555', course_id=course.id, branch='CS', semester=6, division='A', status='Active'
    )
    db.session.add(student)
    db.session.flush()

    # Allocation existed in row 3, col 3 for cancelled exam
    alloc = SeatAllocation(
        examination_id=cancelled_exam.id, student_id=student.id, hall_id=hall.id,
        row_num=3, col_num=3, seat_identifier='H-101-R03-C03', strategy_used='Sequential'
    )
    db.session.add(alloc)
    db.session.commit()

    # Now attempt to toggle/block seat R03-C03
    res = client.post(f'/admin/halls/{hall.id}/toggle-seat', json={'row': 3, 'col': 3, 'reason': 'Damaged leg'})

    assert res.status_code == 200
    data = res.get_json()
    assert data['success'] is True
    assert data['action'] == 'blocked'
    # Seat is successfully blocked
    block = BlockedSeat.query.filter_by(hall_id=hall.id, row_num=3, col_num=3).first()
    assert block is not None

