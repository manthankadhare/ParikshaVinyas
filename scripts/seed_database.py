import os
import sys
from datetime import datetime, date, time

# Add root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models.user import User
from app.models.academic import Department, Course, Subject
from app.models.student import Student
from app.models.hall import ExaminationHall, BlockedSeat
from app.models.exam import Examination, EligibleStudent
from app.models.invigilator import Invigilator, InvigilatorAssignment
from app.models.qa import TestCase, DefectReport
from app.models.audit import ActivityLog, SystemSetting
from app.services.allocation_engine import AllocationEngine


def seed():
    app = create_app()
    with app.app_context():
        print("Initializing database tables...")
        db.create_all()

        # 1. System Settings
        settings_data = [
            ('college_name', 'UPL University of Sustainable Technology', 'Institution Name'),
            ('academic_year', '2025-2026', 'Current Academic Year'),
            ('default_allocation_strategy', 'Mixed Course', 'Default Seat Allocation Algorithm'),
            ('helpline', '+91 (02643) 293300 / examcell@upluniversity.ac.in', 'Exam Emergency Helpline')
        ]
        for k, v, desc in settings_data:
            if not SystemSetting.query.filter_by(key=k).first():
                db.session.add(SystemSetting(key=k, value=v, description=desc))
        db.session.commit()

        # 2. Users (Admin, Invigilators)
        print("Seeding administrative & faculty accounts...")
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(username='admin', email='admin@parikshavinyas.edu', role='admin')
            admin.set_password('Admin@2026')
            db.session.add(admin)
            db.session.commit()
            print("  Created Admin: admin / Admin@2026")

        # 3. Invigilators
        invig_specs = [
            ('invig_sharma', 'FAC-CS-01', 'Dr. Rajesh Sharma', 'Computer Engineering', '9822011223', 'sharma@upluniversity.ac.in'),
            ('invig_patil', 'FAC-IT-02', 'Prof. Sunita Patil', 'Information Technology', '9822011224', 'patil@upluniversity.ac.in'),
            ('invig_deshmukh', 'FAC-ME-03', 'Dr. Anil Deshmukh', 'Mechanical Engineering', '9822011225', 'deshmukh@upluniversity.ac.in')
        ]
        invigilator_objs = []
        for uname, fid, fname, dept, phone, email in invig_specs:
            u = User.query.filter_by(username=uname).first()
            if not u:
                u = User(username=uname, email=email, role='invigilator')
                u.set_password('Invig@2026')
                db.session.add(u)
                db.session.flush()

            inv = Invigilator.query.filter_by(faculty_id=fid).first()
            if not inv:
                inv = Invigilator(user_id=u.id, faculty_id=fid, full_name=fname, department=dept, phone=phone, email=email)
                db.session.add(inv)
                db.session.flush()
            invigilator_objs.append(inv)
        db.session.commit()

        # 4. Departments & Courses
        print("Seeding courses and curricula...")
        courses_data = [
            ('CS', 'B.Tech Computer Science & Engineering', 'Department of Computer Engineering', 8),
            ('IT', 'B.Tech Information Technology', 'Department of Information Technology', 8),
            ('ME', 'B.Tech Mechanical Engineering', 'Department of Mechanical Engineering', 8),
            ('ENTC', 'B.Tech Electronics & Telecommunication', 'Department of Electronics', 8),
        ]
        course_map = {}
        for code, name, dept, sems in courses_data:
            c = Course.query.filter_by(code=code).first()
            if not c:
                c = Course(code=code, name=name, department=dept, total_semesters=sems)
                db.session.add(c)
                db.session.flush()
            course_map[code] = c
        db.session.commit()

        # 5. Subjects
        subjects_data = [
            ('CS601', 'Software Testing & Quality Assurance', 'CS', 6, 4),
            ('CS602', 'Cloud Computing & Distributed Systems', 'CS', 6, 4),
            ('IT601', 'Information & Network Security', 'IT', 6, 4),
            ('IT602', 'Full-Stack Web Architectures', 'IT', 6, 3),
            ('ME401', 'Heat & Mass Transfer', 'ME', 4, 4),
            ('ENTC601', 'Digital Signal Processing', 'ENTC', 6, 4),
        ]
        subject_map = {}
        for scode, sname, ccode, sem, credits in subjects_data:
            s = Subject.query.filter_by(code=scode).first()
            if not s:
                s = Subject(code=scode, name=sname, course_id=course_map[ccode].id, semester=sem, credits=credits)
                db.session.add(s)
                db.session.flush()
            subject_map[scode] = s
        db.session.commit()

        # 6. Examination Halls & Blocked Seats
        print("Seeding examination halls and seating configurations...")
        halls_data = [
            ('H-101', 'Main Academic Wing - Hall 101', 'Main Building', '1st Floor', 5, 8),  # 40 seats
            ('H-102', 'Main Academic Wing - Hall 102', 'Main Building', '1st Floor', 5, 6),  # 30 seats
            ('H-201', 'IT Complex - Seminar Hall 201', 'IT Tower', '2nd Floor', 6, 8),       # 48 seats
            ('H-202', 'IT Complex - Drawing Hall 202', 'IT Tower', '2nd Floor', 4, 6),       # 24 seats
            ('AUD-1', 'Central University Auditorium', 'Central Complex', 'Ground Floor', 8, 10), # 80 seats
        ]
        hall_map = {}
        for hcode, hname, bldg, flr, rows, cols in halls_data:
            h = ExaminationHall.query.filter_by(hall_code=hcode).first()
            if not h:
                h = ExaminationHall(
                    hall_code=hcode, hall_name=hname, building=bldg, floor=flr,
                    num_rows=rows, num_cols=cols, total_capacity=rows * cols, status='Active'
                )
                db.session.add(h)
                db.session.flush()
            hall_map[hcode] = h
        db.session.commit()

        # Blocked seats
        blocked_specs = [
            ('H-101', 1, 3, 'Damaged desk armrest'),
            ('H-101', 3, 7, 'Overhead fan maintenance'),
            ('H-201', 2, 4, 'Wobbly writing board'),
            ('H-201', 5, 8, 'Reserved for disabled student accommodation'),
            ('AUD-1', 1, 1, 'Audio-visual equipment placement obstruction'),
        ]
        for hcode, r, c, reason in blocked_specs:
            hall_obj = hall_map[hcode]
            if not BlockedSeat.query.filter_by(hall_id=hall_obj.id, row_num=r, col_num=c).first():
                bs = BlockedSeat(
                    hall_id=hall_obj.id, row_num=r, col_num=c,
                    seat_identifier=f"{hcode}-R{r:02d}-C{c:02d}", reason=reason
                )
                db.session.add(bs)
        db.session.commit()

        # 7. Students (60 Realistic Indian Engineering Students)
        print("Seeding student candidates roster (60 candidates)...")
        first_names = [
            'Aarav', 'Ananya', 'Rohan', 'Pooja', 'Aditya', 'Sneha', 'Vikram', 'Tanvi',
            'Siddharth', 'Ishita', 'Arjun', 'Priyanka', 'Varun', 'Neha', 'Kunal', 'Riya',
            'Abhishek', 'Kavita', 'Manish', 'Shreya', 'Pranav', 'Meera', 'Gaurav', 'Aditi',
            'Nikhil', 'Divya', 'Rahul', 'Sakshi', 'Karan', 'Deepika'
        ]
        last_names = [
            'Sharma', 'Verma', 'Patil', 'Deshmukh', 'Joshi', 'Kulkarni', 'Mehta', 'Shah',
            'Chauhan', 'Singhania', 'Gupta', 'Iyer', 'Nair', 'Reddy', 'Rao'
        ]

        student_objs = []
        enroll_idx = 101

        # Course distribution: 30 CS (Sem 6, Div A & B), 20 IT (Sem 6, Div A), 10 ME (Sem 4, Div A)
        dist = [
            ('CS', 6, 'A', 15),
            ('CS', 6, 'B', 15),
            ('IT', 6, 'A', 20),
            ('ME', 4, 'A', 10),
        ]

        name_counter = 0
        for ccode, sem, div, count in dist:
            c_obj = course_map[ccode]
            for _ in range(count):
                fn = first_names[name_counter % len(first_names)]
                ln = last_names[(name_counter // 2) % len(last_names)]
                full_name = f"{fn} {ln}"
                enroll_no = f"EN2026{enroll_idx}"
                email = f"{fn.lower()}.{ln.lower()}{enroll_idx}@upluniversity.ac.in"
                mobile = f"9822{enroll_idx:06d}"
                enroll_idx += 1
                name_counter += 1

                st = Student.query.filter_by(enrollment_no=enroll_no).first()
                if not st:
                    # Create student user login
                    u = User.query.filter_by(username=enroll_no.lower()).first()
                    if not u:
                        u = User(username=enroll_no.lower(), email=email, role='student')
                        last4 = enroll_no[-4:]
                        u.set_password(f"Student@{last4}")
                        db.session.add(u)
                        db.session.flush()

                    st = Student(
                        user_id=u.id,
                        enrollment_no=enroll_no,
                        full_name=full_name,
                        email=email,
                        mobile=mobile,
                        course_id=c_obj.id,
                        branch=c_obj.name.replace('B.Tech ', ''),
                        semester=sem,
                        division=div,
                        academic_year='2025-2026',
                        status='Active'
                    )
                    db.session.add(st)
                    db.session.flush()
                student_objs.append(st)
        db.session.commit()
        print(f"  Created {len(student_objs)} active candidates with credentials.")

        # 8. Examinations
        print("Scheduling examinations...")
        exams_specs = [
            ('EX-CS601', 'Software Testing & Quality Assurance', 'CS601', 'CS', 6, date(2026, 12, 10), time(10, 0), time(13, 0), 180, 'Regular'),
            ('EX-IT601', 'Information & Network Security', 'IT601', 'IT', 6, date(2026, 12, 12), time(10, 0), time(13, 0), 180, 'Regular'),
            ('EX-CS602', 'Cloud Computing & Virtualization', 'CS602', 'CS', 6, date(2026, 12, 15), time(14, 0), time(17, 0), 180, 'Regular'),
        ]
        exam_objs = []
        for ecode, ename, scode, ccode, sem, edate, stime, etime, dur, etype in exams_specs:
            ex = Examination.query.filter_by(exam_code=ecode).first()
            if not ex:
                ex = Examination(
                    exam_code=ecode,
                    exam_name=ename,
                    subject_id=subject_map[scode].id,
                    course_id=course_map[ccode].id,
                    semester=sem,
                    exam_date=edate,
                    start_time=stime,
                    end_time=etime,
                    duration_minutes=dur,
                    exam_type=etype,
                    status='Scheduled'
                )
                db.session.add(ex)
                db.session.flush()

                # Enroll eligible candidates
                matching_students = Student.query.filter_by(course_id=course_map[ccode].id, semester=sem, status='Active').all()
                for mst in matching_students:
                    el = EligibleStudent(examination_id=ex.id, student_id=mst.id)
                    db.session.add(el)
            exam_objs.append(ex)
        db.session.commit()

        # 9. Assign Invigilators
        if exam_objs and invigilator_objs:
            if not InvigilatorAssignment.query.first():
                db.session.add(InvigilatorAssignment(examination_id=exam_objs[0].id, hall_id=hall_map['H-101'].id, invigilator_id=invigilator_objs[0].id))
                db.session.add(InvigilatorAssignment(examination_id=exam_objs[0].id, hall_id=hall_map['H-102'].id, invigilator_id=invigilator_objs[1].id))
                db.session.add(InvigilatorAssignment(examination_id=exam_objs[1].id, hall_id=hall_map['H-201'].id, invigilator_id=invigilator_objs[2].id))
                db.session.commit()

        # 10. Execute Auto Allocation for EX-CS601 (Mixed Course) and EX-IT601 (Sequential)
        print("Running automatic seat allocation engine for initial exams...")
        res1 = AllocationEngine.allocate_examination(
            examination_id=exam_objs[0].id,
            strategy='Mixed Course',
            hall_ids=[hall_map['H-101'].id, hall_map['H-102'].id],
            user_id=admin.id,
            force_reallocate=True
        )
        print(f"  EX-CS601 Allocation Result: {res1.message}")

        res2 = AllocationEngine.allocate_examination(
            examination_id=exam_objs[1].id,
            strategy='Sequential',
            hall_ids=[hall_map['H-201'].id],
            user_id=admin.id,
            force_reallocate=True
        )
        print(f"  EX-IT601 Allocation Result: {res2.message}")

        # 11. Seed Manual STQA Test Cases (30 comprehensive cases: 15 Positive, 15 Negative/Edge)
        print("Seeding STQA test case repository (30 formal test cases)...")
        test_cases_seed = [
            # 15 Positive Scenarios
            ('TC_AUTH_POS_01', 'Authentication & Security', 'Administrator successful login with valid credentials', 'Admin user exists in database', 'Username: admin, Password: Admin@2026', 'Redirects to /admin/dashboard with 200 OK and session cookie set', 'Pass', 'Equivalence Partitioning (EP)', 'Positive'),
            ('TC_AUTH_POS_02', 'Authentication & Security', 'Student login using enrollment number as username', 'Student user exists with enrollment EN2026101', 'Username: EN2026101, Password: Student@6101', 'Redirects to /student/dashboard; displays personal exam schedule', 'Pass', 'Equivalence Partitioning (EP)', 'Positive'),
            ('TC_AUTH_POS_03', 'Authentication & Security', 'Invigilator login and view assigned duty halls', 'Invigilator user exists', 'Username: invig_sharma, Password: Invig@2026', 'Redirects to /invigilator/dashboard; displays assigned halls', 'Pass', 'Role-Based Access Control', 'Positive'),
            ('TC_STUD_POS_04', 'Student Management', 'Register new candidate with all valid mandatory fields', 'Course CS exists', 'Enrollment: EN2026199, Name: Aarav Joshi, Sem: 6, Div: A', 'Student and linked user account created successfully with Active status', 'Pass', 'Equivalence Partitioning (EP)', 'Positive'),
            ('TC_STUD_POS_05', 'Student Management', 'Search candidates by enrollment number substring', '60 students in database', 'Search query: 101', 'Table filters to show matching candidate EN2026101', 'Pass', 'Functional Equivalence', 'Positive'),
            ('TC_STUD_POS_06', 'Student Management', 'Filter candidates by Degree Course and Semester', 'Multiple courses exist', 'Course: CS, Semester: 6', 'Table renders only CS Semester 6 students', 'Pass', 'Decision Table Testing', 'Positive'),
            ('TC_HALL_POS_07', 'Hall Management', 'Create new examination hall and verify capacity auto-calculation', 'Admin logged in', 'Rows: 6, Cols: 8, Building: Block C', 'Hall created with Total Capacity = 48 (6*8); Usable Capacity = 48', 'Pass', 'Functional Testing', 'Positive'),
            ('TC_HALL_POS_08', 'Hall Management', 'Toggle block state on seat R01-C01 in empty hall', 'Hall H-102 exists', 'Block Row 1, Col 1 with reason: Broken armrest', 'Usable capacity drops by 1; seat turns red in visual layout', 'Pass', 'State Transition Testing', 'Positive'),
            ('TC_EXAM_POS_09', 'Exam Scheduling', 'Schedule examination with valid future date and positive duration', 'Course & Subject exist', 'Exam Date: 2026-12-20, Time: 10:00 to 13:00 (180 mins)', 'Exam created in Scheduled state; active students enrolled', 'Pass', 'Equivalence Partitioning (EP)', 'Positive'),
            ('TC_ALLOC_POS_10', 'Allocation Engine', 'Sequential seat allocation when capacity exceeds student count', 'Exam has 30 students; Hall has 40 seats', 'Strategy: Sequential', 'All 30 students allocated; 0 unallocated; 10 remaining seats', 'Pass', 'Boundary Value Analysis (BVA)', 'Positive'),
            ('TC_ALLOC_POS_11', 'Allocation Engine', 'Randomized allocation produces reproducible arrangement with fixed seed', 'Exam CS601, Seed: 42', 'Execute allocation twice with Seed=42', 'Identical seat mappings produced on both executions', 'Pass', 'Reproducible Random Testing', 'Positive'),
            ('TC_ALLOC_POS_12', 'Allocation Engine', 'Mixed Course allocation interleaves students across adjacent desks', 'Students from Div A and Div B', 'Strategy: Mixed Course', 'Adjacent seats alternate between Div A and Div B', 'Pass', 'Combinatorial Testing', 'Positive'),
            ('TC_ALLOC_POS_13', 'Allocation Engine', 'Manual seat assignment to unblocked empty desk', 'Student S1, Seat H-101-R02-C03', 'Assign student manually', 'Seat allocated to S1; history logged with timestamp', 'Pass', 'Functional Testing', 'Positive'),
            ('TC_ALLOC_POS_14', 'Allocation Engine', 'Manual seat swap between two currently allocated students', 'Student S1 on Seat 1, Student S2 on Seat 2', 'Trigger swap between S1 and S2', 'Seats swapped cleanly without orphaned records', 'Pass', 'State Transition Testing', 'Positive'),
            ('TC_REP_POS_15', 'Reports & PDF', 'Generate and download official ReportLab examination seating PDF', 'Exam CS601 allocated', 'GET /admin/reports/exam/<id>/pdf', 'Valid 200 OK binary PDF streamed with header and student list', 'Pass', 'Output Verification', 'Positive'),

            # 15 Negative / Boundary / Edge Scenarios
            ('TC_AUTH_NEG_16', 'Authentication & Security', 'Reject login attempt with invalid password', 'User admin exists', 'Username: admin, Password: WrongPassword!', 'Authentication fails with error alert; no session created', 'Pass', 'Negative Testing', 'Negative'),
            ('TC_AUTH_NEG_17', 'Authentication & Security', 'Block unauthorized student access to admin dashboard URL', 'Authenticated as Student', 'GET /admin/dashboard', 'HTTP 403 Forbidden or redirect to login; access denied', 'Pass', 'Security Role Testing', 'Negative'),
            ('TC_STUD_NEG_18', 'Student Management', 'Reject duplicate enrollment number creation', 'Enrollment EN2026101 already exists', 'Attempt to insert second student with EN2026101', 'Rejected with unique constraint validation error', 'Pass', 'Unique Key Negative Testing', 'Negative'),
            ('TC_STUD_NEG_19', 'Student Management', 'Reject semester boundary value below 1', 'Student form submitted', 'Semester: 0', 'Form validation fails: Semester must be between 1 and 8', 'Pass', 'Boundary Value Analysis (Min - 1)', 'Negative'),
            ('TC_STUD_NEG_20', 'Student Management', 'Reject semester boundary value above 8', 'Student form submitted', 'Semester: 9', 'Form validation fails: Semester must be between 1 and 8', 'Pass', 'Boundary Value Analysis (Max + 1)', 'Negative'),
            ('TC_STUD_NEG_21', 'Student Management', 'Reject malformed student email address without domain', 'Student form submitted', 'Email: invalid_email_address', 'WTForms Email validator rejects input', 'Pass', 'Negative Testing & Sanitization', 'Negative'),
            ('TC_HALL_NEG_22', 'Hall Management', 'Reject hall dimensions with zero rows or negative columns', 'Hall form submitted', 'Rows: 0, Columns: -2', 'Form validation blocks submission with NumberRange error', 'Pass', 'Boundary Value Analysis (Zero/Negative)', 'Negative'),
            ('TC_HALL_NEG_23', 'Hall Management', 'Prevent blocking an occupied seat without clearing student first', 'Seat H-101-R01-C01 assigned to EN2026101', 'Attempt to toggle seat to Blocked', 'HTTP 409 Conflict: Seat currently assigned to candidate', 'Pass', 'Integrity Constraint Testing', 'Negative'),
            ('TC_EXAM_NEG_24', 'Exam Scheduling', 'Reject examination where end time is earlier than start time', 'Exam form submitted', 'Start Time: 14:00, End Time: 12:00', 'Validation Error: End time must be later than start time', 'Pass', 'Temporal Negative Testing', 'Negative'),
            ('TC_EXAM_NEG_25', 'Exam Scheduling', 'Prevent overlapping examination schedule for same course and semester', 'Exam 1 scheduled 10:00-13:00 on Dec 10', 'Schedule Exam 2 at 11:00 on Dec 10 for same semester', 'System raises schedule conflict error; blocks duplicate exam', 'Pass', 'Decision Table Testing', 'Negative'),
            ('TC_ALLOC_NEG_26', 'Allocation Engine', 'Reject allocation when student count strictly exceeds hall capacity', '50 students eligible; Hall has 40 seats', 'Strategy: Sequential', 'Atomic rollback: Insufficient seat capacity error; 0 records committed', 'Pass', 'Boundary Value Analysis (Capacity + 1)', 'Negative'),
            ('TC_ALLOC_NEG_27', 'Allocation Engine', 'Ensure blocked damaged seats are skipped during auto allocation', 'Seat H-101-R01-C03 is Blocked', 'Run auto allocation for 38 students', 'Seat R01-C03 is NOT allocated; candidates placed on unblocked seats', 'Pass', 'Negative Constraint Testing', 'Negative'),
            ('TC_ALLOC_NEG_28', 'Allocation Engine', 'Prevent assigning student to an examination they are not eligible for', 'Student S_ME is in Mechanical Sem 4', 'Attempt manual assignment of S_ME into CS601 exam', 'Rejected with eligibility violation error message', 'Pass', 'Business Rule Negative Testing', 'Negative'),
            ('TC_ALLOC_NEG_29', 'Allocation Engine', 'Prevent double allocation of the same student for same exam', 'Student EN2026101 already allocated seat 1', 'Manual assign student to seat 2', 'Reassignment relocates student or unique constraint blocks duplicate', 'Pass', 'Database Integrity Check', 'Negative'),
            ('TC_ALLOC_NEG_30', 'Allocation Engine', 'Prevent silent overwrite of existing valid allocation without confirmation', 'Exam has 30 allocated seats', 'Call allocation without force_reallocate flag', 'Rejects with warning: Confirm regeneration to clear existing records', 'Pass', 'Concurrency & Overwrite Guard', 'Negative'),

            # 12 Defect Regression Verification Test Cases
            ('TC_REG_01', 'Exam Scheduling', 'Detect timetable collision on exam modification', 'Exam 1 scheduled 10-12', 'Edit Exam 2 start to 11 on same date/course/sem', 'Collision flagged with warning; exam preserved', 'Pass', 'Regression / Decision Table', 'Negative'),
            ('TC_REG_02', 'Student Management', 'Handle in-batch duplicate CSV records', 'CSV uploaded with duplicate rows', 'CSV stream with identical enrollments', 'Valid rows committed; duplicates flagged per line', 'Pass', 'Regression / Batch Integrity', 'Negative'),
            ('TC_REG_03', 'Hall Management', 'Prevent hall resize truncating active seats', 'Hall has seat allocation at R5C6', 'Resize hall dimensions to 4x5', 'Rejected: Active seat allocation outside bounds', 'Pass', 'Regression / Boundary Integrity', 'Negative'),
            ('TC_REG_04', 'Academic Module', 'Prevent course deletion with linked exams', 'Course has scheduled exams', 'Delete course with 0 students', 'Prevent deletion; notify examinations linked', 'Pass', 'Regression / Referential Integrity', 'Negative'),
            ('TC_REG_05', 'Allocation Engine', 'Prevent allocation loss on capacity shortage', 'Exam has 5 allocated students', 'Force reallocate with 2-seat hall', 'Prior allocations preserved 100% intact', 'Pass', 'Regression / Transaction Safety', 'Negative'),
            ('TC_REG_06', 'Allocation Engine', 'Validate manual student choices on POST', 'Exam 2 has eligible students', 'POST manual seat assignment for Exam 2', 'Student choice accepted and seat assigned', 'Pass', 'Regression / Form State', 'Positive'),
            ('TC_REG_07', 'Invigilator Portal', 'Prevent IDOR access to unassigned halls', 'Invigilator assigned to Hall 1', 'Invigilator accesses unassigned Hall 2', 'HTTP 403 Forbidden returned', 'Pass', 'Security / BOLA Prevention', 'Negative'),
            ('TC_REG_08', 'Authentication', 'Sanitize login next redirect (CWE-601)', 'Login page opened', 'Login with next=https://attacker.com', 'Redirection constrained to internal dashboard', 'Pass', 'Security / Open Redirect', 'Negative'),
            ('TC_REG_09', 'Admin Dashboard', 'Calculate usable seats accurately', 'Inactive hall has 10 blocked seats', 'View admin dashboard', 'Dashboard reflects active usable capacity only', 'Pass', 'Mathematical Integrity', 'Positive'),
            ('TC_REG_10', 'App Architecture', 'Enforce HTTP defense-in-depth headers', 'Client makes GET request', 'Inspect response headers on all routes', 'Headers present: SAMEORIGIN, nosniff, etc.', 'Pass', 'Security / Clickjacking', 'Positive'),
            ('TC_REG_11', 'Student Management', 'Prevent email collision on student update', 'Student 1 has email st1@test.com', 'Update student 2 email to st1@test.com', 'Validation error; no unhandled 500 crash', 'Pass', 'Data Integrity / Validation', 'Negative'),
            ('TC_REG_12', 'Hall Management', 'Permit seat blocking for cancelled exams', 'Seat was in cancelled exam', 'Block desk in hall layout', 'Desk successfully blocked for maintenance', 'Pass', 'State Filter / Functional', 'Positive'),
        ]

        for code, mod, scen, pre, inp, exp, stat, tech, ttype in test_cases_seed:
            if not TestCase.query.filter_by(case_code=code).first():
                tc = TestCase(
                    case_code=code,
                    module=mod,
                    scenario=scen,
                    preconditions=pre,
                    test_input=inp,
                    expected_result=exp,
                    actual_result=exp if stat == 'Pass' else 'Observed test failure in controlled test environment',
                    test_technique=tech,
                    test_type=ttype,
                    status=stat,
                    tester_name='STQA QA Automation Engineer',
                    execution_date=datetime.utcnow()
                )
                db.session.add(tc)
        db.session.commit()

        # 12. Seed Real STQA Defect Reports (Controlled real-life defects from testing iterations)
        print("Seeding STQA defect reports...")
        defects_seed = [
            ('BUG_ALLOC_001', 'TC_ALLOC_NEG_26', 'Atomic rollback failed when student count exceeded capacity by 1',
             'When student count was 41 and capacity was 40, partial records were inserted before raising exception.',
             '1. Register 41 students.\n2. Select Hall with 40 seats.\n3. Execute auto allocation without try-catch rollback.',
             'Engine should validate total capacity before inserting any record and rollback transaction cleanly.',
             'Partial 40 records were committed while 1 student was left stranded.',
             'Critical', 'P1', 'Resolved', 'Lead Backend Engineer'),
            ('BUG_SCHED_002', 'TC_EXAM_NEG_25', 'Overlapping timetable conflict was not detected for same semester exams',
             'Students were able to be scheduled for two concurrent exams on the same date and time slot.',
             '1. Schedule CS601 from 10:00 to 13:00.\n2. Schedule CS602 from 11:00 to 14:00 on same date for same semester.',
             'System should block overlapping time interval for same class.',
             'Overlapping exam was saved successfully without warning.',
             'High', 'P2', 'Resolved', 'Lead Backend Engineer'),
            ('BUG_GRID_003', 'TC_HALL_NEG_23', 'Blocked damaged seat could be toggled while allocated in upcoming exam',
             'Toggling a seat to blocked allowed an occupied seat to be marked damaged without releasing the student.',
             '1. Allocate Student S1 to Seat R1C1.\n2. Open Hall Layout and click Block Seat R1C1.',
             'System should verify active allocations and forbid blocking an occupied desk.',
             'Seat changed to blocked while student allocation record remained intact.',
             'Medium', 'P2', 'Resolved', 'Frontend QA Engineer'),
            ('BUG_SCHED_004', 'TC_EXAM_NEG_25', 'Exam Edit Timetable Collision Bypass',
             'Editing an examination allowed changing time/date to collide with another scheduled exam for the same course and semester.',
             '1. Open scheduled exam.\n2. Edit start/end time to match another exam on same date.\n3. Submit form.',
             'Form validation rejects collision with warning.',
             'Exam saved without collision detection.',
             'High', 'P1', 'Resolved', 'Lead Backend Engineer'),
            ('BUG_DATA_005', 'TC_STUD_NEG_18', 'CSV Batch Import Unhandled Batch Rollback on Duplicate Row',
             'Uploading a CSV with duplicate enrollment numbers or emails within the same batch triggered IntegrityError at commit, rolling back valid rows.',
             '1. Upload CSV containing two rows with same enrollment or email.\n2. Submit import.',
             'Valid rows imported, duplicate rows flagged with line error.',
             '500 or entire batch rolled back with 0 students added.',
             'High', 'P2', 'Resolved', 'Lead Backend Engineer'),
            ('BUG_HALL_006', 'TC_HALL_NEG_22', 'Hall Resize Truncation of Active Seat Allocations',
             'Resizing a hall to smaller row/col dimensions only validated blocked seats, allowing active student allocations to fall out of physical bounds.',
             '1. Allocate student to R05-C06.\n2. Edit hall dimensions to 4x5.\n3. Submit.',
             'Rejection with warning that active allocations exist in truncated rows.',
             'Hall resized, leaving orphaned out-of-bounds seat allocations.',
             'High', 'P2', 'Resolved', 'Lead Backend Engineer'),
            ('BUG_ACAD_007', 'TC_EXAM_NEG_25', 'Course Deletion Integrity Crash with Scheduled Exams',
             'Deleting a course with 0 enrolled students but active examinations triggered unhandled 500 SQLite foreign key integrity error.',
             '1. Create course and schedule exam.\n2. Ensure 0 students enrolled.\n3. Delete course.',
             'Graceful validation rejection stating exams are linked.',
             'Unhandled 500 Foreign Key Integrity Error.',
             'Medium', 'P2', 'Resolved', 'Lead Backend Engineer'),
            ('BUG_ALLOC_008', 'TC_ALLOC_NEG_26', 'Data Loss in Force Reallocation on Insufficient Capacity',
             'Force re-allocation executed delete() and flush() before checking if selected halls had enough seats, destroying prior allocations permanently on failure.',
             '1. Allocate exam.\n2. Re-allocate selecting hall with insufficient capacity and force=True.',
             'Validation failure preserving prior allocation intact.',
             'Allocation failed and wiped all previous allocations permanently.',
             'Critical', 'P1', 'Resolved', 'Lead Backend Engineer'),
            ('BUG_ALLOC_009', 'TC_ALLOC_POS_13', 'Manual Allocation WTForms Choice Rejection for Non-First Exam',
             'Manual seat assignment initialized student choices using request.args. On POST without query params, choices defaulted to Exam 1, rejecting Exam 2 students.',
             '1. Go to manual allocation.\n2. Select Exam 2 and eligible student.\n3. Submit.',
             'Student assigned to target seat successfully.',
             'WTForms validation failed with Not a valid choice.',
             'High', 'P2', 'Resolved', 'Lead Frontend Engineer'),
            ('BUG_SEC_010', 'TC_AUTH_NEG_17', 'IDOR / BOLA Authorization Bypass in Invigilator Hall Roster',
             'Invigilator hall roster and PDF export endpoints lacked assignment ownership verification, allowing any logged-in invigilator to view any exam hall roster.',
             '1. Log in as invigilator.\n2. Change hall_id/exam_id in URL to unassigned hall.',
             'HTTP 403 Forbidden.',
             'Full attendance and seating sheet displayed.',
             'High', 'P1', 'Resolved', 'Security QA Engineer'),
            ('BUG_SEC_011', 'TC_AUTH_POS_01', 'CWE-601 Open Redirect Vulnerability in User Login',
             'Login next parameter validation only checked not next_page.startswith("/auth"), permitting external URL redirection to attacker domains.',
             '1. Visit /login?next=https://attacker.com.\n2. Enter valid credentials.\n3. Submit.',
             'Redirect to role-based dashboard.',
             'Redirected to external attacker site.',
             'Medium', 'P2', 'Resolved', 'Security QA Engineer'),
            ('BUG_DASH_012', 'TC_HALL_POS_07', 'Dashboard Usable Capacity Skewed by Inactive Hall Blocked Seats',
             'Admin dashboard calculated usable capacity by subtracting total blocked seats across all halls from active hall gross capacity.',
             '1. Decommission hall with blocked seats.\n2. Check dashboard usable capacity.',
             'Usable capacity equals sum of active halls usable seats.',
             'Usable capacity artificially deflated by inactive hall blocked seats.',
             'Low', 'P3', 'Resolved', 'Frontend QA Engineer'),
            ('BUG_SEC_013', 'TC_AUTH_POS_01', 'Missing Defensive HTTP Security Headers',
             'Application responses lacked X-Frame-Options, X-Content-Type-Options, and Referrer-Policy headers.',
             '1. Inspect HTTP response headers on any route.',
             'Headers present: SAMEORIGIN, nosniff, strict-origin-when-cross-origin.',
             'Headers completely missing.',
             'Medium', 'P3', 'Resolved', 'Security QA Engineer'),
            ('BUG_STUD_014', 'TC_STUD_NEG_18', 'Student Edit Profile Email Collision Integrity Crash',
             'Editing student details validated unique enrollment but did not check if updated email belonged to another student, crashing with IntegrityError.',
             '1. Edit student A.\n2. Set email to student B email.\n3. Save.',
             'Validation error: Email address is already used.',
             '500 Server Error due to UNIQUE constraint failed.',
             'Medium', 'P2', 'Resolved', 'Lead Backend Engineer'),
            ('BUG_HALL_015', 'TC_HALL_NEG_23', 'Hall Layout Seat Blocking False Positive on Cancelled Exams',
             'Attempting to block a seat previously allocated to a Cancelled or Completed exam was permanently blocked.',
             '1. Allocate exam.\n2. Cancel exam.\n3. Attempt to block that seat in hall layout.',
             'Seat toggle succeeds and desk is blocked.',
             'Error: Cannot block seat: Currently assigned in cancelled exam.',
             'Low', 'P3', 'Resolved', 'Frontend QA Engineer'),
        ]

        for bcode, tcode, title, desc, steps, exp, act, sev, pri, stat, assigned in defects_seed:
            if not DefectReport.query.filter_by(bug_code=bcode).first():
                tc_obj = TestCase.query.filter_by(case_code=tcode).first()
                tc_id = tc_obj.id if tc_obj else None
                dr = DefectReport(
                    bug_code=bcode,
                    test_case_id=tc_id,
                    title=title,
                    description=desc,
                    steps_to_reproduce=steps,
                    expected_result=exp,
                    actual_result=act,
                    severity=sev,
                    priority=pri,
                    status=stat,
                    assigned_to=assigned,
                    resolved_date=datetime.utcnow() if stat == 'Resolved' else None
                )
                db.session.add(dr)
        db.session.commit()

        # Activity log entry
        act_entry = ActivityLog(
            user_name='Database Seeder',
            action='Database Seed Completed',
            module='System Initialization',
            details=f"Seeded 60 students, 5 halls, 3 exams, 42 STQA test cases, and 15 defect reports.",
            ip_address='127.0.0.1'
        )
        db.session.add(act_entry)
        db.session.commit()
        print("Database seeding completed successfully!")


if __name__ == '__main__':
    seed()

