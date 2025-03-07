from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from wtforms import render_template

app = Flask(__name__)
#db = SQLAlchemy(app)



app.route('/')
def index():
    return render_template('templates/index.html')



app.run(debug=True)