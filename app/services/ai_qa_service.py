import os
import json
import re
import requests
from flask import current_app


class AIQAService:
    """
    AI-Assisted STQA Service for ParikshaVinyas.
    Provides intelligent test case generation, boundary value analysis,
    defect diagnosis, and bug report drafting.
    Includes smart heuristic rule engine fallback when no Gemini API key is configured.
    """

    @classmethod
    def generate_test_scenarios(cls, module_name, requirement_text, test_type='All'):
        """
        Generates structured test cases (Positive, Negative, Boundary Value, Edge Cases)
        for a given requirement.
        """
        api_key = os.environ.get('GEMINI_API_KEY') or current_app.config.get('GEMINI_API_KEY')
        if api_key:
            try:
                scenarios = cls._call_gemini_for_test_cases(api_key, module_name, requirement_text, test_type)
                if scenarios:
                    return scenarios
            except Exception as e:
                current_app.logger.warning(f"Gemini API call failed, using heuristic STQA engine: {e}")

        # Fallback heuristic generator
        return cls._heuristic_test_case_generator(module_name, requirement_text, test_type)

    @classmethod
    def analyze_defect(cls, bug_title, steps_to_reproduce, actual_result, expected_result):
        """
        Analyzes a defect, suggests root causes and recommends code/data fixes.
        """
        api_key = os.environ.get('GEMINI_API_KEY') or current_app.config.get('GEMINI_API_KEY')
        if api_key:
            try:
                analysis = cls._call_gemini_for_defect_analysis(api_key, bug_title, steps_to_reproduce, actual_result, expected_result)
                if analysis:
                    return analysis
            except Exception as e:
                current_app.logger.warning(f"Gemini API call failed, using heuristic defect analyzer: {e}")

        return cls._heuristic_defect_analyzer(bug_title, steps_to_reproduce, actual_result, expected_result)

    @staticmethod
    def _call_gemini_for_test_cases(api_key, module_name, requirement_text, test_type):
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        prompt = f"""
You are a Lead QA Automation & STQA Engineer for an Examination Management System (ParikshaVinyas).
Module: {module_name}
Requirement: {requirement_text}
Test Category: {test_type}

Generate 4 to 6 detailed, high-quality test cases following standard STQA testing methodology (Equivalence Partitioning, Boundary Value Analysis, Negative Testing).
Return ONLY a valid JSON array of objects with these keys:
- case_code: e.g. "TC_{module_name.upper()[:4]}_101"
- scenario: Short descriptive title
- preconditions: What system state is required
- test_input: Concrete input data
- expected_result: Clear expected verification
- test_technique: e.g. "Boundary Value Analysis", "Equivalence Partitioning", "Negative Testing", "State Transition"
- test_type: "Positive" or "Negative"
"""
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.2, "responseMimeType": "application/json"}
        }
        res = requests.post(url, json=payload, timeout=12)
        if res.status_code == 200:
            data = res.json()
            text = data['candidates'][0]['content']['parts'][0]['text']
            return json.loads(text)
        return None

    @staticmethod
    def _call_gemini_for_defect_analysis(api_key, bug_title, steps, actual, expected):
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        prompt = f"""
You are an STQA Quality Assurance Specialist debugging ParikshaVinyas (Flask/SQLAlchemy examination system).
Bug Title: {bug_title}
Steps to reproduce: {steps}
Actual Result: {actual}
Expected Result: {expected}

Analyze the defect and provide:
1. Probable Root Cause (database constraint, race condition, algorithm boundary error, validation gap)
2. Severity & Priority suggestion
3. Remediation / Fix Recommendation
4. Regression Testing Steps
Return concise structured markdown with bullet points.
"""
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.3}
        }
        res = requests.post(url, json=payload, timeout=12)
        if res.status_code == 200:
            data = res.json()
            return data['candidates'][0]['content']['parts'][0]['text']
        return None

    @staticmethod
    def _heuristic_test_case_generator(module_name, requirement_text, test_type):
        """
        Deterministic, comprehensive STQA heuristic test generation
        tailored for ParikshaVinyas modules.
        """
        mod = (module_name or 'General').strip().lower()
        cases = []

        if 'alloc' in mod or 'seat' in mod:
            cases = [
                {
                    "case_code": "TC_ALLOC_BVA_01",
                    "scenario": "Verify allocation when eligible students exactly equal available hall capacity",
                    "preconditions": "Exam scheduled with 40 eligible students; Hall A-101 has exactly 40 usable seats.",
                    "test_input": "Strategy: Sequential; Hall: A-101; Students: 40",
                    "expected_result": "System allocates all 40 students with 0 unallocated and 0 remaining seats.",
                    "test_technique": "Boundary Value Analysis (Exact Capacity)",
                    "test_type": "Positive"
                },
                {
                    "case_code": "TC_ALLOC_BVA_02",
                    "scenario": "Verify allocation rejection when student count exceeds available seats by 1",
                    "preconditions": "Exam scheduled with 41 eligible students; Hall A-101 has 40 seats.",
                    "test_input": "Strategy: Sequential; Students: 41; Hall usable seats: 40",
                    "expected_result": "System rolls back atomically, displays error: 'Insufficient seat capacity: Required 41, available 40'. No partial records created.",
                    "test_technique": "Boundary Value Analysis (Capacity + 1)",
                    "test_type": "Negative"
                },
                {
                    "case_code": "TC_ALLOC_NEG_03",
                    "scenario": "Attempt allocation to a damaged/blocked seat",
                    "preconditions": "Seat R01-C03 in Hall B-202 is marked as Blocked in database.",
                    "test_input": "Trigger auto or manual allocation targeting R01-C03.",
                    "expected_result": "Algorithm skips blocked seat R01-C03, allocating next available seat. Manual assignment fails with warning.",
                    "test_technique": "Negative Testing & Equivalence Partitioning",
                    "test_type": "Negative"
                },
                {
                    "case_code": "TC_ALLOC_MIX_04",
                    "scenario": "Verify Mixed Course allocation interleaves distinct branches in adjacent seats",
                    "preconditions": "Two courses (CS and ME) have 20 eligible candidates each in same hall.",
                    "test_input": "Strategy: Mixed Course; Total: 40 students",
                    "expected_result": "Adjacent seats alternate between CS and ME candidates, minimizing peer proximity.",
                    "test_technique": "Equivalence Partitioning & Combinatorial Testing",
                    "test_type": "Positive"
                },
                {
                    "case_code": "TC_ALLOC_CON_05",
                    "scenario": "Prevent double allocation of the same student in overlapping exam schedules",
                    "preconditions": "Student S1 already allocated in Hall A at 10:00 AM - 1:00 PM on Exam Date.",
                    "test_input": "Schedule another exam at 11:00 AM on same date; attempt allocation for S1.",
                    "expected_result": "System raises scheduling conflict validation error; student cannot be placed in two places concurrently.",
                    "test_technique": "Decision Table Testing (Temporal Conflict)",
                    "test_type": "Negative"
                }
            ]
        elif 'student' in mod:
            cases = [
                {
                    "case_code": "TC_STUD_VAL_01",
                    "scenario": "Valid student registration with complete details",
                    "preconditions": "Course and Department exist in system.",
                    "test_input": "Enrollment: EN2026101, Name: 'Aarav Sharma', Email: 'aarav@upluniversity.ac.in', Mobile: '9876543210', Sem: 6",
                    "expected_result": "Student record created successfully with 'Active' status and audit log registered.",
                    "test_technique": "Equivalence Partitioning (Valid Inputs)",
                    "test_type": "Positive"
                },
                {
                    "case_code": "TC_STUD_DUP_02",
                    "scenario": "Prevent duplicate student enrollment number insertion",
                    "preconditions": "Student with enrollment 'EN2026101' already exists in database.",
                    "test_input": "Attempt to create another student with enrollment 'EN2026101'.",
                    "expected_result": "System raises unique constraint validation error: 'Enrollment number already exists'.",
                    "test_technique": "Negative Testing / Unique Key Constraint",
                    "test_type": "Negative"
                },
                {
                    "case_code": "TC_STUD_BVA_03",
                    "scenario": "Verify semester range boundary limits (1 to 8)",
                    "preconditions": "Course configured with 8 semesters.",
                    "test_input": "Test inputs: Semester 0, Semester 8, Semester 9",
                    "expected_result": "Semester 8 accepted; Semester 0 and Semester 9 rejected with boundary error message.",
                    "test_technique": "Boundary Value Analysis (Min-1, Max, Max+1)",
                    "test_type": "Negative"
                },
                {
                    "case_code": "TC_STUD_CSV_04",
                    "scenario": "Bulk CSV import with valid and malformed rows",
                    "preconditions": "CSV file with 5 valid rows and 2 rows missing email/enrollment.",
                    "test_input": "Upload CSV file via Bulk Student Import form.",
                    "expected_result": "Valid rows imported successfully; invalid rows reported with specific line numbers and error reasons.",
                    "test_technique": "Error Guessing & Input Sanitization",
                    "test_type": "Positive"
                }
            ]
        elif 'hall' in mod:
            cases = [
                {
                    "case_code": "TC_HALL_DIM_01",
                    "scenario": "Create examination hall and verify automatic capacity calculation",
                    "preconditions": "Admin authenticated.",
                    "test_input": "Rows: 5, Cols: 8, Building: 'Main Wing', Floor: '2nd Floor'",
                    "expected_result": "Hall created with total capacity = 40 (5*8); usable capacity = 40.",
                    "test_technique": "Functional Equivalence",
                    "test_type": "Positive"
                },
                {
                    "case_code": "TC_HALL_BLK_02",
                    "scenario": "Block 3 seats in examination hall and verify usable capacity update",
                    "preconditions": "Hall total capacity = 50.",
                    "test_input": "Block seats R01-C01, R01-C02, R02-C05.",
                    "expected_result": "Usable capacity decreases from 50 to 47; blocked count displays 3; visual grid marks seats red.",
                    "test_technique": "State Transition Testing",
                    "test_type": "Positive"
                },
                {
                    "case_code": "TC_HALL_BVA_03",
                    "scenario": "Prevent negative or zero row/column dimensions for examination hall",
                    "preconditions": "Hall creation modal open.",
                    "test_input": "Rows: 0, Cols: -5",
                    "expected_result": "Form validation blocks submission with 'Row and column counts must be greater than zero'.",
                    "test_technique": "Boundary Value Analysis",
                    "test_type": "Negative"
                }
            ]
        else:
            cases = [
                {
                    "case_code": "TC_GEN_01",
                    "scenario": f"Verify {mod.capitalize()} standard workflow execution",
                    "preconditions": "System initialized and logged in.",
                    "test_input": f"Standard test dataset for {mod}.",
                    "expected_result": "Operation completes within 500ms with 200 OK status.",
                    "test_technique": "Equivalence Partitioning",
                    "test_type": "Positive"
                },
                {
                    "case_code": "TC_GEN_02",
                    "scenario": f"Verify unauthorized role access to {mod.capitalize()} administrative endpoint",
                    "preconditions": "Authenticated as Student role.",
                    "test_input": f"Navigate directly to /admin/{mod}",
                    "expected_result": "HTTP 403 Forbidden received; access blocked.",
                    "test_technique": "Security & Negative Testing",
                    "test_type": "Negative"
                }
            ]

        # Filter by test_type if specified
        if test_type in ['Positive', 'Negative']:
            return [c for c in cases if c['test_type'] == test_type]
        return cases

    @staticmethod
    def _heuristic_defect_analyzer(bug_title, steps, actual, expected):
        return f"""
### STQA Defect Diagnostic Report

**Bug Title:** {bug_title}

#### 1. Probable Root Cause Analysis
- **Analysis Category:** Business Logic / Constraint Violation
- **Hypothesis:** The application failed to enforce an atomic transactional lock or pre-condition validation before updating state.
- **Data Integrity Check:** Check for foreign key uniqueness or datetime interval overlaps in SQLAlchemy queries.

#### 2. Severity & Priority Recommendation
- **Suggested Severity:** High (Affects core examination scheduling or integrity)
- **Suggested Priority:** P1 / P2 (Requires resolution prior to exam day deployment)

#### 3. Recommended Remediation
- Wrap the operation in an explicit `db.session.begin_nested()` or transactional block with automatic rollback.
- Add an explicit validation check in the WTForm or Service layer before executing the SQL statement.
- Ensure unique constraint `(examination_id, student_id)` and `(examination_id, hall_id, row, col)` are respected.

#### 4. Automated Regression Verification
- Write a Pytest unit test reproducing the exact input sequence: `{steps[:80]}...`.
- Assert that expected result (`{expected[:80]}...`) is verified and database rollback functions cleanly.
"""

