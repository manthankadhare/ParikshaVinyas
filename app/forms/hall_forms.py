from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange


class HallForm(FlaskForm):
    hall_code = StringField('Hall Code (e.g. H-101)', validators=[DataRequired(), Length(min=2, max=30)])
    hall_name = StringField('Hall Name / Description', validators=[DataRequired(), Length(min=2, max=100)])
    building = StringField('Building / Block', validators=[DataRequired(), Length(min=2, max=100)])
    floor = StringField('Floor', validators=[DataRequired(), Length(min=1, max=20)])
    num_rows = IntegerField('Number of Rows', validators=[DataRequired(), NumberRange(min=1, max=25, message="Rows must be between 1 and 25")])
    num_cols = IntegerField('Number of Columns', validators=[DataRequired(), NumberRange(min=1, max=20, message="Columns must be between 1 and 20")])
    status = SelectField('Status', choices=[('Active', 'Active'), ('Maintenance', 'Maintenance'), ('Inactive', 'Inactive')], default='Active')
    submit = SubmitField('Save Hall')


class BlockSeatForm(FlaskForm):
    row_num = IntegerField('Row Number', validators=[DataRequired(), NumberRange(min=1)])
    col_num = IntegerField('Column Number', validators=[DataRequired(), NumberRange(min=1)])
    reason = StringField('Reason for Blocking', default='Damaged desk / Reserved', validators=[Length(max=200)])
    submit = SubmitField('Block Seat')

