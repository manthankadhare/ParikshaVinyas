import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from datetime import datetime
from app import create_app, db
from app.models.qa import DefectReport

app = create_app()
with app.app_context():
    defects_data = [
        ('BUG_SCHED_004', 'Exam Edit Timetable Collision Bypass',
         'Editing an examination allowed changing time/date to collide with another scheduled exam for the same course and semester.',
         '1. Open scheduled exam. 2. Edit start/end time to match another exam on same date. 3. Submit form.',
         'Form validation rejects collision with warning.',
         'Exam saved without collision detection.', 'High', 'P1'),

        ('BUG_DATA_005', 'CSV Batch Import Unhandled Batch Rollback on Duplicate Row',
         'Uploading a CSV with duplicate enrollment numbers or emails within the same batch triggered IntegrityError at commit, rolling back valid rows.',
         '1. Upload CSV containing two rows with same enrollment or email. 2. Submit import.',
         'Valid rows imported, duplicate rows flagged with line error.',
         '500 or entire batch rolled back with 0 students added.', 'High', 'P2'),

        ('BUG_HALL_006', 'Hall Resize Truncation of Active Seat Allocations',
         'Resizing a hall to smaller row/col dimensions only validated blocked seats, allowing active student allocations to fall out of physical bounds.',
         '1. Allocate student to R05-C06. 2. Edit hall dimensions to 4x5. 3. Submit.',
         'Rejection with warning that active allocations exist in truncated rows.',
         'Hall resized, leaving orphaned out-of-bounds seat allocations.', 'High', 'P2'),

        ('BUG_ACAD_007', 'Course Deletion Integrity Crash with Scheduled Exams',
         'Deleting a course with 0 enrolled students but active examinations triggered unhandled 500 SQLite foreign key integrity error.',
         '1. Create course and schedule exam. 2. Ensure 0 students enrolled. 3. Delete course.',
         'Graceful validation rejection stating exams are linked.',
         'Unhandled 500 Foreign Key Integrity Error.', 'Medium', 'P2'),

        ('BUG_ALLOC_008', 'Data Loss in Force Reallocation on Insufficient Capacity',
         'Force re-allocation executed delete() and flush() before checking if selected halls had enough seats, destroying prior allocations permanently on failure.',
         '1. Allocate exam. 2. Re-allocate selecting hall with insufficient capacity and force=True.',
         'Validation failure preserving prior allocation intact.',
         'Allocation failed and wiped all previous allocations permanently.', 'Critical', 'P1'),

        ('BUG_ALLOC_009', 'Manual Allocation WTForms Choice Rejection for Non-First Exam',
         'Manual seat assignment initialized student choices using request.args. On POST without query params, choices defaulted to Exam 1, rejecting Exam 2 students.',
         '1. Go to manual allocation. 2. Select Exam 2 and eligible student. 3. Submit.',
         'Student assigned to target seat successfully.',
         'WTForms validation failed with Not a valid choice.', 'High', 'P2'),

        ('BUG_SEC_010', 'IDOR / BOLA Authorization Bypass in Invigilator Hall Roster',
         'Invigilator hall roster and PDF export endpoints lacked assignment ownership verification, allowing any logged-in invigilator to view any exam hall roster.',
         '1. Log in as invigilator. 2. Change hall_id/exam_id in URL to unassigned hall.',
         'HTTP 403 Forbidden.',
         'Full attendance and seating sheet displayed.', 'High', 'P1'),

        ('BUG_SEC_011', 'CWE-601 Open Redirect Vulnerability in User Login',
         'Login next parameter validation only checked not next_page.startswith("/auth"), permitting external URL redirection to attacker domains.',
         '1. Visit /login?next=https://attacker.com. 2. Enter valid credentials. 3. Submit.',
         'Redirect to role-based dashboard.',
         'Redirected to external attacker site.', 'Medium', 'P2'),

        ('BUG_DASH_012', 'Dashboard Usable Capacity Skewed by Inactive Hall Blocked Seats',
         'Admin dashboard calculated usable capacity by subtracting total blocked seats across all halls from active hall gross capacity.',
         '1. Decommission hall with blocked seats. 2. Check dashboard usable capacity.',
         'Usable capacity equals sum of active halls usable seats.',
         'Usable capacity artificially deflated by inactive hall blocked seats.', 'Low', 'P3'),

        ('BUG_SEC_013', 'Missing Defensive HTTP Security Headers',
         'Application responses lacked X-Frame-Options, X-Content-Type-Options, and Referrer-Policy headers.',
         '1. Inspect HTTP response headers on any route.',
         'Headers present: SAMEORIGIN, nosniff, strict-origin-when-cross-origin.',
         'Headers completely missing.', 'Medium', 'P3'),

        ('BUG_STUD_014', 'Student Edit Profile Email Collision Integrity Crash',
         'Editing student details validated unique enrollment but did not check if updated email belonged to another student, crashing with IntegrityError.',
         '1. Edit student A. 2. Set email to student B email. 3. Save.',
         'Validation error: Email address is already used.',
         '500 Server Error due to UNIQUE constraint failed.', 'Medium', 'P2'),

        ('BUG_HALL_015', 'Hall Layout Seat Blocking False Positive on Cancelled Exams',
         'Attempting to block a seat previously allocated to a Cancelled or Completed exam was permanently blocked.',
         '1. Allocate exam. 2. Cancel exam. 3. Attempt to block that seat in hall layout.',
         'Seat toggle succeeds and desk is blocked.',
         'Error: Cannot block seat: Currently assigned in cancelled exam.', 'Low', 'P3'),
    ]

    for code, title, desc, steps, exp, act, sev, prio in defects_data:
        if not DefectReport.query.filter_by(bug_code=code).first():
            d = DefectReport(
                bug_code=code, title=title, description=desc, steps_to_reproduce=steps,
                expected_result=exp, actual_result=act, severity=sev, priority=prio,
                status='Resolved', assigned_to='Senior QA & Full-Stack Lead',
                resolved_date=datetime.utcnow()
            )
            db.session.add(d)
    db.session.commit()
    print('Total Defect Reports in DB now:', DefectReport.query.count())
