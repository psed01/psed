from flask import Flask, render_template, request, session, redirect, url_for, jsonify
import joblib
import numpy as np
import os
from model.feature_extractor import EmailAnalyzer

app = Flask(__name__)
app.secret_key = 'your_secret_key_here_change_in_production'

# Add custom template filters
@app.template_filter('yesno')
def yesno_filter(value, yesno_str='Yes,No'):
    """Custom filter to mimic Django's yesno filter"""
    yes, no = yesno_str.split(',')
    return yes if value else no

# Global variables for model and vectorizer
model = None
vectorizer = None
email_analyzer = None

def load_models():
    """Load ML model and vectorizer"""
    global model, vectorizer, email_analyzer
    try:
        # Initialize the feature extractor
        email_analyzer = EmailAnalyzer()
        
        # For now, we'll use a dummy model - you'll replace this with your trained model
        print("⚠️  Using dummy model. Train your model and update model/trained_model.pkl")
        
        # Placeholder - you'll load your actual model here
        # model = joblib.load('model/trained_model.pkl')
        # vectorizer = joblib.load('model/vectorizer.pkl')
        
    except Exception as e:
        print(f"Error loading models: {e}")

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    """Analyze email content"""
    try:
        print("Analysis endpoint hit")  # Debug log
        
        # Get email content from form
        email_content = ""
        analysis_type = "text"
        
        # Check if it's a file upload
        if 'email_file' in request.files and request.files['email_file'].filename:
            file = request.files['email_file']
            if file.filename.endswith('.eml'):
                email_content = file.read().decode('utf-8', errors='ignore')
                analysis_type = "file"
                print(f"File uploaded: {file.filename}")  # Debug log
            else:
                return render_template('index.html', error="Please upload a valid .eml file")
        
        # Check if it's text content
        elif 'email_content' in request.form and request.form['email_content'].strip():
            email_content = request.form['email_content']
            analysis_type = "text"
            print(f"Text content received: {len(email_content)} characters")  # Debug log
        
        else:
            return render_template('index.html', error="Please provide email content or upload a file")
        
        if not email_content.strip():
            return render_template('index.html', error="Email content cannot be empty")
        
        print("Extracting features...")  # Debug log
        
        # Extract features using the correct method name
        features = email_analyzer.extract_features(email_content)
        print(f"Features extracted: {len(features)}")  # Debug log
        
        # For demonstration - you'll replace this with actual model prediction
        # Use the correct method name for checking suspicious emails
        if email_analyzer.is_phishing(features):
            prediction = "Phishing"
            confidence = 87.5
            risk_level = "high"
        else:
            prediction = "Legitimate"
            confidence = 92.3
            risk_level = "low"
        
        # Prepare result data - ensure all features are serializable
        result_data = {
            'classification': prediction,
            'confidence': confidence,
            'risk_level': risk_level,
            'features': {
                'sender': features.get('sender', ''),
                'suspicious_sender': features.get('suspicious_sender', False),
                'subject': features.get('subject', ''),
                'subject_urgency': features.get('subject_urgency', False),
                'suspicious_keywords': features.get('suspicious_keywords', []),
                'keyword_count': features.get('keyword_count', 0),
                'urls': features.get('urls', []),
                'url_count': features.get('url_count', 0),
                'suspicious_urls': features.get('suspicious_urls', []),
                'body_length': features.get('body_length', 0),
                'has_html': features.get('has_html', False),
                'urgency_score': features.get('urgency_score', 0),
                'risk_score': features.get('risk_score', 0)
            },
            'email_preview': email_content[:200] + "..." if len(email_content) > 200 else email_content,
            'analysis_type': analysis_type
        }
        
        session['result'] = result_data
        print(f"Redirecting to results with prediction: {prediction}")  # Debug log
        return redirect(url_for('results'))
        
    except Exception as e:
        print(f"Analysis error: {str(e)}")  # Debug log
        import traceback
        traceback.print_exc()
        return render_template('index.html', error=f"Analysis error: {str(e)}")

@app.route('/results')
def results():
    """Display analysis results"""
    result_data = session.get('result')
    if not result_data:
        return redirect(url_for('index'))
    
    # Ensure all data is properly formatted for the template
    if 'features' not in result_data:
        result_data['features'] = {}
    
    return render_template('results.html', result=result_data)

@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')

@app.route('/api/analyze', methods=['POST'])
def api_analyze():
    """API endpoint for email analysis"""
    try:
        data = request.get_json()
        email_content = data.get('email_content', '')
        
        if not email_content.strip():
            return jsonify({'error': 'Email content is required'}), 400
        
        features = email_analyzer.extract_features(email_content)
        
        # Demo prediction
        is_phishing = email_analyzer.is_phishing(features)
        
        return jsonify({
            'classification': 'Phishing' if is_phishing else 'Legitimate',
            'confidence': 85.2 if is_phishing else 90.1,
            'features': {
                'suspicious_keywords': features.get('suspicious_keywords', []),
                'url_count': features.get('url_count', 0),
                'suspicious_sender': features.get('suspicious_sender', False)
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('index.html', error="Page not found"), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('index.html', error="Internal server error"), 500

if __name__ == '__main__':
    load_models()
    app.run(debug=True, port=5000)