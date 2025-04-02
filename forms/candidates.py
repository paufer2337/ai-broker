from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Email

class CandidateForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[Email()])
    location = StringField('Location')
    core_skills = StringField('Core Skills')
    experience_years = IntegerField('Years of Experience')
    resume = FileField('Resume (PDF)', validators=[
        FileRequired(),
        FileAllowed(['pdf'], 'PDF files only!')
    ])
    submit = SubmitField('Add Candidate') 