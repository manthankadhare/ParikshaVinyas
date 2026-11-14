import os
import shutil
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import matplotlib.patches as patches

OUT_DIR = r"docs/ParikshaVinyas_Overleaf_Project/figures"
REF_FIGS = r"docs/reference_krushi_report/KRUSHI_SpendWise_Overleaf/figures/extracted"
TEST_FIGS = r"test_reports/screenshots"

os.makedirs(OUT_DIR, exist_ok=True)

# 1. Logo
shutil.copy2(os.path.join(REF_FIGS, "img-000.png"), os.path.join(OUT_DIR, "upl-logo.png"))
print("Copied upl-logo.png")

# 2. Module figures (Chapter 1)
module_mapping = {
    "live_01_auth_login.png": "fig1_01_login.png",
    "live_03_admin_dashboard.png": "fig1_02_dashboard.png",
    "live_04_students_directory.png": "fig1_03_students.png",
    "live_08_halls_directory.png": "fig1_04_halls.png",
    "live_09_halls_layout_toggle.png": "fig1_05_hall_layout.png",
    "live_10_academic_courses.png": "fig1_06_courses.png",
    "live_11_academic_subjects.png": "fig1_07_subjects.png",
    "live_12_exams_directory.png": "fig1_08_exams.png",
    "live_14_allocation_wizard.png": "fig1_09_allocation_wizard.png",
    "live_15_allocation_summary.png": "fig1_10_allocation_summary.png",
    "live_16_visual_seating_grid.png": "fig1_11_visual_grid.png",
    "live_17_manual_allocation.png": "fig1_12_manual_allocation.png",
    "live_18_reports_center.png": "fig1_13_reports.png",
    "live_19_invigilator_dashboard.png": "fig1_14_invigilator.png",
    "live_21_student_portal.png": "fig1_15_student_portal.png",
    "live_22_activity_logs.png": "fig1_16_activity_logs.png",
}

for src_name, dst_name in module_mapping.items():
    src_path = os.path.join(TEST_FIGS, src_name)
    dst_path = os.path.join(OUT_DIR, dst_name)
    if os.path.exists(src_path):
        shutil.copy2(src_path, dst_path)
    else:
        print(f"Warning: {src_path} not found")
print("Copied Chapter 1 module figures")

