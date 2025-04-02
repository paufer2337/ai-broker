import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, send_from_directory, jsonify, current_app
from werkzeug.utils import secure_filename
from forms.candidates import CandidateForm
from model.candidate import Candidate
from extensions import db

candidates_bp = Blueprint('candidates', __name__)

@candidates_bp.route('/', methods=['GET', 'POST'])
def candidate_index():
    form = CandidateForm()
    print("Form created")  # Debug print
    
    if request.method == 'POST':
        print("POST request received")  # Debug print
        print("Form data:", request.form)  # Debug print
        print("Files:", request.files)  # Debug print
    
    if form.validate_on_submit():
        print("Form validated successfully")  # Debug print
        
        # Save PDF file
        pdf_file = form.resume.data
        if pdf_file is None:
            print("No file was uploaded")  # Debug print
            flash('No file was uploaded', 'error')
            return redirect(url_for('candidates.candidate_index'))
            
        filename = secure_filename(pdf_file.filename)
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        print(f"Saving file to: {file_path}")  # Debug print
        
        try:
            pdf_file.save(file_path)
            print("File saved successfully")  # Debug print
            
            # Create candidate
            candidate = Candidate(
                name=form.name.data,
                email=form.email.data,
                location=form.location.data,
                core_skills=form.core_skills.data,
                experience_years=form.experience_years.data,
                resume_path=filename  # Store just the filename
            )
            db.session.add(candidate)
            db.session.commit()
            print("Candidate saved to database")  # Debug print
            
            flash('Candidate added successfully!', 'success')
        except Exception as e:
            print(f"Error occurred: {str(e)}")  # Debug print
            flash(f'Error saving candidate: {str(e)}', 'error')
        
        return redirect(url_for('candidates.candidate_index'))
    elif form.errors:
        print("Form validation errors:", form.errors)  # Debug print
    
    candidates = Candidate.query.all()
    print(f"Found {len(candidates)} candidates")  # Debug print
    return render_template('candidates/index.html', form=form, candidates=candidates)

@candidates_bp.route('/resume/<filename>')
def view_resume(filename):
    try:
        print(f"Attempting to serve PDF: {filename}")  # Debug print
        return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)
    except Exception as e:
        print(f"Error serving PDF: {str(e)}")  # Debug print
        return "PDF not found", 404

@candidates_bp.route('/delete/<int:candidate_id>', methods=['POST'])
def delete_candidate(candidate_id):
    try:
        candidate = Candidate.query.get_or_404(candidate_id)
        
        # Delete the PDF file if it exists
        if candidate.resume_path:
            pdf_path = os.path.join(current_app.config['UPLOAD_FOLDER'], candidate.resume_path)
            if os.path.exists(pdf_path):
                os.remove(pdf_path)
        
        # Delete from database
        db.session.delete(candidate)
        db.session.commit()
        
        flash('Candidate deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting candidate: {str(e)}', 'error')
    
    return redirect(url_for('candidates.candidate_index'))

@candidates_bp.route('/api/edit/<int:id>', methods=['POST'])
def edit_candidate(id):
    try:
        candidate = Candidate.query.get_or_404(id)
        data = request.json
        
        # Update candidate fields
        candidate.name = data.get('name', candidate.name)
        candidate.location = data.get('location', candidate.location)
        candidate.core_skills = data.get('core_skills', candidate.core_skills)
        candidate.experience_years = data.get('experience_years', candidate.experience_years)
        
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400