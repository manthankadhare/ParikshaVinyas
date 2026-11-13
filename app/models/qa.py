from datetime import datetime
from app import db


class TestCase(db.Model):
    __tablename__ = 'test_cases'

    id = db.Column(db.Integer, primary_key=True)
    case_code = db.Column(db.String(30), unique=True, nullable=False, index=True)  # e.g., TC_ALLOC_001
    module = db.Column(db.String(60), nullable=False)  # Allocation, Student, Hall, Exam, Auth, Security
    scenario = db.Column(db.String(255), nullable=False)
    preconditions = db.Column(db.Text, nullable=True)
    test_input = db.Column(db.Text, nullable=True)
    expected_result = db.Column(db.Text, nullable=False)
    actual_result = db.Column(db.Text, nullable=True)
    test_technique = db.Column(db.String(50), default='Functional Testing')  # BVA, Equivalence Partitioning, Negative Testing, etc.
    test_type = db.Column(db.String(20), default='Positive')  # Positive, Negative
    status = db.Column(db.String(20), default='Not Executed')  # Not Executed, Pass, Fail, Blocked
    tester_name = db.Column(db.String(80), default='STQA QA Engineer')
    execution_date = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    defects = db.relationship('DefectReport', back_populates='test_case', lazy='dynamic')

    def __repr__(self):
        return f'<TestCase {self.case_code}: {self.scenario} [{self.status}]>'


class DefectReport(db.Model):
    __tablename__ = 'defect_reports'

    id = db.Column(db.Integer, primary_key=True)
    bug_code = db.Column(db.String(30), unique=True, nullable=False, index=True)  # e.g., BUG_SEC_001
    test_case_id = db.Column(db.Integer, db.ForeignKey('test_cases.id'), nullable=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    steps_to_reproduce = db.Column(db.Text, nullable=False)
    expected_result = db.Column(db.Text, nullable=False)
    actual_result = db.Column(db.Text, nullable=False)
    severity = db.Column(db.String(20), default='Medium')  # Critical, High, Medium, Low
    priority = db.Column(db.String(10), default='P2')  # P1, P2, P3, P4
    status = db.Column(db.String(20), default='Open')  # New, Open, In Progress, Resolved, Closed
    assigned_to = db.Column(db.String(80), default='Lead Developer')
    screenshot_path = db.Column(db.String(255), nullable=True)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    resolved_date = db.Column(db.DateTime, nullable=True)

    # Relationships
    test_case = db.relationship('TestCase', back_populates='defects')

    def __repr__(self):
        return f'<DefectReport {self.bug_code}: {self.title} [{self.severity}|{self.status}]>'

