from extensions import db
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf.csrf import CSRFProtect
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Hemlig Nyckel'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sqlite3'

# Configure upload folder
UPLOAD_FOLDER = os.path.join(app.root_path, 'uploads', 'resumes')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

bootstrap = Bootstrap(app)
csrf = CSRFProtect(app)
db.init_app(app)

# register the blueprints
from blueprints.brokers import brokers_bp
from blueprints.candidate import candidates_bp
from blueprints.matching import matching_bp

app.register_blueprint(brokers_bp, url_prefix='/brokers')
app.register_blueprint(candidates_bp, url_prefix='/candidates')
app.register_blueprint(matching_bp, url_prefix='/matches')

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)