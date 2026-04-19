# Resume Matching AI Agent

## Overview
This project implements an AI agent that matches broker missions with candidate resumes using tag-based semantic matching. The system extracts text from PDF resumes, identifies relevant tags, and uses a lightweight semantic matching algorithm to find the best candidates for each mission.

## Features
- PDF resume text extraction and preprocessing
- Automatic tag/keyword identification from resumes
- Semantic matching between mission tags and resume content
- Integration with Flask web applications
- Real-time matching capabilities

## Project Structure
```
ai-broker/
├── src/
│   ├── __init__.py
│   ├── pdf_processor.py      # PDF text extraction and processing
│   ├── matching_engine.py    # Semantic matching algorithm
│   └── integration.py        # Flask integration code
├── tests/
│   ├── __init__.py
│   ├── test_pdf_processor.py # Tests for PDF processing
│   └── test_matching_engine.py # Tests for matching algorithm
└── README.md                 # This file
```

## Installation
- See requirements.txt

### Prerequisites
- Python 3.6+
- Flask (for web integration)
- PDFMiner.six (for PDF processing)
- NLTK (for text processing)

### Setup
1. Clone this repository to your project
2. Install the required dependencies:
```bash
pip install pdfminer.six nltk flask
```
3. Download required NLTK resources:
```python
import nltk
nltk.download('stopwords')
nltk.download('wordnet')
```

## Usage

### PDF Processing
The `PDFProcessor` class extracts text from PDF resumes and identifies relevant sections and tags:

```python
from src.pdf_processor import PDFProcessor

# Initialize the processor
processor = PDFProcessor()

# Process a resume
pdf_path = "path/to/resume.pdf"
text, sections, tags = processor.process_resume(pdf_path)

# Print extracted information
print(f"Extracted {len(tags)} tags: {tags}")
print("\nIdentified sections:")
for section_name, content in sections.items():
    if content:  # Only print non-empty sections
        print(f"\n--- {section_name.upper()} ---")
        print(content[:200] + "..." if len(content) > 200 else content)
```

### Matching Engine
The `MatchingEngine` class matches mission tags with candidate resumes:

```python
from src.matching_engine import MatchingEngine

# Initialize the matching engine
engine = MatchingEngine()

# Example resumes
resumes = {
    "candidate1": "Experienced software developer with 5 years of Python and Flask development...",
    "candidate2": "Frontend developer with expertise in React, Angular, and Vue...",
    # Add more candidates...
}

# Mission tags
mission_tags = ["Python", "Flask", "Web Development"]

# Get top matches
top_matches = engine.get_top_matches(resumes, mission_tags, top_k=3)

# Print results
print(f"Top matches for mission tags: {mission_tags}")
for candidate_id, score in top_matches:
    print(f"{candidate_id}: {score:.4f} - {resumes[candidate_id][:50]}...")
```

### Integration with Flask
The `integration.py` module provides code to integrate the matching functionality with a Flask application:

```python
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from src.integration import create_resume_matching_agent, integrate_with_flask_app

# Create Flask app
app = Flask(__name__)

# Initialize database (replace with your actual database setup)
# db = SQLAlchemy(app)

# Create resume matching agent
resume_upload_dir = "path/to/resume/uploads"
agent = create_resume_matching_agent(resume_upload_dir)

# Integrate with Flask app
integrate_with_flask_app(app, db, agent)

if __name__ == "__main__":
    app.run(debug=True)
```

## Integration with Your Existing Project

To integrate this matching system with your existing Flask application:

1. Copy the `src` directory to your project
2. Modify the `integrate_with_flask_app` function in `integration.py` to work with your specific database models
3. Update the example routes to match your application's URL structure
4. Ensure your database models include fields for storing resume text and tags

### Database Schema Recommendations

For optimal integration, your database should include:

**Candidates Table:**
- `id`: Unique identifier
- `name`: Candidate name
- `resume_path`: Path to the uploaded PDF file
- `resume_text`: Extracted text from the resume
- `tags`: Comma-separated list of extracted tags

**Missions Table:**
- `id`: Unique identifier
- `title`: Mission title
- `description`: Mission description
- `tags`: Comma-separated list of mission tags
- `broker_id`: Reference to the broker who created the mission

