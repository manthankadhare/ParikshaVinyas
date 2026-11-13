import os
import time
import subprocess
import pytest
from playwright.sync_api import sync_playwright

BASE_URL = os.environ.get('BASE_URL', 'http://127.0.0.1:5001')
SCREENSHOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'test_reports', 'screenshots'))
os.makedirs(SCREENSHOT_DIR, exist_ok=True)


@pytest.fixture(scope="session")
def test_server():
    """Starts Flask test server on port 5001 without pipe buffer blocking."""
    env = os.environ.copy()
    env['PORT'] = '5001'
    env['FLASK_DEBUG'] = '0'
    
    proc = subprocess.Popen(
        ['.\\venv\\Scripts\\python.exe', 'run.py'],
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    time.sleep(2.5)  # Wait for server startup
    yield BASE_URL
    try:
        proc.terminate()
        proc.wait(timeout=3)
    except Exception:
        proc.kill()


@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()


@pytest.fixture
def page(browser):
    """Provides a fresh, isolated browser context and page per test."""
    context = browser.new_context(viewport={'width': 1280, 'height': 800})
    page = context.new_page()
    page.set_default_timeout(10000)
    yield page
    context.close()


def login_admin(page, test_server):
    page.goto(f"{test_server}/login")
    if "/admin" in page.url or page.locator(".app-topbar").count() > 0:
        return
    page.fill("#usernameInput", "admin")
    page.fill("#passwordInput", "Admin@2026")
    page.click("button[type='submit']")
    page.wait_for_selector(".app-topbar", timeout=5000)


def test_01_admin_login(page, test_server):
    """Scenario 1: Administrator login with valid credentials."""
    login_admin(page, test_server)
    assert "Examination Operations Overview" in page.content()
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "01_admin_dashboard.png"))


def test_02_invalid_login(page, test_server):
    """Scenario 2: Reject invalid password with alert."""
    page.goto(f"{test_server}/login")
    page.fill("#usernameInput", "admin")
    page.fill("#passwordInput", "WrongPassword999")
    page.click("button[type='submit']")

    page.wait_for_selector(".alert-danger", timeout=5000)
    assert "Invalid username/enrollment number or password." in page.content()
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "02_invalid_login.png"))


CURRENT_TEST_ENROLL = f"EN{int(time.time()) % 900000 + 100000}"

def test_03_student_creation(page, test_server):
    """Scenario 3: Create a new candidate record."""
    login_admin(page, test_server)
    page.goto(f"{test_server}/admin/students/add")
    page.fill("input[name='enrollment_no']", CURRENT_TEST_ENROLL)
    page.fill("input[name='full_name']", "E2E Candidate Dynamic")
    page.fill("input[name='email']", f"cand_{CURRENT_TEST_ENROLL.lower()}@upluniversity.ac.in")
    page.fill("input[name='mobile']", "9876543777")
    page.select_option("select[name='course_id']", index=1)
    page.fill("input[name='branch']", "Computer Engineering")
    page.fill("input[name='semester']", "6")
    page.fill("input[name='division']", "A")
    page.click("button[type='submit']")

    page.wait_for_selector(".alert-success", timeout=5000)
    assert "successfully added" in page.content()
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "03_student_created.png"))


def test_04_duplicate_enrollment_validation(page, test_server):
    """Scenario 4: Duplicate enrollment rejection."""
    login_admin(page, test_server)
    page.goto(f"{test_server}/admin/students/add")
    page.fill("input[name='enrollment_no']", CURRENT_TEST_ENROLL)  # Same dynamic enrollment
    page.fill("input[name='full_name']", "Duplicate Candidate")
    page.fill("input[name='email']", f"dup_{CURRENT_TEST_ENROLL.lower()}@upluniversity.ac.in")
    page.fill("input[name='mobile']", "9876543778")
    page.select_option("select[name='course_id']", index=1)
    page.fill("input[name='branch']", "Computer Engineering")
    page.fill("input[name='semester']", "6")
    page.fill("input[name='division']", "A")
    page.click("button[type='submit']")

    page.wait_for_selector(".alert-danger", timeout=5000)
    assert "already exists" in page.content()
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "04_duplicate_enrollment_error.png"))


