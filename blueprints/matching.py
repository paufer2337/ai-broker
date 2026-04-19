from flask import Blueprint, request, jsonify, current_app, render_template
from werkzeug.utils import secure_filename
import os
from model.candidate import Candidate
from model.mission import Mission
from model.broker import Broker
from extensions import db
from datetime import datetime
from src.pdf_processor import PDFProcessor
from src.matching_engine import MatchingEngine

matching_bp = Blueprint('matching', __name__)
pdf_processor = PDFProcessor()
matching_engine = MatchingEngine()

@matching_bp.route('/process_resume/<int:candidate_id>', methods=['POST'])
def process_resume(candidate_id):
    """Process a candidate's resume and extract text and tags"""
    candidate = Candidate.query.get_or_404(candidate_id)
    
    if not candidate.resume_path:
        return jsonify({'status': 'error', 'message': 'No resume file found for this candidate'}), 400
    
    resume_path = os.path.join(current_app.root_path, candidate.resume_path)
    
    try:
        # Process the resume
        processed_text, sections, tags = pdf_processor.process_resume(resume_path)
        
        # Update candidate in database
        candidate.resume_text = processed_text
        candidate.extracted_tags = ','.join(tags)
        candidate.last_processed = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'candidate_id': candidate_id,
            'tags': tags,
            'sections': {k: v[:100] + '...' if len(v) > 100 else v for k, v in sections.items()}
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@matching_bp.route('/match_mission/<int:mission_id>', methods=['GET'])
def match_mission(mission_id):
    """Match a mission with candidates based on tags and resume content"""
    mission = Mission.query.get_or_404(mission_id)
    
    # Get mission tags
    if mission.required_skills_tags:
        mission_tags = mission.required_skills_tags.split(',')
    elif mission.required_skills:
        # If no specific tags, use the required skills
        mission_tags = mission.required_skills.split(',')
    else:
        return jsonify({'status': 'error', 'message': 'No skills or tags found for this mission'}), 400
    
    # Get candidates with processed resumes
    candidates = Candidate.query.filter(Candidate.resume_text.isnot(None)).all()
    
    if not candidates:
        return jsonify({'status': 'error', 'message': 'No processed candidate resumes found'}), 404
    
    # Prepare candidate data for matching
    candidate_resumes = {
        str(candidate.id): candidate.resume_text
        for candidate in candidates
    }
    
    # Match mission with candidates
    matches = matching_engine.get_top_matches(candidate_resumes, mission_tags, top_k=5)
    
    # Format results
    results = []
    for candidate_id, score in matches:
        candidate = Candidate.query.get(int(candidate_id))
        results.append({
            'candidate_id': candidate_id,
            'name': candidate.name,
            'score': float(score),
            'core_skills': candidate.core_skills,
            'location': candidate.location,
            'experience_years': candidate.experience_years
        })
    
    return jsonify({
        'status': 'success',
        'mission_id': mission_id,
        'mission_title': mission.title,
        'mission_tags': mission_tags,
        'matches': results
    })

@matching_bp.route('/process_all_resumes', methods=['POST'])
def process_all_resumes():
    """Process all unprocessed candidate resumes"""
    candidates = Candidate.query.filter(
        (Candidate.resume_path.isnot(None)) & 
        ((Candidate.resume_text.is_(None)) | (Candidate.extracted_tags.is_(None)))
    ).all()
    
    results = []
    for candidate in candidates:
        resume_path = os.path.join(current_app.root_path, candidate.resume_path)
        
        try:
            # Process the resume
            processed_text, sections, tags = pdf_processor.process_resume(resume_path)
            
            # Update candidate in database
            candidate.resume_text = processed_text
            candidate.extracted_tags = ','.join(tags)
            candidate.last_processed = datetime.utcnow()
            
            results.append({
                'candidate_id': candidate.id,
                'name': candidate.name,
                'status': 'success',
                'tags': tags
            })
        except Exception as e:
            results.append({
                'candidate_id': candidate.id,
                'name': candidate.name,
                'status': 'error',
                'message': str(e)
            })
    
    db.session.commit()
    
    return jsonify({
        'status': 'success',
        'processed_count': len(candidates),
        'results': results
    })

@matching_bp.route('/mission/<int:mission_id>')
def mission_detail(mission_id):
    """Show detailed information about a specific mission"""
    mission = Mission.query.get_or_404(mission_id)
    return render_template('matching/mission_detail.html', mission=mission)

@matching_bp.route('/dashboard')
def matching_dashboard():
    """Show the matching dashboard with recent missions and matches"""
    missions = Mission.query.order_by(Mission.posted_date.desc()).limit(10).all()
    candidates = Candidate.query.all()
    brokers = Broker.query.all()
    return render_template('matching/dashboard.html', 
                         missions=missions,
                         candidates=candidates,
                         brokers=brokers)