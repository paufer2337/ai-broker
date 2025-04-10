"""
PDF Processing Module for Resume Matching AI Agent

This module handles the extraction of text from PDF resumes using PDFMiner.
It provides functionality to process PDF files, extract text content,
and perform basic preprocessing on the extracted text.
"""

import os
import re
from typing import Dict, List, Optional, Tuple

from pdfminer.high_level import extract_text
from pdfminer.layout import LAParams


class PDFProcessor:
    """
    A class for processing PDF resumes and extracting text content.
    
    This class uses PDFMiner to extract text from PDF files and provides
    methods for cleaning and preprocessing the extracted text.
    """
    
    def __init__(self, laparams: Optional[LAParams] = None):
        """
        Initialize the PDFProcessor with optional layout parameters.
        
        Args:
            laparams: Layout parameters for PDFMiner text extraction
        """
        self.laparams = laparams or LAParams(
            line_margin=0.5,
            word_margin=0.1,
            char_margin=2.0,
            all_texts=True
        )
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """
        Extract text from a PDF file.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Extracted text from the PDF
            
        Raises:
            FileNotFoundError: If the PDF file does not exist
            ValueError: If the file is not a valid PDF
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        if not pdf_path.lower().endswith('.pdf'):
            raise ValueError(f"File is not a PDF: {pdf_path}")
        
        try:
            text = extract_text(pdf_path, laparams=self.laparams)
            return text
        except Exception as e:
            raise ValueError(f"Error extracting text from PDF: {e}")
    
    def preprocess_text(self, text: str) -> str:
        """
        Preprocess the extracted text to clean it up.
        
        Args:
            text: Raw text extracted from PDF
            
        Returns:
            Preprocessed text
        """
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters that aren't useful
        text = re.sub(r'[^\w\s.,;:!?@#$%&*()-+=]', '', text)
        
        # Normalize whitespace around punctuation
        text = re.sub(r'\s*([.,;:!?])\s*', r'\1 ', text)
        
        # Remove leading/trailing whitespace
        text = text.strip()
        
        return text
    
    def identify_sections(self, text: str) -> Dict[str, str]:
        """
        Attempt to identify common resume sections in the text.
        
        Args:
            text: Preprocessed text from resume
            
        Returns:
            Dictionary with section names as keys and section content as values
        """
        # Common section headers in resumes
        section_patterns = {
            'education': r'(?i)education|academic|degree|university|college|school',
            'experience': r'(?i)experience|employment|work history|job history|professional experience',
            'skills': r'(?i)skills|technical skills|competencies|expertise|proficiencies',
            'projects': r'(?i)projects|portfolio|works',
            'certifications': r'(?i)certifications|certificates|licenses',
            'summary': r'(?i)summary|profile|objective|about me|professional summary'
        }
        
        sections = {}
        
        # Split text into lines for processing
        lines = text.split('\n')
        
        current_section = 'other'
        sections[current_section] = []
        
        for line in lines:
            # Check if line is a section header
            is_header = False
            for section_name, pattern in section_patterns.items():
                if re.search(pattern, line, re.IGNORECASE) and len(line) < 100:  # Assume headers are relatively short
                    current_section = section_name
                    sections[current_section] = []
                    is_header = True
                    break
            
            if not is_header:
                sections[current_section].append(line)
        
        # Convert lists of lines back to text
        for section in sections:
            sections[section] = '\n'.join(sections[section]).strip()
        
        return sections
    
    def extract_tags_from_text(self, text: str) -> List[str]:
        """
        Extract potential tags/keywords from the resume text.
        This is a simple implementation that can be enhanced with NLP techniques.
        
        Args:
            text: Preprocessed text from resume
            
        Returns:
            List of extracted tags/keywords
        """
        # Common skills and keywords to look for
        # This is a simplified approach - in a real implementation, 
        # you would use a more comprehensive list or NLP techniques
        common_skills = [
            'python', 'java', 'javascript', 'c++', 'c#', 'ruby', 'php', 'swift',
            'html', 'css', 'sql', 'nosql', 'mongodb', 'mysql', 'postgresql',
            'react', 'angular', 'vue', 'node', 'django', 'flask', 'spring',
            'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'git',
            'agile', 'scrum', 'kanban', 'jira', 'confluence', 'project management',
            'machine learning', 'data science', 'artificial intelligence', 'nlp',
            'data analysis', 'data visualization', 'statistics', 'mathematics',
            'leadership', 'teamwork', 'communication', 'problem solving'
        ]
        
        found_tags = []
        
        # Convert text to lowercase for case-insensitive matching
        text_lower = text.lower()
        
        # Look for each skill in the text
        for skill in common_skills:
            if re.search(r'\b' + re.escape(skill) + r'\b', text_lower):
                found_tags.append(skill)
        
        return found_tags
    
    def process_resume(self, pdf_path: str) -> Tuple[str, Dict[str, str], List[str]]:
        """
        Process a resume PDF file and extract text, sections, and tags.
        
        Args:
            pdf_path: Path to the PDF resume file
            
        Returns:
            Tuple containing:
                - Full preprocessed text
                - Dictionary of identified sections
                - List of extracted tags/keywords
        """
        # Extract text from PDF
        raw_text = self.extract_text_from_pdf(pdf_path)
        
        # Preprocess the text
        processed_text = self.preprocess_text(raw_text)
        
        # Identify sections
        sections = self.identify_sections(processed_text)
        
        # Extract tags
        tags = self.extract_tags_from_text(processed_text)
        
        return processed_text, sections, tags


# Example usage
if __name__ == "__main__":
    processor = PDFProcessor()
    
    # Example: Process a resume
    # pdf_path = "path/to/resume.pdf"
    # text, sections, tags = processor.process_resume(pdf_path)
    # 
    # print(f"Extracted {len(tags)} tags: {tags}")
    # print("\nIdentified sections:")
    # for section_name, content in sections.items():
    #     if content:  # Only print non-empty sections
    #         print(f"\n--- {section_name.upper()} ---")
    #         print(content[:200] + "..." if len(content) > 200 else content)