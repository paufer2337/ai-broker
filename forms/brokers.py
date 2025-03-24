from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Email

class BrokerForm(FlaskForm):
    name = StringField('Broker name: ', validators=[DataRequired(), Length(min=5, max=50, message="Too short/long")])
    email = StringField('Contact email: ', validators=[Email()])
    webpage = StringField('Webpage: ')
    submit = SubmitField('Submit')