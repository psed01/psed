# Helper functions and utilities
# Helper functions and utilities

import re
import hashlib
from datetime import datetime

def generate_email_hash(email_content):
    """Generate a unique hash for email content"""
    return hashlib.md5(email_content.encode('utf-8')).hexdigest()

def sanitize_text(text):
    """Sanitize text for processing"""
    if not text:
        return ""
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def format_timestamp():
    """Get current timestamp in readable format"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def validate_email_content(content):
    """Basic validation for email content"""
    if not content or len(content.strip()) < 10:
        return False, "Email content too short"
    
    if len(content) > 100000:  # 100KB limit
        return False, "Email content too large"
    
    return True, "Valid"