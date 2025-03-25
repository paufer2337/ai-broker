from flask import Blueprint, render_template

candidates_bp = Blueprint('candidates', __name__)

@candidates_bp.route('/')
def candidate_index():
    return render_template('candidates/index.html')