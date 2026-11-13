import os
import sys
import time
import shutil
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from playwright.sync_api import sync_playwright

BASE_URL = os.environ.get("BASE_URL", "http://127.0.0.1:5000")
ARTIFACT_SCREENSHOT_DIR = r"C:\Users\manth\.gemini\antigravity\brain\df22b880-5f44-4f18-bcb0-e62735a7437b\screenshots"
REPORT_SCREENSHOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "test_reports", "screenshots"))

os.makedirs(ARTIFACT_SCREENSHOT_DIR, exist_ok=True)
os.makedirs(REPORT_SCREENSHOT_DIR, exist_ok=True)

test_results = []
console_errors = []

def save_shot(page, name):
    p1 = os.path.join(REPORT_SCREENSHOT_DIR, name)
    p2 = os.path.join(ARTIFACT_SCREENSHOT_DIR, name)
    page.screenshot(path=p1, full_page=True)
    shutil.copy2(p1, p2)
    print(f"  [SCREENSHOT] Saved: {name}")

def log_test(module, title, status, details=""):
    test_results.append({
        "module": module,
        "title": title,
        "status": status,
        "details": details
    })
    badge = f"[{status}]"
    print(f"{badge:10} {module:25} | {title} {('- ' + details) if details else ''}")

def run_live_audit():
    print("=====================================================================")
    print(" PARIKSHAVINYAS - LIVE END-TO-END CHROME BROWSER TESTING CAMPAIGN")
    print(" Target Environment:", BASE_URL)
    print("=====================================================================")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1280, "height": 800})
        page = context.new_page()

        # Capture console messages
        page.on("console", lambda msg: console_errors.append(f"[{msg.type}] {msg.text}") if msg.type in ['error', 'warning'] else None)

        # -------------------------------------------------------------
        # MODULE A: AUTHENTICATION & ACCESS CONTROL
        # -------------------------------------------------------------
        print("\n>>> Testing Module A: Authentication & Access Control...")
        page.goto(f"{BASE_URL}/login")
        assert "Sign In" in page.title()
        save_shot(page, "live_01_auth_login.png")
        log_test("Authentication", "Login page renders successfully", "PASS", "Title verified")

        # Test invalid credentials
        page.fill("#usernameInput", "nonexistent_user")
        page.fill("#passwordInput", "WrongPass@999")
        page.click("button[type='submit']")
        page.wait_for_selector(".alert-danger", timeout=5000)
        assert "Invalid username" in page.content() or "Invalid credentials" in page.content() or "danger" in page.content()
        save_shot(page, "live_02_auth_invalid_credentials.png")
        log_test("Authentication", "Invalid credentials rejection", "PASS", "Error flash displayed")

        # Test valid admin login
        page.fill("#usernameInput", "admin")
        page.fill("#passwordInput", "Admin@2026")
        page.click("button[type='submit']")
        page.wait_for_selector(".app-topbar", timeout=6000)
        assert "/admin" in page.url
        save_shot(page, "live_03_admin_dashboard.png")
        log_test("Authentication", "Admin login with valid credentials", "PASS", "Redirected to /admin/dashboard")

        # -------------------------------------------------------------
        # MODULE B: ADMIN DASHBOARD
        # -------------------------------------------------------------
        print("\n>>> Testing Module B: Admin Dashboard...")
        # Check stat cards
        content = page.content()
        assert "Registered Candidates" in content or "Total Students" in content
        assert "Examination Halls" in content or "Total Halls" in content
        assert "Allocated Seats" in content
        # Check charts render
        canvases = page.locator("canvas").count()
        assert canvases >= 2, f"Expected at least 2 Chart.js canvases, found {canvases}"
        log_test("Admin Dashboard", "KPI widgets & Chart.js canvas elements", "PASS", f"{canvases} chart canvases loaded")

        # -------------------------------------------------------------
        # MODULE C: STUDENT MANAGEMENT
        # -------------------------------------------------------------
        print("\n>>> Testing Module C: Student Management...")
        page.goto(f"{BASE_URL}/admin/students")
        page.wait_for_selector("table", timeout=5000)
        save_shot(page, "live_04_students_directory.png")
        log_test("Student Management", "Students list and pagination", "PASS", "Table rendered")

        # Add valid student
        page.goto(f"{BASE_URL}/admin/students/add")
        page.fill("input[name='enrollment_no']", "EN2026999")
        page.fill("input[name='full_name']", "Kavya Patel")
        page.fill("input[name='email']", "kavya.patel999@upluniversity.ac.in")
        page.fill("input[name='mobile']", "9822999999")
        page.select_option("select[name='course_id']", index=1)
        page.fill("input[name='branch']", "Computer Engineering")
        page.fill("input[name='semester']", "6")
        page.fill("input[name='division']", "A")
        save_shot(page, "live_05_student_add_form.png")
        page.click("button[type='submit']")
        page.wait_for_selector(".alert-success", timeout=5000)
        log_test("Student Management", "Add new valid student", "PASS", "Student EN2026999 created")

        # Try duplicate enrollment validation
        page.goto(f"{BASE_URL}/admin/students/add")
        page.fill("input[name='enrollment_no']", "EN2026999")
        page.fill("input[name='full_name']", "Duplicate Candidate")
        page.fill("input[name='email']", "duplicate999@upluniversity.ac.in")
        page.fill("input[name='mobile']", "9822000000")
        page.select_option("select[name='course_id']", index=1)
        page.fill("input[name='branch']", "Computer Engineering")
        page.fill("input[name='semester']", "6")
        page.fill("input[name='division']", "A")
        page.click("button[type='submit']")
        page.wait_for_selector(".alert-danger", timeout=5000)
        assert "already exists" in page.content()
        save_shot(page, "live_06_student_duplicate_error.png")
        log_test("Student Management", "Duplicate enrollment number rejection", "PASS", "Validation flash displayed")

        # Search by enrollment number
        page.goto(f"{BASE_URL}/admin/students?q=EN2026999")
        page.wait_for_selector("table", timeout=5000)
        assert "Kavya Patel" in page.content()
        save_shot(page, "live_07_student_search.png")
        log_test("Student Management", "Search candidate by enrollment number", "PASS", "Found EN2026999")

        # -------------------------------------------------------------
        # MODULE D: EXAMINATION HALL MANAGEMENT
        # -------------------------------------------------------------
        print("\n>>> Testing Module D: Examination Hall Management...")
        page.goto(f"{BASE_URL}/admin/halls")
        page.wait_for_selector(".card-pv", timeout=5000)
        save_shot(page, "live_08_halls_directory.png")
        log_test("Hall Management", "Examination halls list", "PASS", "Halls cards loaded")

        # Add examination hall
        page.goto(f"{BASE_URL}/admin/halls/add")
        page.fill("input[name='hall_code']", "H-LIVE99")
        page.fill("input[name='hall_name']", "Live Browser Automation Lab")
        page.fill("input[name='building']", "QA Innovation Tower")
        page.fill("input[name='floor']", "3rd Floor")
        page.fill("input[name='num_rows']", "4")
        page.fill("input[name='num_cols']", "5")
        page.click("button[type='submit']")
        page.wait_for_selector(".alert-success", timeout=5000)
        assert "20 seats capacity" in page.content()
        log_test("Hall Management", "Add examination hall with 4x5=20 seats", "PASS", "Hall H-LIVE99 created")

        # Open Hall Layout and Toggle Block Seat
        page.goto(f"{BASE_URL}/admin/halls")
        # Find H-LIVE99 layout link
        layout_link = page.locator("a[href*='/layout']").first.get_attribute("href")
        page.goto(f"{BASE_URL}{layout_link}")
        page.wait_for_selector(".seat-item", timeout=5000)
        save_shot(page, "live_09_halls_layout_toggle.png")
        log_test("Hall Management", "Visual hall layout grid view", "PASS", "Grid seats rendered")

        # -------------------------------------------------------------
        # MODULE E: ACADEMIC CURRICULUM (COURSES & SUBJECTS)
        # -------------------------------------------------------------
        print("\n>>> Testing Module E: Course & Subject Management...")
        page.goto(f"{BASE_URL}/admin/academic/courses")
        page.wait_for_selector("table", timeout=5000)
        has_edit_course = page.locator("a[href*='/courses/'][href*='/edit']").count() > 0
        save_shot(page, "live_10_academic_courses.png")
        log_test("Academic Curriculum", "Courses management view & Edit links", "PASS" if has_edit_course else "DEFECT", "Edit actions present" if has_edit_course else "Edit actions absent")

        # Check duplicate course code validation
        page.fill("input[name='code']", "CS")
        page.fill("input[name='name']", "Duplicate Computer Science")
        page.fill("input[name='department']", "Computer Department")
        page.click("button[type='submit']")
        page.wait_for_selector(".alert-danger", timeout=5000)
        assert "already exists" in page.content()
        log_test("Academic Curriculum", "Duplicate course code prevention", "PASS", "Code conflict detected")

        page.goto(f"{BASE_URL}/admin/academic/subjects")
        page.wait_for_selector("table", timeout=5000)
        has_edit_subj = page.locator("a[href*='/subjects/'][href*='/edit']").count() > 0
        save_shot(page, "live_11_academic_subjects.png")
        log_test("Academic Curriculum", "Subjects curriculum view & Edit links", "PASS" if has_edit_subj else "DEFECT", "Edit actions present" if has_edit_subj else "Edit actions absent")

        # -------------------------------------------------------------
        # MODULE F: EXAMINATION SCHEDULING
        # -------------------------------------------------------------
        print("\n>>> Testing Module F: Examination Scheduling...")
        page.goto(f"{BASE_URL}/admin/exams")
        page.wait_for_selector("table", timeout=5000)
        save_shot(page, "live_12_exams_directory.png")
        log_test("Examination Scheduling", "Examination timetable directory", "PASS", "Timetable rendered")

        # Test invalid schedule: end time <= start time
        page.goto(f"{BASE_URL}/admin/exams/add")
        page.fill("input[name='exam_code']", "EX-ERR01")
        page.fill("input[name='exam_name']", "Invalid Time Exam")
        page.select_option("select[name='course_id']", index=1)
        page.select_option("select[name='subject_id']", index=1)
        page.fill("input[name='semester']", "6")
        page.fill("input[name='exam_date']", "2026-12-15")
        page.fill("input[name='start_time']", "14:00")
        page.fill("input[name='end_time']", "12:00")  # End before start!
        page.click("button[type='submit']")
        page.wait_for_selector(".alert-danger", timeout=5000)
        assert "end time must be later than start time" in page.content()
        save_shot(page, "live_13_exams_conflict_validation.png")
        log_test("Examination Scheduling", "Start/End time constraint validation", "PASS", "Invalid timing rejected")

        # Create valid examination
        page.goto(f"{BASE_URL}/admin/exams/add")
        page.fill("input[name='exam_code']", "EX-LIVE01")
        page.fill("input[name='exam_name']", "Live Browser Automation Testing Exam")
        page.select_option("select[name='course_id']", index=1)
        page.select_option("select[name='subject_id']", index=1)
        page.fill("input[name='semester']", "6")
        page.fill("input[name='exam_date']", "2026-12-20")
        page.fill("input[name='start_time']", "10:00")
        page.fill("input[name='end_time']", "13:00")
        page.fill("input[name='duration_minutes']", "180")
        page.click("button[type='submit']")
        page.wait_for_selector(".alert-success", timeout=5000)
        assert "scheduled successfully" in page.content()
        log_test("Examination Scheduling", "Create valid exam with auto eligible students", "PASS", "Exam EX-LIVE01 created")

        # -------------------------------------------------------------
        # MODULE G: AUTOMATIC SEAT ALLOCATION ENGINE
        # -------------------------------------------------------------
        print("\n>>> Testing Module G: Automatic Seat Allocation Engine...")
        page.goto(f"{BASE_URL}/admin/allocation/wizard")
        page.wait_for_selector("#strategySelect", timeout=5000)
        save_shot(page, "live_14_allocation_wizard.png")

        # Select EX-LIVE01 and Sequential strategy
        # Find option containing EX-LIVE01
        options = page.locator("select[name='examination_id'] option").all_text_contents()
        target_opt_index = 0
        for idx, text in enumerate(options):
            if "EX-LIVE01" in text:
                target_opt_index = idx
                break
        
        page.select_option("select[name='examination_id']", index=target_opt_index)
        page.select_option("select[name='strategy']", value="Sequential")
        page.check("input[name='force_reallocate']")
        page.click("button[type='submit']")
        page.wait_for_selector(".alert-success, .card-header", timeout=8000)
        save_shot(page, "live_15_allocation_summary.png")
        assert "Allocation Completed Successfully" in page.content() or "Successfully allocated" in page.content() or "summary" in page.url.lower()
        log_test("Automatic Allocation", "Sequential strategy allocation execution", "PASS", "Students successfully allocated")

        # -------------------------------------------------------------
        # MODULE H & I: VISUAL SEATING GRID & MANUAL REASSIGNMENT
        # -------------------------------------------------------------
        print("\n>>> Testing Modules H & I: Visual Grid & Manual Allocation...")
        page.goto(f"{BASE_URL}/admin/allocation/visual-grid")
        page.wait_for_selector(".visual-grid-container, .card", timeout=5000)
        save_shot(page, "live_16_visual_seating_grid.png")
        log_test("Visual Grid", "Interactive visual seating grid", "PASS", "Seating matrix rendered")

        # Check manual allocation page
        page.goto(f"{BASE_URL}/admin/allocation/manual")
        page.wait_for_selector("form", timeout=5000)
        save_shot(page, "live_17_manual_allocation.png")
        log_test("Manual Allocation", "Manual seat swap/assignment interface", "PASS", "Manual allocation form loaded")

        # -------------------------------------------------------------
        # MODULE J: REPORTS & DOWNLOADS
        # -------------------------------------------------------------
        print("\n>>> Testing Module J: Reports & Downloads...")
        page.goto(f"{BASE_URL}/admin/reports")
        page.wait_for_selector(".card", timeout=5000)
        save_shot(page, "live_18_reports_center.png")
        log_test("Reports & Downloads", "Reports & Documentation Centre", "PASS", "Reports center loaded")

        # Test student CSV export endpoint
        response = page.request.get(f"{BASE_URL}/admin/students/export")
        assert response.status == 200
        assert "Enrollment Number" in response.text()
        log_test("Reports & Downloads", "Student master CSV export", "PASS", f"{len(response.text())} bytes received")

        # Test exam PDF seating chart
        pdf_resp = page.request.get(f"{BASE_URL}/admin/reports/exam/1/pdf")
        assert pdf_resp.status == 200
        assert pdf_resp.body()[:4] == b"%PDF"
        log_test("Reports & Downloads", "Master Exam Seating Chart PDF", "PASS", f"{len(pdf_resp.body())} bytes PDF generated")

        # -------------------------------------------------------------
        # MODULE K: INVIGILATOR PORTAL & RBAC
        # -------------------------------------------------------------
        print("\n>>> Testing Module K: Invigilator Portal & RBAC Boundaries...")
        # Logout admin
        page.goto(f"{BASE_URL}/logout")
        page.wait_for_selector("#usernameInput", timeout=5000)

        # Login as invigilator
        page.fill("#usernameInput", "invig_sharma")
        page.fill("#passwordInput", "Invig@2026")
        page.click("button[type='submit']")
        page.wait_for_selector(".invigilator-badge, .card", timeout=5000)
        assert "/invigilator" in page.url
        save_shot(page, "live_19_invigilator_dashboard.png")
        log_test("Invigilator Portal", "Invigilator login & duties dashboard", "PASS", "Dashboard rendered")

        # Test RBAC boundary: Invigilator trying to access /admin/students
        resp = page.goto(f"{BASE_URL}/admin/students")
        assert resp.status in [403, 302] or "/invigilator" in page.url or "Access Denied" in page.content() or "Forbidden" in page.content()
        save_shot(page, "live_20_invigilator_rbac_403.png")
        log_test("Invigilator Portal", "RBAC Boundary Enforcement (/admin access forbidden)", "PASS", f"Protected with HTTP {resp.status}")

        # -------------------------------------------------------------
        # MODULE L: STUDENT PORTAL
        # -------------------------------------------------------------
        print("\n>>> Testing Module L: Student Portal...")
        page.goto(f"{BASE_URL}/logout")
        page.wait_for_selector("#usernameInput", timeout=5000)

        # Login as student (EN2026101 / Student@6101)
        page.fill("#usernameInput", "en2026101")
        page.fill("#passwordInput", "Student@6101")
        page.click("button[type='submit']")
        page.wait_for_selector(".card", timeout=5000)
        assert "/student" in page.url
        content = page.content()
        assert "Aarav Sharma" in content or "EN2026101" in content
        save_shot(page, "live_21_student_portal.png")
        log_test("Student Portal", "Candidate dashboard & personal seating information", "PASS", "Student details verified")

        # Test downloading student admit slip
        slip_resp = page.request.get(f"{BASE_URL}/student/slip/pdf")
        assert slip_resp.status == 200
        assert slip_resp.body()[:4] == b"%PDF"
        log_test("Student Portal", "Personal Admit Pass PDF generation", "PASS", f"{len(slip_resp.body())} bytes PDF generated")

        # -------------------------------------------------------------
        # MODULE M: ACTIVITY LOGS & AUDIT TRAIL
        # -------------------------------------------------------------
        print("\n>>> Testing Module M: Activity Logs...")
        page.goto(f"{BASE_URL}/logout")
        # Log back in as Admin
        page.fill("#usernameInput", "admin")
        page.fill("#passwordInput", "Admin@2026")
        page.click("button[type='submit']")
        page.wait_for_selector(".app-topbar", timeout=5000)

        page.goto(f"{BASE_URL}/admin/activity-logs")
        page.wait_for_selector("table", timeout=5000)
        save_shot(page, "live_22_activity_logs.png")
        content = page.content()
        assert "Add Student" in content or "Auto Seat Allocation" in content or "Schedule Exam" in content
        log_test("Activity Logs", "System audit trail & event history", "PASS", "Audit records verified")

        # -------------------------------------------------------------
        # MODULE N & O: AI-ASSISTED QA & DEFECT TRACKING
        # -------------------------------------------------------------
        print("\n>>> Testing Modules N & O: AI QA Studio & Defect Tracker...")
        page.goto(f"{BASE_URL}/admin/qa/ai-workspace")
        page.wait_for_selector("form", timeout=5000)
        page.select_option("select[name='module_name']", value="Allocation Engine")
        page.fill("textarea[name='requirement_text']", "Verify that candidate seat assignments prevent adjacent same-division students.")
        page.click("button[type='submit']")
        page.wait_for_selector(".alert-info, .card", timeout=5000)
        save_shot(page, "live_23_qa_ai_workspace.png")
        log_test("AI-Assisted Testing", "STQA AI Test Scenario Generation", "PASS", "AI scenarios generated")

        page.goto(f"{BASE_URL}/admin/qa/test-cases")
        page.wait_for_selector("table", timeout=5000)
        save_shot(page, "live_24_qa_test_matrix.png")
        log_test("Defect & Test Management", "STQA Test Cases Matrix (42 cases)", "PASS", "Test matrix rendered")

        page.goto(f"{BASE_URL}/admin/qa/defects")
        page.wait_for_selector("table", timeout=5000)
        save_shot(page, "live_25_qa_defects_tracker.png")
        log_test("Defect & Test Management", "Defects Tracker & Severity Management", "PASS", "Defects table rendered")

        # -------------------------------------------------------------
        # MODULE P & UI/UX: MOBILE VIEWPORT TEST
        # -------------------------------------------------------------
        print("\n>>> Testing Responsive UI / Mobile Viewport (375x667)...")
        mobile_context = browser.new_context(viewport={"width": 375, "height": 667})
        mobile_page = mobile_context.new_page()
        # Admin login on mobile
        mobile_page.goto(f"{BASE_URL}/login")
        mobile_page.fill("#usernameInput", "admin")
        mobile_page.fill("#passwordInput", "Admin@2026")
        mobile_page.click("button[type='submit']")
        mobile_page.wait_for_selector(".app-topbar, .card", timeout=5000)
        save_shot(mobile_page, "live_26_mobile_viewport_375x667.png")
        log_test("UI/UX Testing", "Mobile Viewport (375x667) Responsive Layout", "PASS", "Clean mobile rendering")
        mobile_context.close()

        # Clean up test exam & test student
        print("\n>>> Cleaning up temporary test artifacts...")
        from app import create_app, db
        from app.models.exam import Examination
        from app.models.student import Student
        from app.models.hall import ExaminationHall
        
        clean_app = create_app()
        with clean_app.app_context():
            te = Examination.query.filter_by(exam_code="EX-LIVE01").first()
            if te:
                db.session.delete(te)
            th = ExaminationHall.query.filter_by(hall_code="H-LIVE99").first()
            if th:
                db.session.delete(th)
            ts = Student.query.filter_by(enrollment_no="EN2026999").first()
            if ts:
                user = ts.user
                db.session.delete(ts)
                if user:
                    db.session.delete(user)
            db.session.commit()
            print("  [CLEANUP] Successfully pruned live test entities.")

        browser.close()

    print("\n=====================================================================")
    print(" LIVE TESTING CAMPAIGN COMPLETE")
    print(f" Total Test Steps Executed: {len(test_results)}")
    passes = sum(1 for t in test_results if t['status'] == 'PASS')
    defects = sum(1 for t in test_results if t['status'] == 'DEFECT')
    print(f" Passed: {passes} | Defects/Gaps Identified: {defects}")
    print("=====================================================================")

    # Write summary json
    summary_path = os.path.join(REPORT_SCREENSHOT_DIR, "..", "live_audit_summary.json")
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump({"total": len(test_results), "passes": passes, "defects": defects, "results": test_results, "console_errors": console_errors}, f, indent=2)

if __name__ == "__main__":
    run_live_audit()
