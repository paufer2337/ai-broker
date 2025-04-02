from app import app, db
from model.broker import Broker
from model.mission import Mission
from model.candidate import Candidate

with app.app_context():
    db.create_all()
    
    db.session.commit()