**Matches Table:**
- `id`: Unique identifier
- `mission_id`: Reference to the mission
- `candidate_id`: Reference to the candidate
- `score`: Matching score
- `created_at`: Timestamp of when the match was created

## Performance Considerations

- **Pre-compute Embeddings**: For better performance, consider pre-computing and storing the processed resume text and tags when resumes are uploaded
- **Batch Processing**: If you have many resumes, process them in batches
- **Caching**: Cache matching results for missions that don't change frequently

## Extending the System

### Improving Tag Extraction
The current implementation uses a simple approach for tag extraction. To improve it:

1. Use a more comprehensive list of skills and keywords
2. Implement NER (Named Entity Recognition) to identify skills and technologies
3. Use a domain-specific ontology for technical skills

### Enhancing Matching Algorithm
The current matching algorithm uses TF-IDF and cosine similarity. For better results:

1. If disk space allows, use sentence-transformers for more advanced semantic matching
2. Implement a hybrid approach combining exact matching and semantic similarity
3. Add weights to different resume sections (e.g., skills section might be more important than summary)

## Troubleshooting

### PDF Extraction Issues
- If text extraction fails, ensure the PDF is not scanned or image-based
- For complex PDF layouts, try adjusting the LAParams in the PDFProcessor initialization

### Matching Quality Issues
- If matches seem incorrect, try expanding the tag list with more domain-specific terms
- Adjust the preprocessing steps to include or exclude certain types of words
- Consider adding a custom scoring function that gives higher weight to exact matches

## License
This project is provided as-is for your use. You are free to modify and adapt it to your specific needs.

## Contact
For any questions or issues, please contact your project maintainer.




## Definiera taggar på både engelska och svenska
cybersecurity_tags = {
    "Cybersecurity Consulting": "Cybersäkerhetskonsulttjänster",
    "Risk Management": "Riskhantering",
    "GDPR Compliance": "GDPR-efterlevnad",
    "Data Protection": "Dataskydd",
    "Privacy & Integrity": "Integritet & Sekretess",
    "Secure Digital Transformation": "Säker Digital Transformation",
    "Sustainable Digitalization": "Hållbar Digitalisering",
    "Compliance & Audits": "Efterlevnad & Revisioner",
    "Product Security": "Produktäkerhet",
    "Secure Product Development": "Säker Produktutveckling",
    "Information Security": "Informationssäkerhet",
    "Risk Mitigation Strategies": "Riskreduceringsstrategier",
    "Digital Risk Management": "Digital Riskhantering",
    "Proactive Defense Strategies": "Proaktiva Försvarsstategier",
    "National Security Consulting": "Nationell Säkerhetsrådgivning",
    "Internal Investigations": "Interna Undersökningar",
    "External Research": "Extern Forskning",
    "Security Expertise": "Säkerhetsexpertis",
    "Digital Resilience": "Digital Resiliens",
    "Regulatory Compliance": "Regulatorisk Efterlevnad",
    "Security Audits": "Säkerhetsrevisioner",
    "Privacy Laws": "Sekretesslagar",
    "Technology Governance": "Teknologiskt Styre",
    "Ethical Practices": "Etiska Praktiker",
    "Security Training": "Säkerhetsträning",
    "Corporate Security Solutions": "Företagssäkerhetslösningar",
    "Risk Assessment": "Riskbedömning",
    "Digital Innovation": "Digital Innovation",
    "Secure Infrastructure": "Säker Infrastruktur"
}

# Kombinera alla taggar (både engelska och svenska)
all_tags = list(cybersecurity_tags.keys()) + list(cybersecurity_tags.values())

# Uppdatera alla uppdrag med både engelska och svenska taggar
for mission in Mission.query.all():
    mission.required_skills_tags = ", ".join(all_tags)
    mission.required_skills = ", ".join(all_tags)  # Uppdatera även required_skills för konsistens

# Spara ändringar
db.session.commit()
print("Uppdaterade alla uppdrag med både engelska och svenska cybersäkerhetstaggarna")

# Check a mission's tags
mission = Mission.query.first()
print("Mission tags:", mission.required_skills_tags)
print("Mission skills:", mission.required_skills)