from app import app, db
from model.broker import Broker


with app.app_context():
    db.create_all()