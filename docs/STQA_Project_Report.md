# Software Testing and Quality Assurance (STQA) Academic Mini Project Report

**Project Title:** ParikshaVinyas (परीक्षाविन्यास) — Smart Examination Hall & Seat Allocation Management System  
**Institution:** UPL University of Sustainable Technology  
**Academic Session:** 2025–2026  
**Discipline:** Computer Engineering  
**Subject:** Software Testing & Quality Assurance (STQA)

---

## 1. Abstract & Introduction

Examination management in collegiate and university environments is fraught with operational challenges: desk capacity miscalculations, student proximity and unfair practices, conflicting schedules, and manual seat allotment errors. 

**ParikshaVinyas** addresses these challenges by automating examination hall planning, candidate seat allocation, and reporting. Developed as an STQA mini-project, the software has been engineered with testability, input validation, exception handling, data integrity constraints, and automated verification as primary design goals.

---

## 2. System Architecture & Design for Testability

The application implements a decoupled, modular Flask architecture:
- **Presentation Layer:** Jinja2 templates styled with Bootstrap 5, Chart.js, and Lucide icons, offering predictable DOM element IDs and data attributes for resilient E2E browser automation.
- **Application & Service Layer:** Strict separation of business rules into isolated service modules (`AllocationEngine`, `ReportService`, `AIQAService`, `AuditService`), allowing granular unit testing without HTTP overhead.
- **Persistence Layer:** SQLAlchemy ORM models backed by SQLite with database-level uniqueness constraints:
  - `uq_exam_student_seat` prevents assigning multiple seats to one candidate.
  - `uq_exam_hall_pos_seat` prevents double-booking a single desk for the same examination.
  - Atomic transactions (`db.session.rollback()`) guarantee that any allocation failure leaves no orphaned or partial records.

---

## 3. STQA Testing Techniques & Applied Test Design

### 3.1 Boundary Value Analysis (BVA)
BVA was applied to critical numeric boundaries across the system:
1. **Hall Capacity Limits:** Tested behavior when eligible candidates equal capacity ($N = \text{Capacity}$), when candidates exceed capacity by one ($N = \text{Capacity} + 1$), and when candidates fall below capacity ($N = \text{Capacity} - 1$).
2. **Academic Semesters:** Enforced boundary validation for semester values strictly between $1$ (Min) and $8$ (Max). Inputs of $0$ (Min - 1) and $9$ (Max + 1) are rejected with clear validation alerts.
3. **Hall Dimensions:** Enforced constraints preventing non-positive rows or columns ($R \le 0$ or $C \le 0$).

### 3.2 Equivalence Partitioning (EP)
Input domains were divided into valid and invalid equivalence classes:
- **Student Enrollment:** Valid alphanumeric strings vs. duplicate enrollments vs. empty strings.
- **Email Addresses:** Syntactically valid email formats vs. unformatted strings lacking domain parts.
- **Examination Timings:** Valid temporal intervals where $\text{Start Time} < \text{End Time}$ vs. invalid intervals where $\text{End Time} \le \text{Start Time}$.

### 3.3 Decision Table Testing
Complex business rules were modeled via decision tables:
- **Schedule Conflict Detection:** If `Course`, `Semester`, and `Date` match an existing exam, and `Start Time < Existing End Time` and `End Time > Existing Start Time`, the schedule is rejected as a temporal conflict.

### 3.4 State Transition Testing
- **Hall Desk States:** Evaluated desk transitions between `Available` $\to$ `Blocked` $\to$ `Available`. Verified that a desk in the `Allocated` state cannot transition to `Blocked` without first reallocating or clearing the student.

---

## 4. Test Execution Metrics & Automation Summary

### 4.1 Pytest Suite (Unit, Integration & Defect Regressions)
- **Framework:** Pytest 8.3 with Flask Test Client.
- **Scope:** Models, business algorithms, authentication, RBAC boundaries, ReportLab PDF streaming, and 12 dedicated regression tests for identified bugs.
- **Execution Result:** **26 / 26 Passed (100% Pass Rate)** in 22.23 seconds.

### 4.2 Playwright End-to-End Browser Automation Suite
- **Framework:** Playwright 1.48 (Python Chromium).
- **Scope:** 20 complete user scenarios covering Admin, Invigilator, and Student workflows.
- **Execution Result:** **20 / 20 Passed (100% Pass Rate)** in 71.06 seconds.
- **Artifacts:** 20 high-resolution verification screenshots captured automatically in `test_reports/screenshots/`.

---

## 5. Defect Lifecycle & Root Cause Analysis

Fifteen comprehensive functional, security, integrity, and operational defects identified during testing and senior QA inspection were reproduced with verified test scripts, systematically resolved, and validated through regression tests:

| Defect ID | Severity | Module | Root Cause | Resolution | Verification Status |
|---|---|---|---|---|:---:|
| `BUG_ALLOC_001` | Critical | Allocation | Atomic rollback failed during capacity overflow; partial records persisted. | Pre-validated usable capacity before entering allocation loop and wrapped in explicit try-catch rollback. | **Resolved & Verified** |
| `BUG_SCHED_002` | High | Scheduling | Timetable interval overlap was not detected for exams sharing a semester. | Added temporal interval comparison query in `exam.py`. | **Resolved & Verified** |
| `BUG_GRID_003` | Medium | Hall Layout | In-place desk blocking allowed on occupied desks. | Added foreign key allocation lookup before toggling blocked status. | **Resolved & Verified** |
| `BUG_SCHED_004` | High | Exam Management | Exam edit route omitted timetable collision check for identical course/sem. | Added exclusion filter query comparing against other active exams on same date/time. | **Resolved & Verified** |
| `BUG_DATA_005` | High | Student Management | In-batch duplicate CSV records triggered unhandled SQLite IntegrityError at commit. | Implemented in-batch tracking set (`seen_enrollments`, `seen_emails`) and per-row error logging. | **Resolved & Verified** |
| `BUG_HALL_006` | High | Hall Management | Hall resize allowed shrinking dimensions below active seat allocation coordinates. | Added boundary validation query against `hall.allocations` before updating row/col dimensions. | **Resolved & Verified** |
| `BUG_ACAD_007` | Medium | Academic | Deleting course with 0 students but linked examinations raised 500 ForeignKey error. | Added cascade referential checks preventing deletion if exams or subjects have active exams. | **Resolved & Verified** |
| `BUG_ALLOC_008` | Critical | Allocation Engine | Force re-allocate cleared existing seats before checking capacity, wiping prior allocations. | Deferred clearing old allocations until after usable capacity validation passes completely. | **Resolved & Verified** |
| `BUG_ALLOC_009` | High | Allocation Route | Manual seat assignment choices defaulted to Exam 1 on POST without query string. | Prioritized `request.form.get('examination_id')` to dynamically populate valid candidate choices. | **Resolved & Verified** |
| `BUG_SEC_010` | High | Invigilator Portal | Invigilator hall roster and PDF export lacked assignment authorization (IDOR). | Enforced ownership check: verified invigilator is assigned to `(hall_id, exam_id)` or returns 403. | **Resolved & Verified** |
| `BUG_SEC_011` | Medium | Authentication | Unsanitized `next` URL parameter allowed open external redirects (CWE-601). | Parsed `next` target with `urllib.parse.urlsplit` to restrict redirects strictly to relative local paths. | **Resolved & Verified** |
| `BUG_DASH_012` | Low | Admin Dashboard | Dashboard subtracted inactive hall blocked seats from active gross capacity. | Computed usable capacity strictly as the sum of `usable_capacity` across active halls. | **Resolved & Verified** |
| `BUG_SEC_013` | Medium | Security Headers | Missing defensive HTTP response headers exposing UI to clickjacking/MIME sniffing. | Configured `@app.after_request` adding `X-Frame-Options`, `X-Content-Type-Options`, `Referrer-Policy`. | **Resolved & Verified** |
| `BUG_STUD_014` | Medium | Student Management | Editing student profile allowed duplicate email collision crashing with IntegrityError. | Added duplicate email check against existing student records prior to database commit. | **Resolved & Verified** |
| `BUG_HALL_015` | Low | Hall Layout | Layout seat blocking falsely rejected toggling desks linked to cancelled/completed exams. | Filtered active allocations to only consider exams in `Scheduled`, `Allocated`, or `In Progress` state. | **Resolved & Verified** |

---

## 6. Viva Voce Q&A Preparation Guide

### Q1: What makes ParikshaVinyas testable from an STQA perspective?
> **Answer:** The application features decoupled service layers that isolate allocation and report generation logic from HTTP routing. In addition, the DOM elements feature deterministic IDs and test attributes, all database writes use atomic transactions with rollback support, and the randomized allocation algorithm accepts deterministic seeds for reproducible automated testing.

### Q2: How does the system handle Boundary Value Analysis during seat allocation?
> **Answer:** When an examination has $K$ eligible students and the selected halls offer exactly $K$ usable seats (on the boundary), the system allocates all students with 0 remaining seats. If the eligible count is $K+1$, the capacity validator triggers before database insertion, halts execution, rolls back cleanly, and reports the exact shortage of 1 seat without leaving partial records.

### Q3: What is the purpose of the "Mixed Course" allocation strategy?
> **Answer:** In academic examinations, seating adjacent students from the same course or division increases the risk of copying. The Mixed Course strategy groups students by course and division, and interleaves them across adjacent desk coordinates $(r, c)$ in a round-robin / checkerboard pattern to minimize peer proximity.

### Q4: Why did we select Playwright over legacy Selenium for E2E testing?
> **Answer:** Playwright provides native async network waiting, automatic element-readiness polling (eliminating flaky explicit sleeps), built-in headless Chromium bundling, direct viewport control, and built-in screenshot capturing.