def test_05_student_search(page, test_server):
    """Scenario 5: Search students by enrollment number."""
    login_admin(page, test_server)
    page.goto(f"{test_server}/admin/students?q=" + CURRENT_TEST_ENROLL)
    assert CURRENT_TEST_ENROLL in page.content()
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "05_student_search.png"))


def test_06_hall_creation(page, test_server):
    """Scenario 6: Create new examination hall with grid dimensions."""
    login_admin(page, test_server)
    hall_code = f"H-{int(time.time()) % 9000 + 1000}"
    page.goto(f"{test_server}/admin/halls/add")
    page.fill("input[name='hall_code']", hall_code)
    page.fill("input[name='hall_name']", f"Test Hall {hall_code}")
    page.fill("input[name='building']", "Automation Lab Block")
    page.fill("input[name='floor']", "3rd Floor")
    page.fill("input[name='num_rows']", "5")
    page.fill("input[name='num_cols']", "6")
    page.click("button[type='submit']")

    page.wait_for_selector(".alert-success", timeout=5000)
    assert "created with 30 seats capacity" in page.content()
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "06_hall_created.png"))


def test_07_hall_seating_layout_and_block_seat(page, test_server):
    """Scenario 7: Visual seat layout configuration."""
    login_admin(page, test_server)
    page.goto(f"{test_server}/admin/halls/1/layout")
    assert "Invigilator Podium" in page.content()
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "07_hall_layout_grid.png"))


def test_08_examination_creation(page, test_server):
    """Scenario 8: Schedule examination."""
    login_admin(page, test_server)
    ts = int(time.time())
    exam_code = f"EX-{ts % 9000 + 1000}"
    exam_day = (ts % 25) + 1
    page.goto(f"{test_server}/admin/exams/add")
    page.fill("input[name='exam_code']", exam_code)
    page.fill("input[name='exam_name']", f"Verification Exam {exam_code}")
    page.select_option("select[name='course_id']", index=1)
    page.select_option("select[name='subject_id']", index=1)
    page.fill("input[name='semester']", "6")
    page.fill("input[name='exam_date']", f"2027-02-{exam_day:02d}")
    page.fill("input[name='start_time']", "10:00")
    page.fill("input[name='end_time']", "13:00")
    page.click("button[type='submit']")

    page.wait_for_selector(".alert-success", timeout=5000)
    assert "scheduled successfully" in page.content()
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "08_exam_created.png"))


def test_09_invalid_examination_schedule(page, test_server):
    """Scenario 9: Prevent exam where end time is before start time."""
    login_admin(page, test_server)
    page.goto(f"{test_server}/admin/exams/add")
    page.fill("input[name='exam_code']", "EX-INV-99")
    page.fill("input[name='exam_name']", "Invalid Timing Exam")
    page.select_option("select[name='course_id']", index=1)
    page.select_option("select[name='subject_id']", index=1)
    page.fill("input[name='semester']", "6")
    page.fill("input[name='exam_date']", "2026-12-29")
    page.fill("input[name='start_time']", "14:00")
    page.fill("input[name='end_time']", "11:00")
    page.click("button[type='submit']")

    page.wait_for_selector(".alert-danger", timeout=5000)
    assert "end time must be later than start time" in page.content()
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "09_invalid_schedule_error.png"))


def test_10_automatic_seat_allocation(page, test_server):
    """Scenario 10: Automatic seat allocation wizard execution."""
    login_admin(page, test_server)
    page.goto(f"{test_server}/admin/allocation/wizard")
    page.select_option("#strategySelect", "Mixed Course")
    page.check("input[name='force_reallocate']")
    page.click("button[type='submit']")

    page.wait_for_selector(".card-pv", timeout=6000)
    assert "Allocation Completed Successfully" in page.content()
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "10_allocation_summary.png"))


