from extensions import db
from flask import Flask, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Hemlig Nyckel'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sqlite3'

bootstrap = Bootstrap(app)
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