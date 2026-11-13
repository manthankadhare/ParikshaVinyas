# ParikshaVinyas (परीक्षाविन्यास)
### Smart Examination Hall & Seat Allocation Management System
**Institution:** UPL University of Sustainable Technology  
> *Plan Smart. Allocate Fairly. Examine Seamlessly.*

---

## 1. Project Overview & Academic STQA Scope

**ParikshaVinyas** is an enterprise-grade academic examination management platform engineered to automate examination scheduling, hall inventory management, capacity planning, and intelligent seat allocation. 

Developed specifically for a **Software Testing and Quality Assurance (STQA)** academic mini project, the platform demonstrates strict adherence to:
- Testability and robust modular architecture.
- Boundary Value Analysis (BVA) for hall capacities and academic thresholds.
- Equivalence Partitioning (EP) for valid/invalid input domains.
- Deterministic and combinatorial allocation algorithms (Sequential, Random with reproducible seeds, Mixed Course/Branch interleaving).
- Atomic database transactions with strict rollback to prevent partial allocation states.
- Automated end-to-end verification via **Pytest** and **Playwright**.
- An integrated **STQA Quality Engineering Workspace** featuring AI-assisted test case synthesis and defect lifecycle management.

---

## 2. Technology Stack

- **Backend Framework:** Python 3.13, Flask 3.0.3
- **ORM & Database:** SQLAlchemy 2.0 / Flask-SQLAlchemy, SQLite
- **Security & RBAC:** Flask-Login, Flask-WTF, CSRF Protection, Werkzeug Security (Scrypt/PBKDF2)
- **Document & PDF Reporting:** ReportLab 4.2.5
- **Frontend Architecture:** HTML5, CSS3, Bootstrap 5.3, JavaScript (ES6+), Jinja2
- **Data Visualization & Icons:** Chart.js, Lucide Icons
- **Automated Testing:** Pytest 8.3, Playwright 1.48 (Python Chromium)

---

## 3. Key Functional Modules

```
                    ┌─────────────────────────┐
                    │      Administrator      │
                    └────────────┬────────────┘
                                 │
     ┌───────────────────────────┼───────────────────────────┐
     ▼                           ▼                           ▼
┌──────────────┐        ┌─────────────────┐        ┌─────────────────┐
│ Student Mgmt │        │   Hall & Grid   │        │ Exam Scheduling │
│  CRUD & CSV  │        │ Capacity & Desk │        │ Timetable & Slot│
└──────┬───────┘        └────────┬────────┘        └────────┬────────┘
       │                         │                          │
       └─────────────────────────┼──────────────────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │  Seat Allocation Engine │
                    │ • Sequential (Roll No)  │
                    │ • Mixed Course (Checker)│
                    │ • Randomized (With Seed)│
                    └────────────┬────────────┘
                                 │
     ┌───────────────────────────┼───────────────────────────┐
     ▼                           ▼                           ▼
┌──────────────┐        ┌─────────────────┐        ┌─────────────────┐
│ Visual Grid  │        │ Reports & PDFs  │        │   Student Pass  │
│ Color Desks  │        │ Hall Charts/CSV │        │ Personal Slip   │
└──────────────┘        └─────────────────┘        └─────────────────┘
```

1. **Executive Operations Dashboard:** Real-time statistics on hall utilization, candidate distribution, scheduled exams, and interactive Chart.js visualizations.
2. **Student Candidate Directory:** Search, multi-criteria filtering, student profile dossiers, and CSV ingestion with row-level error reporting.
3. **Examination Hall & Visual Grid Engine:** Dynamic row x column dimensions, gross capacity calculation, damaged desk blocking, and net usable capacity tracking.
4. **Curriculum & Examination Scheduling:** Date/time overlap detection, duration validation, and automatic eligibility linking.
5. **Intelligent Seat Allocation Engine:**
   - *Sequential Strategy:* Ordered by enrollment number across available desks.
   - *Mixed Course / Division Strategy:* Checkerboard interleaving of distinct courses/divisions to minimize student collaboration.
   - *Randomized Strategy:* Deterministic shuffle utilizing reproducible random seeds for repeatable STQA test execution.
   - *Atomic Transactions:* Automatic rollback on insufficient capacity; zero orphaned records.
6. **Manual Allocation & Bidirectional Seat Swapping:** Real-time seat reassignment, automated bidirectional seat exchange, and timestamped audit logs.
7. **Official ReportLab PDF Reports:** Official university examination charts, hall door-posting attendance sheets with signature blocks, and candidate admit slips.
8. **Role-Based Portals:**
   - **Administrator:** Full operational and configuration authority.
   - **Invigilator:** View assigned halls, candidate rosters, and attendance sheets.
   - **Student:** View personal timetable, allocated hall, assigned seat code, and download admit passes.
9. **STQA Testing Hub & AI Workspace:**
   - 30 preloaded manual test case specifications (15 Positive, 15 Negative/Edge cases).
   - Defect tracking lifecycle (Severity, Priority, Steps to Reproduce, Status).
   - AI Test Case Synthesizer with 1-click import into persistent test repository.

---

## 4. Default Demonstration Credentials

The database comes pre-seeded with realistic institutional accounts:

| Role | Username / Identifier | Password | Access Rights |
|---|---|---|---|
| **Administrator** | `admin` | `Admin@2026` | Full system administration |
| **Invigilator** | `invig_sharma` | `Invig@2026` | Hall duty roster & attendance sheets |
| **Invigilator** | `invig_patil` | `Invig@2026` | Hall duty roster & attendance sheets |
| **Student** | `EN2026101` | `Student@6101` | Personal examination schedule & admit pass |
| **Student** | `EN2026102` | `Student@6102` | Personal examination schedule & admit pass |

*(Student password convention: `Student@<Last4DigitsOfEnrollment>`)*

---

## 5. Local Setup and Execution Instructions (Windows PowerShell)

### Step 1: Create and Activate Virtual Environment
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### Step 2: Install Required Dependencies
```powershell
pip install -r requirements.txt
playwright install chromium
```

### Step 3: Initialize Database and Populate Demonstration Dataset
```powershell
python scripts\seed_database.py
```
*(To reset the database at any time, execute `python scripts\reset_database.py`)*

### Step 4: Run the Application Server
```powershell
python run.py
```
Open your browser and navigate to: **`http://127.0.0.1:5000`**

---

## 6. Automated Testing Instructions

### Executing Pytest Unit, Integration & Defect Regression Suite
```powershell
pytest tests\unit tests\integration -v
```
Executes 26 automated tests covering:
- Password hashing & model properties.
- Gross & usable capacity math.
- Sequential, Random (reproducible seed), and Mixed Course allocation algorithms.
- Capacity shortage rollback (BVA: capacity vs capacity + 1).
- Manual seat swap integrity.
- Authentication & RBAC access boundaries.
- ReportLab binary PDF generation.
- 12 dedicated regression tests verifying resolution of all real-world defects.

### Executing Playwright E2E Browser Automation Suite
```powershell
pytest tests\automation\test_e2e_scenarios.py -v
```
Automates 20 complete browser scenarios across administrative, student, and invigilator flows, with screenshots saved automatically to `test_reports/screenshots/`.

---

## 7. STQA Test Case Execution Summary

Refer to [`docs/manual_test_cases.md`](docs/manual_test_cases.md) and [`docs/manual_test_cases.csv`](docs/manual_test_cases.csv) for the full 42-case matrix.

| Technique | Total Cases | Pass | Fail |
|---|:---:|:---:|:---:|
| Boundary Value Analysis (BVA) | 6 | 6 | 0 |
| Equivalence Partitioning (EP) | 8 | 8 | 0 |
| Decision Table Testing | 3 | 3 | 0 |
| State Transition Testing | 4 | 4 | 0 |
| Security & Role-Based Access (RBAC) | 4 | 4 | 0 |
| Data Integrity & Unique Constraints | 5 | 5 | 0 |
| Defect Regression Test Cases | 12 | 12 | 0 |
| **Total** | **42** | **42** | **0** |

---

## 8. Verified Defect Reports

Documented in `app/models/qa.py` and accessible in the **STQA Defect Tracking** section (`/admin/qa/defects`):
- **`BUG_ALLOC_001` (Critical / P1):** Atomic rollback failure during boundary capacity overflow. Resolved via pre-allocation seat count validation.
- **`BUG_SCHED_002` (High / P2):** Timetable collision for identical semester examinations. Resolved via temporal interval overlap SQL queries.
- **`BUG_GRID_003` (Medium / P2):** Desk blocking allowed on occupied seat. Resolved by checking active candidate allocations prior to state transition.
- **`BUG_SCHED_004` (High / P1):** Exam Edit Timetable Collision Bypass in `exam.py:edit`. Resolved via schedule collision exclusion query.
- **`BUG_DATA_005` (High / P2):** CSV Batch Import crash on in-batch duplicate rows. Resolved via tracking sets (`seen_enrollments`, `seen_emails`) and per-row error logging.
- **`BUG_HALL_006` (High / P2):** Hall Resize Truncation of Active Seat Allocations. Resolved via active allocation boundary validation.
- **`BUG_ACAD_007` (Medium / P2):** Course Deletion Foreign Key Integrity Crash with scheduled exams. Resolved via referential dependency checks.
- **`BUG_ALLOC_008` (Critical / P1):** Data loss in force re-allocation on insufficient capacity. Resolved by validating capacity before deleting prior allocations.
- **`BUG_ALLOC_009` (High / P2):** Manual allocation WTForms choice rejection on POST. Resolved by prioritizing `request.form.get('examination_id')`.
- **`BUG_SEC_010` (High / P1):** IDOR authorization bypass in invigilator hall roster. Resolved by verifying `InvigilatorAssignment` ownership.
- **`BUG_SEC_011` (Medium / P2):** CWE-601 open redirect in user login. Resolved via `urllib.parse.urlsplit` validation.
- **`BUG_DASH_012` (Low / P3):** Dashboard usable capacity calculation skewed by inactive halls. Resolved by summing active halls strictly.
- **`BUG_SEC_013` (Medium / P3):** Missing defensive HTTP security headers. Resolved via `@app.after_request` security header injection.
- **`BUG_STUD_014` (Medium / P2):** Student edit profile duplicate email collision crash. Resolved via pre-commit email uniqueness check.
- **`BUG_HALL_015` (Low / P3):** Hall layout seat blocking rejected on cancelled/completed exams. Resolved via active examination status filtering.

---

## 9. License & Academic Attribution
Developed for the **Software Testing and Quality Assurance (STQA) Mini Project**, Department of Computer Engineering.
All Rights Reserved &copy; 2026 ParikshaVinyas.

