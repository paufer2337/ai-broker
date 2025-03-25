from flask import Blueprint, render_template, redirect, url_for
from model.mission import Mission
from extensions import db
from scrapers.manager import ScraperManager
from model.broker import Broker

matching_bp = Blueprint('matching', __name__)

@matching_bp.route('/')
def matching_dashboard():
    # Get all brokers and their mission links
    brokers = Broker.query.all()
    return render_template('matching/dashboard.html', brokers=brokers)

@matching_bp.route('/update', methods=['POST'])
def update_missions():
    ScraperManager.update_missions(db)
    return redirect(url_for('matching.matching_dashboard'))