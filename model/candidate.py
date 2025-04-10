from extensions import db
from datetime import datetime

class Candidate(db.Model):
    __tablename__ = 'candidates'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    location = db.Column(db.String(100))
    core_skills = db.Column(db.String(200))  # Main skills to display in the preview
    experience_years = db.Column(db.Integer)
    resume_path = db.Column(db.String(200))  # Path to stored PDF
    added_date = db.Column(db.DateTime, default=datetime.utcnow)
    resume_text = db.Column(db.Text)  # Extracted text from resume
    extracted_tags = db.Column(db.Text)  # Comma-separated list of extracted tags
    last_processed = db.Column(db.DateTime)  # When the resume was last processed