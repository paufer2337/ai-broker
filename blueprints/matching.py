from flask import Blueprint, render_template
from model.mission import Mission
from extensions import db

matching_bp = Blueprint('matching', __name__)

@matching_bp.route('/')
def matching_dashboard():
    # Get latest missions, ordered by post date
    latest_missions = Mission.query.order_by(Mission.posted_date.desc()).all()
    return render_template('matching/dashboard.html', missions=latest_missions)