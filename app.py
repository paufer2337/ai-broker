from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import render_template

app = Flask(__name__)
#db = SQLAlchemy(app)



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/broker')
def broker_index():
    return render_template('brokers/index.html')

app.run(debug=True)