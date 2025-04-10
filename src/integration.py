"""
Integration Module for Resume Matching AI Agent

This module provides integration code to connect the PDF processor
and matching engine with a Flask application.
"""

import os
from typing import Dict, List, Tuple, Optional
from flask import jsonify, request
from werkzeug.utils import secure_filename
from src.pdf_processor import PDFProcessor
from src.matching_engine import MatchingEngine


class ResumeMatchingAgent:
    """
    A class that integrates PDF processing and matching functionality
    for use in a Flask application.
    """
    
    def __init__(self, resume_upload_dir: str):
        """
        Initialize the ResumeMatchingAgent with necessary components.
        
        Args:
            resume_upload_dir: Directory where uploaded resumes are stored
        """
        self.pdf_processor = PDFProcessor()
        self.matching_engine = MatchingEngine()
        self.resume_upload_dir = resume_upload_dir
        
    def process_resume(self, resume_path: str) -> Tuple[str, List[str]]:
        """
        Process a resume and extract text and tags.
        
        Args:
            resume_path: Path to the resume PDF file
            
        Returns:
            Tuple containing processed text and extracted tags
        """
        # Process the resume
        processed_text, sections, tags = self.pdf_processor.process_resume(resume_path)
        
        return processed_text, tags
    
    def match_mission_with_candidates(
        self, 
        mission_tags: List[str], 
        candidate_resumes: Dict[str, str],
        top_k: int = 5
    ) -> List[Tuple[str, float]]:
        """
        Match a mission with candidate resumes and return top matches.
        
        Args:
            mission_tags: List of tags from the broker mission
            candidate_resumes: Dictionary mapping candidate IDs to resume texts
            top_k: Number of top matches to return
            
        Returns:
            List of tuples (candidate_id, similarity_score) for the top k matches
        """
        # Get top matches
        top_matches = self.matching_engine.get_top_matches(
            candidate_resumes, mission_tags, top_k=top_k
        )
        
        return top_matches
    
    def process_new_resume(self, resume_file_path: str, candidate_id: str) -> Dict:
        """
        Process a newly uploaded resume and return extracted information.
        
        Args:
            resume_file_path: Path to the uploaded resume file
            candidate_id: ID of the candidate
            
        Returns:
            Dictionary containing extracted information
        """
        try:
            # Process the resume
            processed_text, tags = self.process_resume(resume_file_path)
            
            # Return extracted information
            return {
                'candidate_id': candidate_id,
                'resume_text': processed_text,
                'tags': tags,
                'status': 'success'
            }
        except Exception as e:
            return {
                'candidate_id': candidate_id,
                'status': 'error',
                'error_message': str(e)
            }
    
    def process_new_mission(
        self, 
        mission_id: str, 
        mission_tags: List[str],
        candidate_data: Dict[str, Dict]
    ) -> Dict:
        """
        Process a new mission and find matching candidates.
        
        Args:
            mission_id: ID of the mission
            mission_tags: List of tags from the mission
            candidate_data: Dictionary mapping candidate IDs to their data
                (including resume_text)
            
        Returns:
            Dictionary containing matching results
        """
        try:
            # Extract resume texts
            candidate_resumes = {
                candidate_id: data['resume_text']
                for candidate_id, data in candidate_data.items()
                if 'resume_text' in data
            }
            
            # Match mission with candidates
            matches = self.match_mission_with_candidates(
                mission_tags, candidate_resumes
            )
            
            # Format results
            match_results = []
            for candidate_id, score in matches:
                match_results.append({
                    'candidate_id': candidate_id,
                    'score': score,
                    'candidate_data': candidate_data[candidate_id]
                })
            
            # Return results
            return {
                'mission_id': mission_id,
                'mission_tags': mission_tags,
                'matches': match_results,
                'status': 'success'
            }
        except Exception as e:
            return {
                'mission_id': mission_id,
                'status': 'error',
                'error_message': str(e)
            }


# Flask integration functions

def create_resume_matching_agent(resume_upload_dir: str) -> ResumeMatchingAgent:
    """
    Create and initialize a ResumeMatchingAgent.
    
    Args:
        resume_upload_dir: Directory where uploaded resumes are stored
        
    Returns:
        Initialized ResumeMatchingAgent
    """
    return ResumeMatchingAgent(resume_upload_dir)


def integrate_with_flask_app(app, db, agent: ResumeMatchingAgent):
    """
    Integrate the ResumeMatchingAgent with a Flask application.
    
    This function is a template that should be adapted to the specific
    database models and routes of the existing Flask application.
    
    Args:
        app: Flask application instance
        db: SQLAlchemy database instance
        agent: ResumeMatchingAgent instance
    """
    # Import models (these should be replaced with actual models from the application)
    # from models import Broker, Mission, Candidate
    
    # Example route for processing a new resume
    @app.route('/process_resume/<int:candidate_id>', methods=['POST'])
    def process_resume(candidate_id):
        """
        Process a newly uploaded resume.
        
        Args:
            candidate_id: ID of the candidate
            
        Returns:
            JSON response with processing results
        """
        # Check if the post request has the file part
        if 'resume' not in request.files:
            return jsonify({'status': 'error', 'message': 'No file part'}), 400
        
        file = request.files['resume']
        
        # If user does not select file, browser also submits an empty part without filename
        if file.filename == '':
            return jsonify({'status': 'error', 'message': 'No selected file'}), 400
        
        # Save the file
        filename = secure_filename(file.filename)
        file_path = os.path.join(agent.resume_upload_dir, filename)
        file.save(file_path)
        
        # Process the resume
        result = agent.process_new_resume(file_path, candidate_id)
        
        # Update candidate in database if processing was successful
        if result['status'] == 'success':
            # This should be adapted to the actual database models
            # candidate = Candidate.query.get(candidate_id)
            # if candidate:
            #     candidate.resume_text = result['resume_text']
            #     candidate.tags = ','.join(result['tags'])
            #     db.session.commit()
            pass
        
        return jsonify(result)
    
    # Example route for matching a mission with candidates
    @app.route('/match_mission/<int:mission_id>', methods=['GET'])
    def match_mission(mission_id):
        """
        Match a mission with candidates.
        
        Args:
            mission_id: ID of the mission
            
        Returns:
            JSON response with matching results
        """
        # This should be adapted to the actual database models
        # mission = Mission.query.get(mission_id)
        # if not mission:
        #     return jsonify({'status': 'error', 'message': 'Mission not found'}), 404
        
        # Get mission tags
        # mission_tags = mission.tags.split(',') if mission.tags else []
        mission_tags = []  # Replace with actual mission tags
        
        # Get candidate data
        # candidates = Candidate.query.all()
        # candidate_data = {
        #     str(candidate.id): {
        #         'name': candidate.name,
        #         'resume_text': candidate.resume_text,
        #         'tags': candidate.tags.split(',') if candidate.tags else []
        #     }
        #     for candidate in candidates
        #     if candidate.resume_text
        # }
        candidate_data = {}  # Replace with actual candidate data
        
        # Match mission with candidates
        result = agent.process_new_mission(str(mission_id), mission_tags, candidate_data)
        
        return jsonify(result)
