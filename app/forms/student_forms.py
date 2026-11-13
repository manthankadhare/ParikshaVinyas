from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Length, NumberRange


class StudentForm(FlaskForm):
    enrollment_no = StringField('Enrollment Number', validators=[DataRequired(), Length(min=4, max=30)])
    full_name = StringField('Full Name', validators=[DataRequired(), Length(min=3, max=120)])
    email = StringField('Email Address', validators=[DataRequired(), Email(), Length(max=120)])
    mobile = StringField('Mobile Number', validators=[DataRequired(), Length(min=10, max=15)])
    course_id = SelectField('Course', coerce=int, validators=[DataRequired()])
    branch = StringField('Branch / Specialization', validators=[DataRequired(), Length(max=80)])
    semester = IntegerField('Semester', validators=[DataRequired(), NumberRange(min=1, max=8, message="Semester must be between 1 and 8")])
    division = StringField('Division', validators=[DataRequired(), Length(min=1, max=5)])
    academic_year = StringField('Academic Year', default='2025-2026', validators=[DataRequired()])
    status = SelectField('Status', choices=[('Active', 'Active'), ('Detained', 'Detained'), ('Inactive', 'Inactive')], default='Active')
    submit = SubmitField('Save Student')


class StudentCSVUploadForm(FlaskForm):
    csv_file = FileField('CSV File', validators=[
        FileRequired(),
        FileAllowed(['csv'], 'Only CSV files are allowed!')
    ])
    submit = SubmitField('Upload and Import')