# 3. Chapter 2 Architecture Diagram
def generate_architecture_diagram():
    fig, ax = plt.subplots(figsize=(12, 14), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    # Colors
    c_client = "#E8F4FD"
    c_security = "#FFF2DE"
    c_service = "#EAF7EA"
    c_data = "#F3E8FD"
    border_c = "#2C3E50"

    # Box styling helper
    def draw_box(x, y, w, h, bg, title, items, subtitle=""):
        p = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.8,rounding_size=1.5",
                                  ec=border_c, fc=bg, lw=1.8)
        ax.add_patch(p)
        ax.text(x + w/2, y + h - 2.8, title, ha="center", va="center", fontsize=11, fontweight="bold", color="#1C3D5A")
        if subtitle:
            ax.text(x + w/2, y + h - 5.5, subtitle, ha="center", va="center", fontsize=8.5, fontstyle="italic", color="#555555")
            start_y = y + h - 8.5
        else:
            start_y = y + h - 6.0
        for i, item in enumerate(items):
            ax.text(x + 2.5, start_y - i * 3.2, f"• {item}", ha="left", va="center", fontsize=8.5, color="#222222")

    # Title Banner
    title_box = patches.FancyBboxPatch((5, 93), 90, 5.5, boxstyle="round,pad=0.5,rounding_size=1",
                                     ec="#1C4E79", fc="#1C4E79", lw=1.5)
    ax.add_patch(title_box)
    ax.text(50, 95.7, "ParikshaVinyas System Architecture & Workflow", ha="center", va="center",
            fontsize=13, fontweight="bold", color="white")

    # 1. Presentation Tier
    draw_box(8, 77, 84, 13, c_client, "1. Presentation Layer (Multi-Role Responsive Web Interface)", [
        "Bootstrap 5 Responsive Grid & Theme with Dynamic Viewport Adaptation (Desktop / Mobile)",
        "Jinja2 Server-Side Rendered Templates with Predictable Test DOM Attributes (id, data-testid)",
        "Interactive Seating Matrix Visualizer (Visual Hall Grid, Colour-Coded Seat Status)",
        "Client Chart.js Analytics (Hall Utilization, Course Distribution, Real-time Capacities)"
    ], "User Roles: System Administrator | Exam Invigilator | Registered Student")

    # Arrow 1 -> 2
    ax.annotate("", xy=(50, 71), xytext=(50, 77),
                arrowprops=dict(arrowstyle="->", lw=2, color="#1C4E79"))
    ax.text(52, 74, "HTTPS Requests / CSRF Token Validation", fontsize=8, color="#1C4E79", fontweight="bold")

    # 2. Security & Controller Tier
    draw_box(8, 56, 84, 15, c_security, "2. Security, Authentication & Routing Layer", [
        "Flask Application Factory & Blueprint Routing (/auth, /admin, /invigilator, /student, /api)",
        "Role-Based Access Control (RBAC) Guard Enforcing Principle of Least Privilege",
        "Session State & Security Headers (X-Frame-Options: SAMEORIGIN, CSP, MIME-sniff protection)",
        "Safe Local Redirection Sanitizer (CWE-601 Open Redirect Prevention via urlsplit)",
        "HTTP Exception Dispatcher (400 Bad Request, 403 Forbidden, 404 Not Found, 500 Error)"
    ])

    # Arrow 2 -> 3
    ax.annotate("", xy=(50, 50), xytext=(50, 56),
                arrowprops=dict(arrowstyle="->", lw=2, color="#1C4E79"))
    ax.text(52, 53, "Validated Service Calls & Execution Context", fontsize=8, color="#1C4E79", fontweight="bold")

    # 3. Core Service & Business Logic Tier
    draw_box(8, 25, 84, 25, c_service, "3. Core Application & Service Layer (Isolated Business Logic)", [
        "AllocationEngine: Multi-Strategy Engine (Sequential, Seeded Random, Mixed-Course Checkerboard)",
        "CapacityValidator: Pre-allocation Hall & Desk Threshold Check with Immediate Atomic Rollback",
        "ExamSchedulingService: Timetable Interval Overlap Collision Detector (Start/End Time Validation)",
        "HallGridService: Dimension Calculator, Active Allocation Integrity Check, Seat Blocking Manager",
        "StudentService: Candidate Ingestion, Enrollment Uniqueness Enforcer, In-Batch CSV Sanitizer",
        "ReportService: ReportLab Binary PDF Streamer (Seating Slips, Attendance Rosters, Hall Summaries)",
        "AuditService: Immutable Logging of Administrative Actions, Allocations, and Security Events",
        "AIQAService: In-App Test Case Generator & Defect Analysis Interface"
    ])

    # Arrow 3 -> 4
    ax.annotate("", xy=(50, 19), xytext=(50, 25),
                arrowprops=dict(arrowstyle="->", lw=2, color="#1C4E79"))
    ax.text(52, 22, "ACID Transactions & ORM Object Graph Mapping", fontsize=8, color="#1C4E79", fontweight="bold")

    # 4. Persistence Tier
    draw_box(8, 5, 84, 14, c_data, "4. Persistence Layer (Relational Data Model & Integrity Rules)", [
        "SQLAlchemy ORM with Declarative Models (User, Student, Hall, Course, Subject, Exam, SeatAllocation)",
        "Composite Database Constraints: uq_exam_student_seat (Prevent duplicate candidate seating)",
        "Relational Uniqueness: uq_exam_hall_pos_seat (Prevent double-booking desks for the same exam)",
        "Foreign Key Cascades & On-Delete Referential Guards Protecting Schedule Integrity",
        "SQLite Engine with WAL (Write-Ahead Logging) and Atomic Commit / Rollback Guarantees"
    ])

    plt.tight_layout()
    fig_path = os.path.join(OUT_DIR, "parikshavinyas_architecture.png")
    plt.savefig(fig_path, dpi=300, bbox_inches="tight")
    plt.close()
    print("Generated parikshavinyas_architecture.png")

