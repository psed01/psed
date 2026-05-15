# create_folder_structure.py
import os
import sys

def create_folder_structure():
    base_dir = "phishing_detector"
    
    # Define the folder structure
    folders = [
        f"{base_dir}",
        f"{base_dir}/model",
        f"{base_dir}/static",
        f"{base_dir}/static/css",
        f"{base_dir}/static/js", 
        f"{base_dir}/static/images",
        f"{base_dir}/templates",
        f"{base_dir}/data",  # For training data if needed
        f"{base_dir}/utils",  # For helper functions
    ]
    
    # Define files to create
    files = {
        f"{base_dir}/app.py": "# Main Flask application file\n",
        f"{base_dir}/requirements.txt": "# Project dependencies\n",
        f"{base_dir}/README.md": "# Phishing/Spam Email Detection Project\n",
        f"{base_dir}/.gitignore": "# Python gitignore\n__pycache__/\n*.pyc\n*.pyo\n.env\n",
        
        f"{base_dir}/model/__init__.py": "",
        f"{base_dir}/model/trained_model.pkl": "# Placeholder for your trained model\n",
        f"{base_dir}/model/vectorizer.pkl": "# Placeholder for your vectorizer\n",
        f"{base_dir}/model/feature_extractor.py": "# Custom module for parsing emails and feature engineering\n",
        f"{base_dir}/model/model_trainer.py": "# Script for training your ML model\n",
        
        f"{base_dir}/static/css/style.css": "/* CSS styles for the web application */\n",
        f"{base_dir}/static/js/script.js": "// JavaScript for frontend interactions\n",
        f"{base_dir}/static/images/placeholder.txt": "# Add your images here\n",
        
        f"{base_dir}/templates/base.html": "<!DOCTYPE html>\n<!-- Base template -->\n",
        f"{base_dir}/templates/index.html": "<!-- Home Page Template -->\n",
        f"{base_dir}/templates/results.html": "<!-- Results Page Template -->\n",
        f"{base_dir}/templates/about.html": "<!-- About Page Template -->\n",
        
        f"{base_dir}/data/__init__.py": "",
        f"{base_dir}/data/placeholder.txt": "# Add your training datasets here\n",
        
        f"{base_dir}/utils/__init__.py": "",
        f"{base_dir}/utils/helpers.py": "# Helper functions and utilities\n",
        f"{base_dir}/utils/email_parser.py": "# Email parsing utilities\n",
    }
    
    print("Creating Phishing Detection Project Structure...")
    
    # Create folders
    for folder in folders:
        try:
            os.makedirs(folder, exist_ok=True)
            print(f"✓ Created folder: {folder}")
        except Exception as e:
            print(f"✗ Error creating {folder}: {e}")
    
    # Create files
    for file_path, content in files.items():
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ Created file: {file_path}")
        except Exception as e:
            print(f"✗ Error creating {file_path}: {e}")
    
    print(f"\n✅ Project structure created successfully!")
    print(f"📁 Location: {os.path.abspath(base_dir)}")
    print(f"\nNext steps:")
    print(f"1. cd {base_dir}")
    print(f"2. pip install -r requirements.txt")
    print(f"3. Start building your Flask application!")

if __name__ == "__main__":
    create_folder_structure()