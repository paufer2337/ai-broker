import os
import sys
from datetime import datetime
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db
from model.mission import Mission
from model.broker import Broker

real_missions = [
    {
        "title": "Senior Security Consultant - Financial Sector",
        "description": "Major bank seeking security expert for critical infrastructure protection",
        "location": "Stockholm",
        "required_skills": "CISSP, Banking Security, Cloud Security",
        "broker_name": "Wise IT"  # This should match a broker name in your database
    },
    {
        "title": "Cyber Security Specialist",
        "description": "Leading tech company needs security specialist for product security",
        "location": "Gothenburg",
        "required_skills": "Application Security, Penetration Testing, OWASP",
        "broker_name": "Experis"
    },
    # Add more real missions here
]

with app.app_context():
    for mission_data in real_missions:
        broker_name = mission_data.pop('broker_name')
        broker = Broker.query.filter_by(name=broker_name).first()
        if broker:
            mission = Mission(broker_id=broker.id, **mission_data)
            db.session.add(mission)
    
    db.session.commit() 