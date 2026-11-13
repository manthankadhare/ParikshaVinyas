from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, DateField, TimeField, SelectMultipleField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, NumberRange


class ExamForm(FlaskForm):
    exam_code = StringField('Exam Code (e.g. EX-CS601)', validators=[DataRequired(), Length(min=3, max=30)])
    exam_name = StringField('Examination Name', validators=[DataRequired(), Length(min=3, max=150)])
    course_id = SelectField('Course', coerce=int, validators=[DataRequired()])
    subject_id = SelectField('Subject', coerce=int, validators=[DataRequired()])
    semester = IntegerField('Semester', validators=[DataRequired(), NumberRange(min=1, max=8)])
    exam_date = DateField('Examination Date', validators=[DataRequired()])
    start_time = TimeField('Start Time', validators=[DataRequired()])
    end_time = TimeField('End Time', validators=[DataRequired()])
    duration_minutes = IntegerField('Duration (Minutes)', default=180, validators=[DataRequired(), NumberRange(min=30, max=360)])
    exam_type = SelectField('Exam Type', choices=[
        ('Regular', 'Regular Semester End Exam'),
        ('ATKT', 'ATKT / Backlog Exam'),
        ('Mid-Term', 'Mid-Term Exam'),
        ('Practical', 'Practical / Viva Exam')
    ], default='Regular')
    academic_year = StringField('Academic Year', default='2025-2026', validators=[DataRequired()])
    status = SelectField('Status', choices=[
        ('Scheduled', 'Scheduled'),
        ('Allocated', 'Allocated'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled')
    ], default='Scheduled')
    submit = SubmitField('Save Examination')


class AllocationWizardForm(FlaskForm):
    examination_id = SelectField('Examination', coerce=int, validators=[DataRequired()])
    strategy = SelectField('Allocation Strategy', choices=[
        ('Sequential', 'Sequential Allocation (by Enrollment No)'),
        ('Mixed Course', 'Mixed Course / Division Interleaved Allocation'),
        ('Random', 'Randomized Allocation (with reproducible seed)')
    ], default='Sequential')
    random_seed = IntegerField('Reproducible Random Seed (Optional)', validators=[], default=42)
    hall_ids = SelectMultipleField('Target Examination Halls', coerce=int, validators=[])
    force_reallocate = BooleanField('Regenerate / Overwrite Existing Allocation')
    submit = SubmitField('Generate Seat Allocations')


class ManualAllocationForm(FlaskForm):
    examination_id = SelectField('Examination', coerce=int, validators=[DataRequired()])
    student_id = SelectField('Student', coerce=int, validators=[DataRequired()])
    hall_id = SelectField('Hall', coerce=int, validators=[DataRequired()])
    row_num = IntegerField('Row', validators=[DataRequired(), NumberRange(min=1)])
    col_num = IntegerField('Column', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Assign Seat')

