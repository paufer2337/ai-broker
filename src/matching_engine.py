"""
Matching Engine Module for Resume Matching AI Agent

This module provides a lighter-weight alternative to sentence-transformers
for matching broker mission tags with candidate resumes.
It implements semantic matching using TF-IDF and cosine similarity.
"""

import re
import math
import string
from typing import Dict, List, Tuple, Set
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from collections import Counter


class MatchingEngine:
    """
    A class for matching broker mission tags with candidate resumes.
    
    This class uses TF-IDF and cosine similarity to perform semantic matching
    between mission tags and resume content.
    """
    
    def __init__(self):
        """
        Initialize the MatchingEngine with necessary NLTK resources.
        """
        # Download required NLTK resources
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
            
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('stopwords')
            
        try:
            nltk.data.find('corpora/wordnet')
        except LookupError:
            nltk.download('wordnet')
        
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()
        
    def preprocess_text(self, text: str) -> List[str]:
        """
        Preprocess text by tokenizing, removing stopwords, and lemmatizing.
        
        Args:
            text: Raw text to preprocess
            
        Returns:
            List of preprocessed tokens
        """
        # Convert to lowercase
        text = text.lower()
        
        # Remove punctuation
        text = text.translate(str.maketrans('', '', string.punctuation))
        
        # Simple tokenization using split instead of NLTK's word_tokenize
        # to avoid dependency on punkt_tab
        tokens = text.split()
        
        # Remove stopwords and lemmatize
        tokens = [
            self.lemmatizer.lemmatize(token) 
            for token in tokens 
            if token not in self.stop_words and len(token) > 2
        ]
        
        return tokens
    
    def calculate_tf(self, tokens: List[str]) -> Dict[str, float]:
        """
        Calculate term frequency for a list of tokens.
        
        Args:
            tokens: List of preprocessed tokens
            
        Returns:
            Dictionary mapping tokens to their term frequencies
        """
        # Count occurrences of each token
        token_counts = Counter(tokens)
        
        # Calculate term frequency
        total_tokens = len(tokens)
        tf = {token: count / total_tokens for token, count in token_counts.items()}
        
        return tf
    
    def calculate_idf(self, documents: List[List[str]]) -> Dict[str, float]:
        """
        Calculate inverse document frequency for a collection of documents.
        
        Args:
            documents: List of preprocessed document tokens
            
        Returns:
            Dictionary mapping tokens to their inverse document frequencies
        """
        # Count documents containing each token
        num_documents = len(documents)
        document_counts = {}
        
        # Create a set of unique tokens in each document
        document_token_sets = [set(doc) for doc in documents]
        
        # Count documents containing each token
        all_tokens = set()
        for doc_tokens in document_token_sets:
            all_tokens.update(doc_tokens)
            
        for token in all_tokens:
            document_counts[token] = sum(1 for doc_tokens in document_token_sets if token in doc_tokens)
        
        # Calculate IDF
        idf = {token: math.log(num_documents / (count + 1)) + 1 for token, count in document_counts.items()}
        
        return idf
    
    def calculate_tfidf(self, tf: Dict[str, float], idf: Dict[str, float]) -> Dict[str, float]:
        """
        Calculate TF-IDF scores for a document.
        
        Args:
            tf: Term frequency dictionary
            idf: Inverse document frequency dictionary
            
        Returns:
            Dictionary mapping tokens to their TF-IDF scores
        """
        tfidf = {token: tf_value * idf.get(token, 0) for token, tf_value in tf.items()}
        return tfidf
    
    def cosine_similarity(self, vec1: Dict[str, float], vec2: Dict[str, float]) -> float:
        """
        Calculate cosine similarity between two vectors.
        
        Args:
            vec1: First vector as a dictionary
            vec2: Second vector as a dictionary
            
        Returns:
            Cosine similarity score between 0 and 1
        """
        # Find common tokens
        common_tokens = set(vec1.keys()) & set(vec2.keys())
        
        # Calculate dot product
        dot_product = sum(vec1[token] * vec2[token] for token in common_tokens)
        
        # Calculate magnitudes
        magnitude1 = math.sqrt(sum(value ** 2 for value in vec1.values()))
        magnitude2 = math.sqrt(sum(value ** 2 for value in vec2.values()))
        
        # Avoid division by zero
        if magnitude1 == 0 or magnitude2 == 0:
            return 0
        
        # Calculate cosine similarity
        similarity = dot_product / (magnitude1 * magnitude2)
        
        return similarity
    
    def expand_tags(self, tags: List[str]) -> List[str]:
        """
        Expand tags with related terms to improve matching.
        
        Args:
            tags: List of original tags
            
        Returns:
            List of expanded tags
        """
        # This is a simplified implementation
        # In a more advanced version, you could use WordNet or a domain-specific
        # dictionary to find synonyms and related terms
        
        expanded_tags = []
        
        # Simple expansions for common programming terms
        expansions = {
            'python': ['py', 'python3', 'programming'],
            'javascript': ['js', 'ecmascript', 'frontend'],
            'java': ['jvm', 'programming'],
            'c++': ['cpp', 'programming'],
            'react': ['reactjs', 'frontend', 'ui'],
            'angular': ['angularjs', 'frontend', 'ui'],
            'vue': ['vuejs', 'frontend', 'ui'],
            'node': ['nodejs', 'backend', 'server'],
            'flask': ['python', 'backend', 'web'],
            'django': ['python', 'backend', 'web'],
            'sql': ['database', 'query'],
            'nosql': ['database', 'mongodb'],
            'aws': ['cloud', 'amazon'],
            'azure': ['cloud', 'microsoft'],
            'gcp': ['cloud', 'google'],
            'docker': ['container', 'devops'],
            'kubernetes': ['k8s', 'container', 'devops'],
            'git': ['version control', 'github'],
            'agile': ['scrum', 'methodology'],
            'scrum': ['agile', 'methodology'],
            'machine learning': ['ml', 'ai', 'data science'],
            'artificial intelligence': ['ai', 'ml'],
            'data science': ['analytics', 'statistics'],
        }
        
        # Add original tags
        expanded_tags.extend(tags)
        
        # Add expansions
        for tag in tags:
            tag_lower = tag.lower()
            if tag_lower in expansions:
                expanded_tags.extend(expansions[tag_lower])
        
        # Remove duplicates and return
        return list(set(expanded_tags))
    
    def match_resume_with_mission(self, resume_text: str, mission_tags: List[str]) -> float:
        """
        Match a resume with mission tags and return a similarity score.
        
        Args:
            resume_text: Preprocessed text from a resume
            mission_tags: List of tags from a broker mission
            
        Returns:
            Similarity score between 0 and 1
        """
        # Preprocess resume text
        resume_tokens = self.preprocess_text(resume_text)
        
        # Expand mission tags
        expanded_tags = self.expand_tags(mission_tags)
        mission_text = ' '.join(expanded_tags)
        mission_tokens = self.preprocess_text(mission_text)
        
        # Create a corpus with both documents
        corpus = [resume_tokens, mission_tokens]
        
        # Calculate TF for each document
        resume_tf = self.calculate_tf(resume_tokens)
        mission_tf = self.calculate_tf(mission_tokens)
        
        # Calculate IDF for the corpus
        corpus_idf = self.calculate_idf(corpus)
        
        # Calculate TF-IDF for each document
        resume_tfidf = self.calculate_tfidf(resume_tf, corpus_idf)
        mission_tfidf = self.calculate_tfidf(mission_tf, corpus_idf)
        
        # Calculate cosine similarity
        similarity = self.cosine_similarity(resume_tfidf, mission_tfidf)
        
        return similarity
    
    def rank_candidates(self, resumes: Dict[str, str], mission_tags: List[str]) -> List[Tuple[str, float]]:
        """
        Rank candidates based on how well their resumes match the mission tags.
        
        Args:
            resumes: Dictionary mapping candidate IDs to resume texts
            mission_tags: List of tags from a broker mission
            
        Returns:
            List of tuples (candidate_id, similarity_score) sorted by score in descending order
        """
        # Calculate similarity scores for each candidate
        scores = []
        for candidate_id, resume_text in resumes.items():
            similarity = self.match_resume_with_mission(resume_text, mission_tags)
            scores.append((candidate_id, similarity))
        
        # Sort by similarity score in descending order
        scores.sort(key=lambda x: x[1], reverse=True)
        
        return scores
    
    def get_top_matches(self, resumes: Dict[str, str], mission_tags: List[str], top_k: int = 5) -> List[Tuple[str, float]]:
        """
        Get the top k candidates that best match the mission tags.
        
        Args:
            resumes: Dictionary mapping candidate IDs to resume texts
            mission_tags: List of tags from a broker mission
            top_k: Number of top matches to return
            
        Returns:
            List of tuples (candidate_id, similarity_score) for the top k matches
        """
        # Rank all candidates
        ranked_candidates = self.rank_candidates(resumes, mission_tags)
        
        # Return top k
        return ranked_candidates[:top_k]


# Example usage
if __name__ == "__main__":
    # Initialize the matching engine
    engine = MatchingEngine()
    
    # Example resumes
    resumes = {
        "candidate1": "Experienced software developer with 5 years of Python and Flask development. Skilled in building web applications and RESTful APIs.",
        "candidate2": "Frontend developer with expertise in React, Angular, and Vue. 3 years of experience in building responsive web applications.",
        "candidate3": "DevOps engineer with experience in AWS, Docker, and Kubernetes. Skilled in CI/CD pipelines and infrastructure as code.",
        "candidate4": "Data scientist with expertise in machine learning and statistical analysis. Proficient in Python, R, and SQL.",
        "candidate5": "Backend developer with Java and Spring Boot experience. Skilled in database design and optimization."
    }
    
    # Example mission tags
    mission_tags = ["Python", "Flask", "Web Development"]
    
    # Get top matches
    top_matches = engine.get_top_matches(resumes, mission_tags, top_k=3)
    
    # Print results
    print(f"Top matches for mission tags: {mission_tags}")
    for candidate_id, score in top_matches:
        print(f"{candidate_id}: {score:.4f} - {resumes[candidate_id][:50]}...")
