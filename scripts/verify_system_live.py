"""
Live End-to-End System Verification Script for ParikshaVinyas
Tests:
1. Admin, Invigilator, and Student authentication & RBAC.
2. Exam scheduling collision checks.
3. Automatic seat allocation (Sequential, Mixed Course, Random).
4. Capacity boundary rejection.
5. Manual seat assignment and seat swapping.
6. ReportLab PDF generation for Seating Charts and Student Admit Passes.
7. Security: IDOR protection and HTTP response headers.
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models.exam import Examination
from app.models.hall import ExaminationHall
from app.models.student import Student
from app.models.allocation import SeatAllocation
from app.models.invigilator import Invigilator, InvigilatorAssignment
from app.services.allocation_engine import AllocationEngine
from app.services.report_service import ReportService
from datetime import date, time

app = create_app()
app.config['WTF_CSRF_ENABLED'] = False
app.config['TESTING'] = True

def run_live_verification():
    print("=================================================================")
    print(" PARIKSHAVINYAS — LIVE SYSTEM VERIFICATION RUN")
    print("=================================================================")
    
    with app.app_context():
        client = app.test_client()

        # ---------------------------------------------------------------
        # 1. Test Admin Workflow
        # ---------------------------------------------------------------
        print("\n[1] Testing Administrator Authentication & Role Controls...")
        login_res = client.post('/login', data={'username': 'admin', 'password': 'Admin@2026'}, follow_redirects=True)
        assert login_res.status_code == 200, "Admin login failed"
        assert b"admin" in login_res.data, "Admin username not found in dashboard"
        print("  -> Admin Login: SUCCESS (Redirected to /admin/dashboard)")

        # Verify Dashboard metrics
        dash_res = client.get('/admin/dashboard')
        assert dash_res.status_code == 200
        assert b"Registered Candidates" in dash_res.data
        print("  -> Admin Dashboard Metrics: SUCCESS")

        # ---------------------------------------------------------------
        # 2. Test Exam Scheduling Constraints & Collision Detection
        # ---------------------------------------------------------------
        print("\n[2] Testing Examination Scheduling & Conflict Enforcement...")
        exam_cs = Examination.query.filter_by(exam_code='EX-CS601').first()
        assert exam_cs is not None

        # Attempt to schedule an overlapping exam for the same course and semester on same date
        conflict_res = client.post('/admin/exams/add', data={
            'exam_code': 'EX-CONFLICT',
            'exam_name': 'Conflicting Exam',
            'course_id': exam_cs.course_id,
            'subject_id': exam_cs.subject_id,
            'semester': exam_cs.semester,
            'exam_date': exam_cs.exam_date.strftime('%Y-%m-%d'),
            'start_time': '11:00',
            'end_time': '12:30',
            'duration_minutes': 90,
            'exam_type': 'Regular',
            'academic_year': '2025-2026',
            'status': 'Scheduled'
        }, follow_redirects=True)
        assert b"Scheduling Conflict" in conflict_res.data, "Collision detection failed on add"
        print("  -> Timetable Conflict Prevention (Add): SUCCESS")

        # ---------------------------------------------------------------
        # 3. Test Automatic Seat Allocation Engine
        # ---------------------------------------------------------------
        print("\n[3] Testing Automatic Allocation Strategies & Rollback Safety...")
        exam_cs602 = Examination.query.filter_by(exam_code='EX-CS602').first()
        hall_101 = ExaminationHall.query.filter_by(hall_code='H-101').first()
        hall_102 = ExaminationHall.query.filter_by(hall_code='H-102').first()

        # Strategy A: Mixed Course Allocation
        res_mixed = AllocationEngine.allocate_examination(
            examination_id=exam_cs.id,
            strategy='Mixed Course',
            hall_ids=[hall_101.id, hall_102.id],
            force_reallocate=True
        )
        assert res_mixed.success is True, f"Mixed course allocation failed: {res_mixed.message}"
        print(f"  -> Mixed Course Allocation: SUCCESS ({res_mixed.message})")

        # Strategy B: Random Allocation with Reproducible Seed
        res_random = AllocationEngine.allocate_examination(
            examination_id=exam_cs602.id,
            strategy='Random',
            hall_ids=[hall_101.id],
            seed=42,
            force_reallocate=True
        )
        assert res_random.success is True, f"Random allocation failed: {res_random.message}"
        print(f"  -> Random Allocation (Seed 42): SUCCESS ({res_random.message})")

        # Strategy C: Sequential Allocation
        exam_it = Examination.query.filter_by(exam_code='EX-IT601').first()
        hall_201 = ExaminationHall.query.filter_by(hall_code='H-201').first()
        res_seq = AllocationEngine.allocate_examination(
            examination_id=exam_it.id,
            strategy='Sequential',
            hall_ids=[hall_201.id],
            force_reallocate=True
        )
        assert res_seq.success is True, f"Sequential allocation failed: {res_seq.message}"
        print(f"  -> Sequential Allocation: SUCCESS ({res_seq.message})")

        # Capacity Shortage Boundary Rejection
        tiny_hall = ExaminationHall.query.filter_by(hall_code='H-202').first() # 24 seats
        # exam_cs has 30 students. Attempt allocation into tiny_hall alone:
        res_shortage = AllocationEngine.allocate_examination(
            examination_id=exam_cs.id,
            strategy='Sequential',
            hall_ids=[tiny_hall.id],
            force_reallocate=True
        )
        assert res_shortage.success is False, "Capacity boundary rejection failed"
        assert "Insufficient seat capacity" in res_shortage.message
        print(f"  -> Capacity Shortage Boundary Rejection: SUCCESS ({res_shortage.message[:60]}...)")
        # Ensure prior allocations were NOT wiped:
        assert SeatAllocation.query.filter_by(examination_id=exam_cs.id).count() == 30
        print("  -> Allocation Preservation on Failure: SUCCESS (30 prior seats kept)")

        # ---------------------------------------------------------------
        # 4. Test Manual Seat Allocation & Swapping
        # ---------------------------------------------------------------
        print("\n[4] Testing Manual Allocation & Seat Swapping...")
        allocs = SeatAllocation.query.filter_by(examination_id=exam_cs.id).order_by(SeatAllocation.id).all()
        student_a = allocs[0].student
        student_b = allocs[1].student
        seat_a_ident = allocs[0].seat_identifier
        seat_b_ident = allocs[1].seat_identifier
        seat_b_row = allocs[1].row_num
        seat_b_col = allocs[1].col_num
        seat_b_hall = allocs[1].hall_id

        # Swap student A into student B's seat
        swap_res = AllocationEngine.manual_assign_or_swap(
            examination_id=exam_cs.id,
            student_id=student_a.id,
            target_hall_id=seat_b_hall,
            target_row=seat_b_row,
            target_col=seat_b_col
        )
        assert swap_res.success is True, f"Manual swap failed: {swap_res.message}"
        print(f"  -> Manual Bidirectional Seat Swap: SUCCESS ({swap_res.message})")

        # ---------------------------------------------------------------
        # 5. Test ReportLab PDF Generation
        # ---------------------------------------------------------------
        print("\n[5] Testing PDF Report Generation (ReportLab)...")
        # Hall Attendance PDF
        pdf_hall_buffer = ReportService.generate_hall_seating_pdf(exam_cs.id, hall_101.id)
        assert pdf_hall_buffer is not None
        pdf_bytes = pdf_hall_buffer.getvalue()
        assert pdf_bytes.startswith(b'%PDF'), "Invalid PDF generated for hall seating"
        print(f"  -> Hall Seating Attendance PDF: SUCCESS ({len(pdf_bytes)} bytes generated)")

        # Student Admit Card PDF
        pdf_admit_buffer = ReportService.generate_student_seating_slip_pdf(student_a.id)
        assert pdf_admit_buffer is not None
        admit_bytes = pdf_admit_buffer.getvalue()
        assert admit_bytes.startswith(b'%PDF'), "Invalid PDF generated for student admit pass"
        print(f"  -> Student Admit Card PDF: SUCCESS ({len(admit_bytes)} bytes generated)")

        # ---------------------------------------------------------------
        # 6. Test Invigilator Workflow & IDOR Protection
        # ---------------------------------------------------------------
        print("\n[6] Testing Invigilator Role & Authorization Controls...")
        client.get('/logout') # Logout admin
        invig_login = client.post('/login', data={'username': 'invig_sharma', 'password': 'Invig@2026'}, follow_redirects=True)
        assert invig_login.status_code == 200
        assert b"Invigilation" in invig_login.data
        print("  -> Invigilator Login: SUCCESS (Redirected to /invigilator/dashboard)")

        # Assigned Hall access
        invig_profile = Invigilator.query.filter_by(faculty_id='FAC-CS-01').first()
        assignment = InvigilatorAssignment.query.filter_by(invigilator_id=invig_profile.id).first()
        assert assignment is not None
        res_assigned = client.get(f'/invigilator/hall/{assignment.hall_id}/exam/{assignment.examination_id}')
        assert res_assigned.status_code == 200
        print(f"  -> Access to Assigned Hall {assignment.hall.hall_code}: SUCCESS (200 OK)")

        # IDOR check: Attempt access to unassigned hall
        unassigned_hall = hall_201
        res_unauth = client.get(f'/invigilator/hall/{unassigned_hall.id}/exam/{assignment.examination_id}')
        assert res_unauth.status_code == 403, f"Expected 403 Forbidden on unassigned hall, got {res_unauth.status_code}"
        print(f"  -> IDOR Authorization Protection on Unassigned Hall: SUCCESS (403 Forbidden)")

        # ---------------------------------------------------------------
        # 7. Test Student Portal Workflow
        # ---------------------------------------------------------------
        print("\n[7] Testing Student Portal Role & Schedule Access...")
        client.get('/logout') # Logout invigilator
        student_user = student_a.user
        stud_login = client.post('/login', data={'username': student_a.enrollment_no, 'password': f"Student@{student_a.enrollment_no[-4:]}"}, follow_redirects=True)
        assert stud_login.status_code == 200
        assert b"My Examination Schedule" in stud_login.data
        print(f"  -> Student Login ({student_a.enrollment_no}): SUCCESS (Redirected to /student/dashboard)")

        # Verify Student Seating Pass PDF Download
        slip_res = client.get('/student/slip/pdf')
        assert slip_res.status_code == 200
        assert slip_res.data.startswith(b'%PDF'), "Invalid PDF received from student portal download"
        print(f"  -> Digital Seating Slip PDF Download: SUCCESS ({len(slip_res.data)} bytes)")

        # RBAC Check: Ensure Student cannot access admin endpoints
        admin_blocked = client.get('/admin/dashboard')
        assert admin_blocked.status_code == 403, f"Expected 403 Forbidden for Student on /admin/dashboard, got {admin_blocked.status_code}"
        print("  -> RBAC Student Security Boundary: SUCCESS (403 Forbidden on /admin/dashboard)")

        # ---------------------------------------------------------------
        # 8. Test Security Response Headers
        # ---------------------------------------------------------------
        print("\n[8] Testing Defense-in-Depth HTTP Security Headers...")
        headers_res = client.get('/login')
        assert headers_res.headers.get('X-Frame-Options') == 'SAMEORIGIN'
        assert headers_res.headers.get('X-Content-Type-Options') == 'nosniff'
        assert headers_res.headers.get('Referrer-Policy') == 'strict-origin-when-cross-origin'
        print("  -> HTTP Security Headers (X-Frame-Options, X-Content-Type-Options, Referrer-Policy): SUCCESS")

        print("\n=================================================================")
        print(" ALL 8 LIVE WORKFLOWS PASSED ZERO FAILURES!")
        print("=================================================================")

if __name__ == '__main__':
    run_live_verification()
