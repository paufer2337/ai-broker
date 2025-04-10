"""
Test module for the Matching Engine

This module provides testing functionality for the Matching Engine module.
It tests the text preprocessing, tag expansion, and matching functionality.
"""

import sys
import os
from typing import Dict, List, Tuple

# Add the parent directory to the path so we can import the matching_engine module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.matching_engine import MatchingEngine


def test_matching_engine():
    """
    Test the Matching Engine functionality.
    """
    # Initialize the matching engine
    engine = MatchingEngine()
    
    # Test text preprocessing
    print("\n=== TESTING TEXT PREPROCESSING ===")
    sample_text = "Python developer with 5+ years of experience in Flask and Django frameworks."
    tokens = engine.preprocess_text(sample_text)
    print(f"Original text: {sample_text}")
    print(f"Preprocessed tokens: {tokens}")
    
    # Test tag expansion
    print("\n=== TESTING TAG EXPANSION ===")
    sample_tags = ["Python", "Flask", "Web Development"]
    expanded_tags = engine.expand_tags(sample_tags)
    print(f"Original tags: {sample_tags}")
    print(f"Expanded tags: {expanded_tags}")
    
    # Test matching functionality with sample resumes
    print("\n=== TESTING MATCHING FUNCTIONALITY ===")
    
    # Sample resumes
    resumes = {
        "candidate1": "Experienced software developer with 5 years of Python and Flask development. Skilled in building web applications and RESTful APIs.",
        "candidate2": "Frontend developer with expertise in React, Angular, and Vue. 3 years of experience in building responsive web applications.",
        "candidate3": "DevOps engineer with experience in AWS, Docker, and Kubernetes. Skilled in CI/CD pipelines and infrastructure as code.",
        "candidate4": "Data scientist with expertise in machine learning and statistical analysis. Proficient in Python, R, and SQL.",
        "candidate5": "Backend developer with Java and Spring Boot experience. Skilled in database design and optimization."
    }
    
    # Test different mission tags
    test_missions = [
        {
            "name": "Python Web Developer",
            "tags": ["Python", "Flask", "Web Development"]
        },
        {
            "name": "Frontend Developer",
            "tags": ["JavaScript", "React", "UI/UX"]
        },
        {
            "name": "DevOps Engineer",
            "tags": ["AWS", "Docker", "CI/CD"]
        },
        {
            "name": "Data Scientist",
            "tags": ["Python", "Machine Learning", "Statistics"]
        }
    ]
    
    # Test each mission
    for mission in test_missions:
        print(f"\nMission: {mission['name']}")
        print(f"Tags: {mission['tags']}")
        
        # Get top matches
        top_matches = engine.get_top_matches(resumes, mission['tags'], top_k=3)
        
        # Print results
        print("Top 3 matches:")
        for i, (candidate_id, score) in enumerate(top_matches, 1):
            print(f"{i}. {candidate_id}: {score:.4f} - {resumes[candidate_id][:50]}...")
    
    return True


if __name__ == "__main__":
    test_matching_engine()