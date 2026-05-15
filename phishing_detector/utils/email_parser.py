# Email parsing utilities
# Email parsing utilities

import email
from email import policy
from email.parser import BytesParser

def parse_email_headers(raw_email):
    """Parse email headers only"""
    try:
        if isinstance(raw_email, bytes):
            msg = BytesParser(policy=policy.default).parsebytes(raw_email)
        else:
            msg = BytesParser(policy=policy.default).parsebytes(raw_email.encode('utf-8'))
        
        headers = {}
        for key, value in msg.items():
            headers[key.lower()] = value
        
        return headers
    except Exception as e:
        print(f"Error parsing headers: {e}")
        return {}

def extract_email_body(raw_email):
    """Extract only the email body"""
    try:
        if isinstance(raw_email, bytes):
            msg = BytesParser(policy=policy.default).parsebytes(raw_email)
        else:
            msg = BytesParser(policy=policy.default).parsebytes(raw_email.encode('utf-8'))
        
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                if content_type == 'text/plain':
                    body = part.get_content()
                    break
                elif content_type == 'text/html' and not body:
                    body = part.get_content()
        else:
            body = msg.get_content()
        
        return str(body) if body else ""
    except Exception as e:
        print(f"Error extracting body: {e}")
        return raw_email if isinstance(raw_email, str) else ""