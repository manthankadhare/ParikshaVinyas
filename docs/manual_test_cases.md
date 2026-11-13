# ParikshaVinyas — Formal STQA Manual Test Case Specification & Execution Matrix

**Project:** ParikshaVinyas (परीक्षाविन्यास) — Smart Examination Hall & Seat Allocation Management System  
**Academic Module:** Software Testing & Quality Assurance (STQA)  
**Total Test Cases:** 42 (15 Positive Scenarios, 15 Negative / Edge Scenarios, 12 Defect Regression Scenarios)  
**Testing Methodologies Applied:** Equivalence Partitioning (EP), Boundary Value Analysis (BVA), Decision Table Testing, Error Guessing, State Transition Testing, Role-Based Access Control (RBAC), Transactional Integrity Checks, Security Vulnerability Remediation (OWASP/CWE).

---

## 1. Test Execution Summary

| Total Cases | Executed | Passed | Failed | Blocked | Pass Rate |
|:-----------:|:--------:|:------:|:------:|:-------:|:---------:|
| 42 | 42 | 42 | 0 | 0 | **100%** |

---

## 2. Test Cases Specification & Execution Record

| Test Case ID | Module | Scenario Description | STQA Technique | Input Data | Expected Result | Actual Result | Status |
|:---|:---|:---|:---|:---|:---|:---|:---:|
| `TC_AUTH_POS_01` | Auth & Security | Admin login with valid credentials | Equivalence Partitioning | `user=admin`, `pass=Admin@2026` | Authenticated session created; redirects to `/admin/dashboard` | Redirected to dashboard; welcome toast displayed | **Pass** |
| `TC_AUTH_POS_02` | Auth & Security | Student login via Enrollment No | Equivalence Partitioning | `user=EN2026101`, `pass=Student@6101` | Authenticated student portal session; personal timetable rendered | Successfully logged in; student schedule rendered | **Pass** |
| `TC_AUTH_POS_03` | Auth & Security | Invigilator login & duty schedule | Role-Based Access Control | `user=invig_sharma`, `pass=Invig@2026` | Redirects to `/invigilator/dashboard`; displays assigned halls | Successfully authenticated; displays 2 assigned duties | **Pass** |
| `TC_STUD_POS_04` | Student Management | Register student with valid fields | Equivalence Partitioning | Enrollment: `EN2026199`, Name: `Aarav Joshi`, Sem: 6 | Candidate created in Active state with auto-generated login | Student created and listed in directory with Active status | **Pass** |
| `TC_STUD_POS_05` | Student Management | Search candidates by enrollment substring | Functional Testing | Query: `101` | Filters directory to matching records | Matches `EN2026101` Aarav Sharma | **Pass** |
| `TC_STUD_POS_06` | Student Management | Filter candidates by Course & Semester | Decision Table Testing | Course: `CS`, Semester: `6` | Table displays only 6th Semester CS candidates | Exactly 30 CS Sem 6 candidates returned | **Pass** |
| `TC_HALL_POS_07` | Hall Management | Hall creation & capacity auto-calc | Functional Testing | Rows: `6`, Columns: `8`, Building: `Block C` | Gross capacity computed as `48` (`6*8`); usable capacity `48` | Created with 48 seats total capacity | **Pass** |
| `TC_HALL_POS_08` | Hall Management | Toggle blocked seat state in hall | State Transition Testing | Hall: `H-102`, Seat: `R01-C01`, Reason: `Broken desk` | Usable capacity decreases by 1; seat flagged red in grid | Usable capacity decreased to 29; seat blocked | **Pass** |
| `TC_EXAM_POS_09` | Exam Scheduling | Schedule exam with valid future date | Equivalence Partitioning | Date: `2026-12-20`, Time: `10:00 - 13:00` | Exam created in Scheduled state; active students enrolled | Exam scheduled; 30 eligible students linked | **Pass** |
| `TC_ALLOC_POS_10` | Allocation Engine | Sequential allocation with surplus capacity | Boundary Value Analysis | 30 students; 40 usable seats; Strategy: `Sequential` | All 30 students assigned seats; 0 unallocated; 10 remaining | All 30 allocated sequentially by enrollment no | **Pass** |
| `TC_ALLOC_POS_11` | Allocation Engine | Reproducible random allocation with seed | Random Seed Verification | Strategy: `Random`, Seed: `42` | Successive runs with seed 42 generate identical seat maps | Identical seat mapping produced on repeated test runs | **Pass** |
| `TC_ALLOC_POS_12` | Allocation Engine | Mixed Course / Division interleaving | Combinatorial Testing | Strategy: `Mixed Course`, 15 Div A + 15 Div B | Adjacent seats alternate between Div A and Div B | Checkerboard distribution achieved across rows | **Pass** |
| `TC_ALLOC_POS_13` | Allocation Engine | Manual seat assignment to empty desk | Functional Testing | Student: `EN2026101`, Target: `H-101-R02-C03` | Candidate assigned to target seat; audit entry logged | Assigned to H-101-R02-C03; audit history created | **Pass** |
| `TC_ALLOC_POS_14` | Allocation Engine | Bidirectional manual seat swap | State Transition Testing | Swap Student 1 (`R2C2`) and Student 2 (`R2C3`) | Both students exchange seats without unique key collision | Seats swapped cleanly without duplicate error | **Pass** |
| `TC_REP_POS_15` | Reports & PDF | Generate official ReportLab PDF chart | Output Verification | Exam: `EX-CS601`, Route: `/admin/reports/exam/<id>/pdf` | 200 OK binary PDF streamed with college branding | Valid PDF stream starting with `%PDF-1.4` received | **Pass** |
| `TC_AUTH_NEG_16` | Auth & Security | Reject login with incorrect password | Negative Testing | `user=admin`, `pass=WrongPass123` | Authentication fails; flash error displayed; no session | Rejected with error alert: Invalid credentials | **Pass** |
| `TC_AUTH_NEG_17` | Auth & Security | Block student access to admin endpoints | Security Role Testing | Role: `student`, Target: `/admin/dashboard` | HTTP 403 Forbidden received; access blocked | HTTP 403 Forbidden returned | **Pass** |
| `TC_STUD_NEG_18` | Student Management | Reject duplicate enrollment number | Unique Key Constraint | Re-insert existing enrollment `EN2026101` | Unique constraint error raised; duplicate rejected | Form displays error: Enrollment number already exists | **Pass** |
| `TC_STUD_NEG_19` | Student Management | Reject semester boundary below minimum (0) | Boundary Value Analysis | Semester: `0` | Form validation blocks submission (`min=1`) | Rejected: Semester must be between 1 and 8 | **Pass** |
| `TC_STUD_NEG_20` | Student Management | Reject semester boundary above maximum (9) | Boundary Value Analysis | Semester: `9` | Form validation blocks submission (`max=8`) | Rejected: Semester must be between 1 and 8 | **Pass** |
| `TC_STUD_NEG_21` | Student Management | Reject malformed email address | Error Guessing / Sanitization | Email: `not_a_valid_email` | Rejected by email validator | Form reports invalid email format | **Pass** |
| `TC_HALL_NEG_22` | Hall Management | Reject non-positive hall dimensions | Boundary Value Analysis | Rows: `0`, Columns: `-2` | Validation rejects submission; dimensions must be >= 1 | Form reports: Rows and cols must be >= 1 | **Pass** |
| `TC_HALL_NEG_23` | Hall Management | Prevent blocking an allocated seat | Data Integrity Check | Seat `H-101-R01-C01` occupied by candidate | Rejected with HTTP 409 conflict message | System blocks action: Seat occupied by student | **Pass** |
| `TC_EXAM_NEG_24` | Exam Scheduling | Reject end time earlier than start time | Temporal Validation | Start: `14:00`, End: `11:00` | Validation error: End time must be later than start | Blocked with: End time must be later than start | **Pass** |
| `TC_EXAM_NEG_25` | Exam Scheduling | Prevent overlapping exam schedules | Decision Table Testing | Same semester & date, overlapping time slot | Conflict detected; duplicate schedule prevented | Blocked with scheduling conflict alert | **Pass** |
| `TC_ALLOC_NEG_26` | Allocation Engine | Reject allocation when students > seats | Boundary Value Analysis | 41 students; 40 usable seats (Capacity + 1) | Atomic rollback; error summary displays shortage of 1 | Insufficient capacity error; 0 partial records | **Pass** |
| `TC_ALLOC_NEG_27` | Allocation Engine | Skip damaged/blocked seats in allocation | Constraint Verification | Seat `H-101-R01-C03` is Blocked | Algorithm skips `R01-C03`; assigns next available seat | Damaged seat left untouched; 0 students assigned | **Pass** |
| `TC_ALLOC_NEG_28` | Allocation Engine | Reject manual allocation of ineligible student | Business Rule Verification | Assign Mechanical student to CS exam | Rejected with: Student is not eligible for exam | Error raised: Candidate not in eligible list | **Pass** |
| `TC_ALLOC_NEG_29` | Allocation Engine | Prevent duplicate seat allocation | Database Unique Constraint | Assign student twice in same exam | Reassignment safely relocates student; no duplicates | Unique constraint uq_exam_student_seat enforced | **Pass** |
| `TC_SYS_NEG_30` | System Integrity | Prevent CSRF attack without valid token | Security Testing | POST form without CSRF token | Request rejected with HTTP 400 Bad Request | HTTP 400 Bad Request CSRF missing | **Pass** |
| `TC_REG_01` | Exam Scheduling | Detect timetable collision on exam modification | Regression / Decision Table | Edit Exam 2 to collide with Exam 1 slot | Collision flagged with warning; exam preserved | Rejected with Scheduling Conflict alert | **Pass** |
| `TC_REG_02` | Student Management | Handle in-batch duplicate CSV records | Regression / Batch Integrity | CSV containing duplicate rows within stream | Valid rows committed; duplicates flagged per line | 2 valid added; 2 duplicates logged in errors | **Pass** |
| `TC_REG_03` | Hall Management | Prevent hall resize truncating active seats | Regression / Boundary Integrity | Resize 5x6 hall with seat at R5C6 to 4x5 | Rejected: Active seat allocation outside bounds | Form reports active seat allocation collision | **Pass** |
| `TC_REG_04` | Academic Module | Prevent course deletion with linked exams | Regression / Referential Integrity | Delete course having scheduled examinations | Prevent deletion; notify examinations linked | Rejection notice: examinations are linked | **Pass** |
| `TC_REG_05` | Allocation Engine | Prevent allocation loss on capacity shortage | Regression / Transaction Safety | Force reallocate with undersized hall | Prior allocations preserved 100% intact | Shortage reported; 5/5 previous seats kept | **Pass** |
| `TC_REG_06` | Allocation Engine | Validate manual student choices on POST | Regression / Form State | POST manual seat assignment for Exam 2 | Student choice accepted and seat assigned | Student assigned; no WTForms invalid choice | **Pass** |
| `TC_REG_07` | Invigilator Portal | Prevent IDOR access to unassigned halls | Security / BOLA Prevention | Invigilator accesses unassigned hall ID | HTTP 403 Forbidden returned | HTTP 403 Forbidden verified | **Pass** |
| `TC_REG_08` | Authentication | Sanitize login next redirect (CWE-601) | Security / Open Redirect | Login with `?next=https://attacker.com` | Redirection constrained to internal dashboard | Redirects to `/admin/dashboard` safely | **Pass** |
| `TC_REG_09` | Admin Dashboard | Calculate usable seats accurately | Mathematical Integrity | Decommission hall with 10 blocked seats | Dashboard reflects active usable capacity only | Usable capacity exact sum of active halls | **Pass** |
| `TC_REG_10` | App Architecture | Enforce HTTP defense-in-depth headers | Security / Clickjacking | Inspect response headers on all routes | Headers present: SAMEORIGIN, nosniff, etc. | Security headers verified present | **Pass** |
| `TC_REG_11` | Student Management | Prevent email collision on student update | Data Integrity / Validation | Update student email to existing student email | Validation error; no unhandled 500 crash | Form displays: Email already used by another | **Pass** |
| `TC_REG_12` | Hall Management | Permit seat blocking for cancelled exams | State Filter / Functional | Block desk assigned to cancelled exam | Desk successfully blocked for maintenance | Action succeeds; seat blocked | **Pass** |
| `TC_ALLOC_NEG_30` | Allocation Engine | Prevent silent overwrite of existing allocation | Concurrency Guard | Re-run allocation without force flag | Rejection warning: Confirm regeneration to overwrite | Warning shown: Confirm regeneration to clear | **Pass** |

