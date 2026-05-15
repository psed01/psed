# Phishing/Spam Email Detection Project
# Phishing/Spam Email Detection System

A Flask-based web application that uses Natural Language Processing (NLP) and Machine Learning to detect phishing and spam emails.

## Features

- **Real-time Email Analysis**: Analyze email content and headers for phishing indicators
- **Multiple Input Methods**: Paste email content or upload .eml files
- **Comprehensive Feature Extraction**: 
  - Header analysis (sender, subject, reply-to)
  - Content analysis (suspicious keywords, sentiment)
  - URL analysis (suspicious links, domain reputation)
- **Visual Results**: Clear classification with detailed breakdown
- **REST API**: JSON API for integration with other systems

## Installation

1. Clone or create the project structure
2. Install dependencies:
   ```bash
   pip install -r requirements.txt