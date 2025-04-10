"""
Test module for PDF Processor

This module provides testing functionality for the PDF Processor module.
It includes a sample PDF resume and tests the extraction, preprocessing,
and tag identification capabilities.
"""

import os
import sys
import tempfile
from typing import List, Dict

# Add the parent directory to the path so we can import the pdf_processor module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.pdf_processor import PDFProcessor


def create_sample_pdf(content: str) -> str:
    """
    Create a sample PDF file with the given content for testing.
    
    Args:
        content: Text content to include in the PDF
        
    Returns:
        Path to the created PDF file
    """
    try:
        # Try to import reportlab for PDF creation
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
        
        # Create a temporary file
        fd, path = tempfile.mkstemp(suffix='.pdf')
        os.close(fd)
        
        # Create the PDF
        c = canvas.Canvas(path, pagesize=letter)
        text_object = c.beginText(40, 750)
        text_object.setFont("Helvetica", 12)
        
        # Split content by newlines and add each line
        for line in content.split('\n'):
            text_object.textLine(line)
        
        c.drawText(text_object)
        c.save()
        
        return path
    except ImportError:
        print("ReportLab is not installed. Installing...")
        os.system("pip install reportlab")
        print("Please run the test again.")
        sys.exit(1)


def test_pdf_processor():
    """
    Test the PDF Processor functionality.
    """
    # Sample resume content
    sample_resume = """
JOHN DOE
Software Developer
john.doe@example.com | (123) 456-7890 | linkedin.com/in/johndoe

SUMMARY
Experienced software developer with 5 years of experience in Python and Flask development.
Skilled in building web applications and RESTful APIs.

EDUCATION
Bachelor of Science in Computer Science
University of Technology, 2015-2019

EXPERIENCE
Senior Software Developer
Tech Solutions Inc., 2021-Present
- Developed and maintained Flask-based web applications
- Implemented RESTful APIs for mobile applications
- Used SQLAlchemy for database operations
- Deployed applications using Docker and Kubernetes

Software Developer
WebDev Corp, 2019-2021
- Built responsive web applications using Python and JavaScript
- Worked with MongoDB and PostgreSQL databases
- Implemented CI/CD pipelines using Jenkins

SKILLS
Programming Languages: Python, JavaScript, SQL, HTML, CSS
Frameworks: Flask, Django, React, Angular
Databases: PostgreSQL, MongoDB, MySQL
Tools: Git, Docker, Kubernetes, Jenkins
Methodologies: Agile, Scrum, Test-Driven Development

PROJECTS
E-commerce Platform
- Built a full-stack e-commerce platform using Flask and React
- Implemented payment processing with Stripe API
- Deployed on AWS using Docker containers

Data Visualization Dashboard
- Created a dashboard for visualizing business metrics
- Used Python with Pandas for data processing
- Implemented interactive charts with D3.js
"""

    # Create a sample PDF
    pdf_path = create_sample_pdf(sample_resume)
    print(f"Created sample PDF at: {pdf_path}")
    
    # Initialize the PDF processor
    processor = PDFProcessor()
    
    # Process the resume
    try:
        text, sections, tags = processor.process_resume(pdf_path)
        
        # Print results
        print("\n=== EXTRACTED TEXT ===")
        print(text[:200] + "..." if len(text) > 200 else text)
        
        print("\n=== IDENTIFIED SECTIONS ===")
        for section_name, content in sections.items():
            if content:  # Only print non-empty sections
                print(f"\n--- {section_name.upper()} ---")
                print(content[:100] + "..." if len(content) > 100 else content)
        
        print("\n=== EXTRACTED TAGS ===")
        print(tags)
        
        # Cleanup
        os.remove(pdf_path)
        print(f"\nTest completed successfully. Removed temporary PDF file.")
        
        return True
    except Exception as e:
        print(f"Error during testing: {e}")
        # Cleanup
        if os.path.exists(pdf_path):
            os.remove(pdf_path)
        return False


if __name__ == "__main__":
    test_pdf_processor()
