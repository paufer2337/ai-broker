from app import db


class Broker(db.Model):
    __tablename__ = 'brokers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), index=True, unique=True)
    email = db.Column(db.String(50))
    webpage = db.Column(db.String(50))

    