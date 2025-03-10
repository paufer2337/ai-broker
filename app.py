from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask import render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Email
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Hemlig Nyckel'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sqlite3'

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)


class BrokerForm(FlaskForm):
    name = StringField('Broker name: ', validators=[DataRequired(), Length(min=5, max=50, message="Too short/long")])
    email = StringField('Contact email: ', validators=[Email()])
    webpage = StringField('Webpage: ')
    submit = SubmitField('Submit')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/broker')
def broker_index():
    form = BrokerForm()
    return render_template('brokers/index.html', form=form)

@app.route('/broker', methods=['POST'])
def broker_post():
    form = BrokerForm()
    
    if (form.validate_on_submit()):
        print('Saving to database...')
        return 'Saving to database...'

    else: 
        return render_template('brokers/index.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)