from app import db


class Broker(db.Model):
    __tablename__ = 'brokers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True)
    email = db.Column(db.String(100))
    webpage = db.Column(db.String(200))
    description = db.Column(db.Text)
    location = db.Column(db.String(100))
    focus_areas = db.Column(db.String(200))  # Store as comma-separated values
    last_sync = db.Column(db.DateTime)  # For tracking when missions were last fetched

    