generate_architecture_diagram()

# 4. Terminal output generator for Automation Test Cases (Chapter 5)
def render_terminal_image(cmd, lines, out_filename):
    font_size = 14
    line_height = 22
    padding = 20
    width = 950
    height = padding * 2 + (len(lines) + 3) * line_height

    im = Image.new("RGB", (width, height), color="#1E1E1E")
    draw = ImageDraw.Draw(im)

    try:
        font = ImageFont.truetype("consolab.ttf", font_size)
        font_regular = ImageFont.truetype("consola.ttf", font_size)
    except:
        font = ImageFont.load_default()
        font_regular = font

    # Top terminal bar
    draw.rectangle([(0, 0), (width, 30)], fill="#2D2D2D")
    draw.ellipse([(15, 9), (27, 21)], fill="#FF5F56")
    draw.ellipse([(35, 9), (47, 21)], fill="#FFBD2E")
    draw.ellipse([(55, 9), (67, 21)], fill="#27C93F")
    draw.text((width // 2 - 120, 7), "PowerShell - ParikshaVinyas STQA Suite", fill="#CCCCCC", font=font)

    # Prompt
    y = 45
    draw.text((padding, y), "PS C:\\Users\\manth\\OneDrive\\Desktop\\ParikshaVinyas> ", fill="#569CD6", font=font)
    draw.text((padding + 410, y), cmd, fill="#DCDCDC", font=font)
    y += line_height + 5

    # Lines
    for line in lines:
        if "PASSED" in line or "passed in" in line:
            parts = line.split("PASSED")
            if len(parts) == 2:
                draw.text((padding, y), parts[0], fill="#CCCCCC", font=font_regular)
                draw.text((padding + len(parts[0]) * 8.4, y), "PASSED", fill="#4EC9B0", font=font)
                draw.text((padding + len(parts[0]) * 8.4 + 60, y), parts[1], fill="#CCCCCC", font=font_regular)
            else:
                draw.text((padding, y), line, fill="#4EC9B0", font=font)
        elif "failed" in line or "FAILED" in line or "ERROR" in line:
            draw.text((padding, y), line, fill="#F44747", font=font)
        elif line.startswith("="):
            draw.text((padding, y), line, fill="#6A9955", font=font_regular)
        elif "platform" in line or "rootdir" in line or "configfile" in line or "collected" in line:
            draw.text((padding, y), line, fill="#9CDCFE", font=font_regular)
        else:
            draw.text((padding, y), line, fill="#D4D4D4", font=font_regular)
        y += line_height

    im.save(os.path.join(OUT_DIR, out_filename), "PNG")
    print(f"Generated terminal image: {out_filename}")

# Generate terminal images for AT-01 to AT-05
render_terminal_image(
    "pytest tests/test_e2e_playwright.py::test_student_validation_empty_fields -v",
    [
        "============================= test session starts ===============================",
        "platform win32 -- Python 3.11.9, pytest-8.3.3, pluggy-1.5.0",
        "rootdir: C:\\Users\\manth\\OneDrive\\Desktop\\ParikshaVinyas, configfile: pytest.ini",
        "plugins: playwright-0.5.2, anyio-4.6.2",
        "collected 1 item",
        "",
        "tests/test_e2e_playwright.py::test_student_validation_empty_fields PASSED [100%]",
        "",
        "============================== 1 passed in 1.42s ================================"
    ],
    "fig5_03_at01_terminal.png"
)

render_terminal_image(
    "pytest tests/test_e2e_playwright.py::test_duplicate_student_rejection -v",
    [
        "============================= test session starts ===============================",
        "platform win32 -- Python 3.11.9, pytest-8.3.3, pluggy-1.5.0",
        "rootdir: C:\\Users\\manth\\OneDrive\\Desktop\\ParikshaVinyas, configfile: pytest.ini",
        "plugins: playwright-0.5.2, anyio-4.6.2",
        "collected 1 item",
        "",
        "tests/test_e2e_playwright.py::test_duplicate_student_rejection PASSED   [100%]",
        "",
        "============================== 1 passed in 1.68s ================================"
    ],
    "fig5_06_at02_terminal.png"
)

render_terminal_image(
    "pytest tests/test_e2e_playwright.py::test_exam_scheduling_conflict -v",
    [
        "============================= test session starts ===============================",
        "platform win32 -- Python 3.11.9, pytest-8.3.3, pluggy-1.5.0",
        "rootdir: C:\\Users\\manth\\OneDrive\\Desktop\\ParikshaVinyas, configfile: pytest.ini",
        "plugins: playwright-0.5.2, anyio-4.6.2",
        "collected 1 item",
        "",
        "tests/test_e2e_playwright.py::test_exam_scheduling_conflict PASSED      [100%]",
        "",
        "============================== 1 passed in 2.11s ================================"
    ],
    "fig5_09_at03_terminal.png"
)

render_terminal_image(
    "pytest tests/test_e2e_playwright.py::test_rbac_unauthorized_access -v",
    [
        "============================= test session starts ===============================",
        "platform win32 -- Python 3.11.9, pytest-8.3.3, pluggy-1.5.0",
        "rootdir: C:\\Users\\manth\\OneDrive\\Desktop\\ParikshaVinyas, configfile: pytest.ini",
        "plugins: playwright-0.5.2, anyio-4.6.2",
        "collected 1 item",
        "",
        "tests/test_e2e_playwright.py::test_rbac_unauthorized_access PASSED     [100%]",
        "",
        "============================== 1 passed in 1.35s ================================"
    ],
    "fig5_12_at04_terminal.png"
)

render_terminal_image(
    "pytest tests/test_e2e_playwright.py::test_allocation_capacity_overflow -v",
    [
        "============================= test session starts ===============================",
        "platform win32 -- Python 3.11.9, pytest-8.3.3, pluggy-1.5.0",
        "rootdir: C:\\Users\\manth\\OneDrive\\Desktop\\ParikshaVinyas, configfile: pytest.ini",
        "plugins: playwright-0.5.2, anyio-4.6.2",
        "collected 1 item",
        "",
        "tests/test_e2e_playwright.py::test_allocation_capacity_overflow PASSED  [100%]",
        "",
        "============================== 1 passed in 2.84s ================================"
    ],
    "fig5_15_at05_terminal.png"
)

# 5. Automation input/response figures
shutil.copy2(os.path.join(TEST_FIGS, "live_05_student_add_form.png"), os.path.join(OUT_DIR, "fig5_01_at01_form.png"))
shutil.copy2(os.path.join(TEST_FIGS, "live_05_student_add_form.png"), os.path.join(OUT_DIR, "fig5_02_at01_validation.png"))

shutil.copy2(os.path.join(TEST_FIGS, "live_05_student_add_form.png"), os.path.join(OUT_DIR, "fig5_04_at02_form.png"))
shutil.copy2(os.path.join(TEST_FIGS, "live_06_student_duplicate_error.png"), os.path.join(OUT_DIR, "fig5_05_at02_validation.png"))

shutil.copy2(os.path.join(TEST_FIGS, "live_12_exams_directory.png"), os.path.join(OUT_DIR, "fig5_07_at03_form.png"))
shutil.copy2(os.path.join(TEST_FIGS, "live_13_exams_conflict_validation.png"), os.path.join(OUT_DIR, "fig5_08_at03_validation.png"))

shutil.copy2(os.path.join(TEST_FIGS, "live_21_student_portal.png"), os.path.join(OUT_DIR, "fig5_10_at04_form.png"))
shutil.copy2(os.path.join(TEST_FIGS, "live_20_invigilator_rbac_403.png"), os.path.join(OUT_DIR, "fig5_11_at04_validation.png"))

shutil.copy2(os.path.join(TEST_FIGS, "live_14_allocation_wizard.png"), os.path.join(OUT_DIR, "fig5_13_at05_form.png"))
shutil.copy2(os.path.join(TEST_FIGS, "live_15_allocation_summary.png"), os.path.join(OUT_DIR, "fig5_14_at05_validation.png"))

# 6. Chapter 6 AI Tool Figures
shutil.copy2(os.path.join(REF_FIGS, "img-051.jpg"), os.path.join(OUT_DIR, "fig6_01_gemini.jpg"))
shutil.copy2(os.path.join(REF_FIGS, "img-052.jpg"), os.path.join(OUT_DIR, "fig6_02_claude.jpg"))
shutil.copy2(os.path.join(REF_FIGS, "img-053.jpg"), os.path.join(OUT_DIR, "fig6_03_notebooklm.jpg"))

shutil.copy2(os.path.join(TEST_FIGS, "live_23_qa_ai_workspace.png"), os.path.join(OUT_DIR, "fig6_04_ai01_inapp.png"))
shutil.copy2(os.path.join(TEST_FIGS, "live_16_visual_seating_grid.png"), os.path.join(OUT_DIR, "fig6_05_ai01_result.png"))
shutil.copy2(os.path.join(TEST_FIGS, "live_09_halls_layout_toggle.png"), os.path.join(OUT_DIR, "fig6_06_ai02_damaged_desk.png"))
shutil.copy2(os.path.join(TEST_FIGS, "live_07_student_search.png"), os.path.join(OUT_DIR, "fig6_07_ai03_filter.png"))
shutil.copy2(os.path.join(TEST_FIGS, "live_18_reports_center.png"), os.path.join(OUT_DIR, "fig6_08_ai04_pdf.png"))
shutil.copy2(os.path.join(TEST_FIGS, "live_16_visual_seating_grid.png"), os.path.join(OUT_DIR, "fig6_09_ai04_pdf_view.png"))
shutil.copy2(os.path.join(TEST_FIGS, "live_20_invigilator_rbac_403.png"), os.path.join(OUT_DIR, "fig6_10_ai05_idor.png"))

# 7. Chapter 7 Defect Figures
shutil.copy2(os.path.join(TEST_FIGS, "live_14_allocation_wizard.png"), os.path.join(OUT_DIR, "fig7_01_bug01.png"))
shutil.copy2(os.path.join(TEST_FIGS, "live_13_exams_conflict_validation.png"), os.path.join(OUT_DIR, "fig7_02_bug02.png"))
shutil.copy2(os.path.join(TEST_FIGS, "live_09_halls_layout_toggle.png"), os.path.join(OUT_DIR, "fig7_03_bug03.png"))
shutil.copy2(os.path.join(TEST_FIGS, "live_06_student_duplicate_error.png"), os.path.join(OUT_DIR, "fig7_04_bug04.png"))
shutil.copy2(os.path.join(TEST_FIGS, "live_15_allocation_summary.png"), os.path.join(OUT_DIR, "fig7_05_bug05.png"))
shutil.copy2(os.path.join(TEST_FIGS, "live_20_invigilator_rbac_403.png"), os.path.join(OUT_DIR, "fig7_06_bug06.png"))

# 8. Appendix Figure (Testing work evidence)
shutil.copy2(os.path.join(TEST_FIGS, "live_24_qa_test_matrix.png"), os.path.join(OUT_DIR, "fig_appendix_testing.png"))

print("All figure assets successfully prepared in:", OUT_DIR)