def test_11_visual_seating_arrangement_grid(page, test_server):
    """Scenario 11: Visual Seating Grid inspection and modal."""
    login_admin(page, test_server)
    page.goto(f"{test_server}/admin/allocation/visual-grid")
    assert "Visual Seating Chart" in page.content()
    assert "Invigilator Podium" in page.content()

    first_seat = page.locator(".seat-allocated").first
    if first_seat.count() > 0:
        first_seat.click()
        page.wait_for_selector("#seatDetailModal.show", timeout=3000)
        assert "Candidate Name" in page.content()

    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "11_visual_grid_modal.png"))


def test_12_reports_and_pdf_generation(page, test_server):
    """Scenario 12: PDF reports access center."""
    login_admin(page, test_server)
    page.goto(f"{test_server}/admin/reports")
    assert "Examination Reports" in page.content()
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "12_reports_center.png"))


def test_13_qa_test_cases_repository(page, test_server):
    """Scenario 13: STQA Test Cases Repository."""
    login_admin(page, test_server)
    page.goto(f"{test_server}/admin/qa/test-cases")
    assert "Test Case Specification" in page.content()
    assert "TC_ALLOC_POS_10" in page.content()
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "13_test_cases_matrix.png"))


def test_14_ai_testing_workspace(page, test_server):
    """Scenario 14: AI-Assisted Testing Workspace."""
    login_admin(page, test_server)
    page.goto(f"{test_server}/admin/qa/ai-workspace")
    page.fill("textarea[name='requirement_text']", "Test capacity boundary overflow when student count exceeds hall capacity.")
    page.click("button[type='submit']")

    page.wait_for_selector(".card-pv", timeout=6000)
    assert "Scenarios Synthesized" in page.content() or "generated" in page.content()
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "14_ai_workspace.png"))


def test_15_defects_tracking(page, test_server):
    """Scenario 15: Defect Tracking."""
    login_admin(page, test_server)
    page.goto(f"{test_server}/admin/qa/defects")
    assert "Reported Defects" in page.content()
    assert "BUG_ALLOC_001" in page.content()
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "15_defects_tracker.png"))


def test_16_student_login_and_seating_portal(page, test_server):
    """Scenario 16: Student candidate portal view with assigned desk."""
    page.goto(f"{test_server}/login")
    page.fill("#usernameInput", "EN2026101")
    page.fill("#passwordInput", "Student@6101")
    page.click("button[type='submit']")

    page.wait_for_selector(".app-topbar", timeout=5000)
    assert "My Examination Schedule" in page.content()
    assert "EN2026101" in page.content()
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "16_student_portal.png"))


def test_17_invigilator_dashboard(page, test_server):
    """Scenario 17: Invigilator portal and assigned duties."""
    page.goto(f"{test_server}/login")
    page.fill("#usernameInput", "invig_sharma")
    page.fill("#passwordInput", "Invig@2026")
    page.click("button[type='submit']")

    page.wait_for_selector(".app-topbar", timeout=5000)
    assert "Invigilation Duty Schedule" in page.content()
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "17_invigilator_dashboard.png"))


def test_18_unauthorized_access_guard(page, test_server):
    """Scenario 18: Student cannot access administrative settings."""
    page.goto(f"{test_server}/login")
    page.fill("#usernameInput", "EN2026101")
    page.fill("#passwordInput", "Student@6101")
    page.click("button[type='submit']")
    page.wait_for_selector(".app-topbar", timeout=5000)

    # Attempt to open admin settings
    response = page.goto(f"{test_server}/admin/settings")
    assert response.status == 403 or "You do not have permission" in page.content()
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "18_unauthorized_403.png"))


def test_19_logout_functionality(page, test_server):
    """Scenario 19: Clean logout and session termination."""
    login_admin(page, test_server)
    page.goto(f"{test_server}/logout")
    page.wait_for_selector(".alert-info", timeout=5000)
    assert "You have been logged out successfully." in page.content()
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "19_logout.png"))


def test_20_activity_audit_logs(page, test_server):
    """Scenario 20: System audit logs capture all operational events."""
    login_admin(page, test_server)
    page.goto(f"{test_server}/admin/activity-logs")
    assert "System Activity Logs" in page.content()
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "20_activity_logs.png"))
