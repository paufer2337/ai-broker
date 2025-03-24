from extensions import db
from flask import Flask, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Hemlig Nyckel'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sqlite3'

bootstrap = Bootstrap(app)
db.init_app(app)

# register the blueprints in app
from blueprints.brokers import brokers_bp
app.register_blueprint(brokers_bp)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)