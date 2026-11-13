from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length


class TestCaseForm(FlaskForm):
    case_code = StringField('Test Case ID (e.g. TC_ALLOC_001)', validators=[DataRequired(), Length(max=30)])
    module = SelectField('Module', choices=[
        ('Allocation Engine', 'Allocation Engine'),
        ('Student Management', 'Student Management'),
        ('Hall Management', 'Hall Management'),
        ('Exam Scheduling', 'Exam Scheduling'),
        ('Authentication & Security', 'Authentication & Security'),
        ('Reports & PDF', 'Reports & PDF')
    ], default='Allocation Engine')
    scenario = StringField('Test Scenario', validators=[DataRequired(), Length(max=255)])
    preconditions = TextAreaField('Preconditions')
    test_input = TextAreaField('Test Input Data')
    expected_result = TextAreaField('Expected Result', validators=[DataRequired()])
    actual_result = TextAreaField('Actual Result')
    test_technique = SelectField('STQA Technique', choices=[
        ('Boundary Value Analysis (BVA)', 'Boundary Value Analysis (BVA)'),
        ('Equivalence Partitioning (EP)', 'Equivalence Partitioning (EP)'),
        ('Negative Testing', 'Negative Testing'),
        ('Decision Table Testing', 'Decision Table Testing'),
        ('State Transition Testing', 'State Transition Testing'),
        ('Error Guessing', 'Error Guessing'),
        ('Security & Role Testing', 'Security & Role Testing'),
        ('Usability Testing', 'Usability Testing')
    ], default='Equivalence Partitioning (EP)')
    test_type = SelectField('Test Type', choices=[('Positive', 'Positive Scenario'), ('Negative', 'Negative Scenario')], default='Positive')
    status = SelectField('Execution Status', choices=[
        ('Not Executed', 'Not Executed'),
        ('Pass', 'Pass'),
        ('Fail', 'Fail'),
        ('Blocked', 'Blocked')
    ], default='Not Executed')
    tester_name = StringField('Tester Name', default='STQA QA Lead', validators=[Length(max=80)])
    submit = SubmitField('Save Test Case')


class DefectReportForm(FlaskForm):
    bug_code = StringField('Defect / Bug ID (e.g. BUG_ALLOC_001)', validators=[DataRequired(), Length(max=30)])
    test_case_id = SelectField('Related Test Case', coerce=int, validators=[])
    title = StringField('Bug Title / Summary', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Defect Description', validators=[DataRequired()])
    steps_to_reproduce = TextAreaField('Steps to Reproduce', validators=[DataRequired()])
    expected_result = TextAreaField('Expected Result', validators=[DataRequired()])
    actual_result = TextAreaField('Actual Result', validators=[DataRequired()])
    severity = SelectField('Severity', choices=[
        ('Critical', 'Critical'),
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Low', 'Low')
    ], default='High')
    priority = SelectField('Priority', choices=[
        ('P1', 'P1 - Urgent'),
        ('P2', 'P2 - High'),
        ('P3', 'P3 - Medium'),
        ('P4', 'P4 - Low')
    ], default='P2')
    status = SelectField('Defect Status', choices=[
        ('New', 'New'),
        ('Open', 'Open'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
        ('Closed', 'Closed')
    ], default='Open')
    assigned_to = StringField('Assigned To', default='Lead Backend Developer', validators=[Length(max=80)])
    submit = SubmitField('Submit Defect Report')


class AIGeneratorForm(FlaskForm):
    module_name = SelectField('Target Module', choices=[
        ('Allocation Engine', 'Allocation Engine & Seating Algorithm'),
        ('Student Management', 'Student Management & CSV Import'),
        ('Examination Hall', 'Examination Hall & Grid Configuration'),
        ('Exam Scheduling', 'Exam Scheduling & Conflict Detector'),
        ('Authentication & RBAC', 'Authentication & Role-Based Access')
    ], default='Allocation Engine')
    requirement_text = TextAreaField('Feature Requirement / User Story', validators=[DataRequired()])
    test_type = SelectField('Category Filter', choices=[
        ('All', 'All Categories (Positive, Negative, BVA, Edge Cases)'),
        ('Positive', 'Positive Scenarios Only'),
        ('Negative', 'Negative & Failure Scenarios Only')
    ], default='All')
    submit = SubmitField('Generate Test Cases with AI Engine')

