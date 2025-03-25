from app import app, db
from model.broker import Broker
from model.mission import Mission

with app.app_context():
    db.create_all()
    
    db.session.commit()