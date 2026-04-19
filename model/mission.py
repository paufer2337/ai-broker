from extensions import db
from datetime import datetime

class Mission(db.Model):
    __tablename__ = 'missions'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    description = db.Column(db.Text)
    location = db.Column(db.String(100))
    required_skills = db.Column(db.String(200))
    posted_date = db.Column(db.DateTime, default=datetime.utcnow)
    broker_id = db.Column(db.Integer, db.ForeignKey('brokers.id'))
    broker = db.relationship('Broker', backref='missions', lazy=True)
    start_date = db.Column(db.DateTime)
    duration = db.Column(db.String(50))  
    rate = db.Column(db.String(50)) 
    status = db.Column(db.String(50), default='active')
    required_skills_tags = db.Column(db.Text)  