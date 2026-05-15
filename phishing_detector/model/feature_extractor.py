import re
import email
from email import policy
from email.parser import BytesParser
import urllib.parse
from urllib.parse import urlparse
import numpy as np

class EmailAnalyzer:
    def __init__(self):
        self.suspicious_keywords = [
            'verify your account', 'password', 'login', 'suspend', 'restrict',
            'urgent', 'immediately', 'click here', 'confirm your identity',
            'account verification', 'security alert', 'unauthorized access',
            'bank', 'paypal', 'amazon', 'microsoft', 'apple', 'netflix',
            'dear customer', 'valued member', 'prize', 'winner', 'free',
            'limited time', 'offer expires', 'act now', 'click below'
        ]
        
    def parse_email(self, email_content):
        """Parse email content and extract headers/body"""
        try:
            if isinstance(email_content, bytes):
                msg = BytesParser(policy=policy.default).parsebytes(email_content)
            else:
                msg = BytesParser(policy=policy.default).parsebytes(email_content.encode('utf-8'))
            
            headers = {}
            for key, value in msg.items():
                headers[key.lower()] = value
            
            # Extract body
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
            
            return headers, str(body) if body else ""
            
        except Exception as e:
            print(f"Error parsing email: {e}")
            # Return empty headers and use original content as body
            return {}, str(email_content) if not isinstance(email_content, bytes) else email_content.decode('utf-8', errors='ignore')

    def extract_header_features(self, headers):
        """Extract features from email headers"""
        features = {}
        
        # Sender analysis
        from_header = headers.get('from', '')
        features['sender'] = from_header
        
        # Check for suspicious sender patterns
        features['suspicious_sender'] = self.analyze_sender(from_header)
        
        # Subject analysis
        subject = headers.get('subject', '')
        features['subject'] = subject
        features['subject_urgency'] = self.check_urgency(subject)
        
        # Reply-to analysis
        reply_to = headers.get('reply-to', '')
        features['reply_to_mismatch'] = reply_to and reply_to != from_header
        
        return features

    def analyze_sender(self, sender):
        """Analyze sender for suspicious patterns"""
        if not sender:
            return True
        
        sender_lower = sender.lower()
        
        # Check for suspicious domains
        suspicious_domains = ['.tk', '.ml', '.ga', '.cf', '.xyz', '.top']
        if any(domain in sender_lower for domain in suspicious_domains):
            return True
        
        # Check for IP address in sender
        ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
        if re.search(ip_pattern, sender):
            return True
            
        return False

    def check_urgency(self, text):
        """Check for urgent language"""
        if not text:
            return False
            
        urgent_words = ['urgent', 'immediate', 'asap', 'important', 'alert', 'action required']
        text_lower = text.lower()
        return any(word in text_lower for word in urgent_words)

    def extract_content_features(self, body):
        """Extract features from email body content"""
        features = {}
        
        if not body:
            features['suspicious_keywords'] = []
            features['keyword_count'] = 0
            features['urls'] = []
            features['url_count'] = 0
            features['suspicious_urls'] = []
            features['body_length'] = 0
            features['has_html'] = False
            features['urgency_score'] = 0
            return features
        
        body_lower = body.lower()
        
        # Keyword analysis
        found_keywords = []
        for keyword in self.suspicious_keywords:
            if keyword in body_lower:
                found_keywords.append(keyword)
        
        features['suspicious_keywords'] = found_keywords
        features['keyword_count'] = len(found_keywords)
        
        # URL analysis
        urls = self.extract_urls(body)
        features['urls'] = urls
        features['url_count'] = len(urls)
        features['suspicious_urls'] = [url for url in urls if self.is_suspicious_url(url)]
        
        # Text characteristics
        features['body_length'] = len(body)
        features['has_html'] = '<html' in body_lower or '<body' in body_lower
        
        # Sentiment analysis (simple)
        features['urgency_score'] = self.calculate_urgency_score(body)
        
        return features

    def extract_urls(self, text):
        """Extract URLs from text"""
        if not text:
            return []
            
        url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
        return re.findall(url_pattern, text)

    def is_suspicious_url(self, url):
        """Check if URL is suspicious"""
        try:
            parsed = urlparse(url)
            
            # Check for IP address
            ip_pattern = r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'
            if re.match(ip_pattern, parsed.netloc):
                return True
            
            # Check for URL shortening services
            shorteners = ['bit.ly', 'tinyurl.com', 'goo.gl', 't.co', 'ow.ly']
            if any(shortener in parsed.netloc for shortener in shorteners):
                return True
            
            # Check for suspicious TLDs
            suspicious_tlds = ['.tk', '.ml', '.ga', '.cf', '.xyz']
            if any(parsed.netloc.endswith(tld) for tld in suspicious_tlds):
                return True
            
            # Check for @ symbol (redirect trick)
            if '@' in url:
                return True
                
            return False
            
        except Exception:
            return True

    def calculate_urgency_score(self, text):
        """Calculate urgency score based on threatening language"""
        if not text:
            return 0
            
        urgency_indicators = [
            'immediately', 'right away', 'as soon as possible', 'urgent',
            'action required', 'verify now', 'account suspension', 'limited time',
            'expire', 'last chance', 'final warning'
        ]
        
        text_lower = text.lower()
        score = sum(1 for indicator in urgency_indicators if indicator in text_lower)
        return min(score / 5.0, 1.0)  # Normalize to 0-1

    def extract_features(self, email_content):
        """Extract all features from email - CORRECTED METHOD NAME"""
        headers, body = self.parse_email(email_content)
        
        features = {}
        features.update(self.extract_header_features(headers))
        features.update(self.extract_content_features(body))
        
        # Calculate overall risk score
        features['risk_score'] = self.calculate_risk_score(features)
        
        return features

    def calculate_risk_score(self, features):
        """Calculate overall risk score"""
        risk_score = 0
        
        # Sender risk
        if features.get('suspicious_sender', False):
            risk_score += 0.3
        
        # Keyword risk
        keyword_count = features.get('keyword_count', 0)
        risk_score += min(keyword_count * 0.1, 0.3)
        
        # URL risk
        suspicious_urls = features.get('suspicious_urls', [])
        risk_score += min(len(suspicious_urls) * 0.2, 0.3)
        
        # Urgency risk
        urgency_score = features.get('urgency_score', 0)
        risk_score += urgency_score * 0.1
        
        return min(risk_score, 1.0)

    def is_phishing(self, features):
        """Determine if email is phishing based on features - CORRECTED METHOD NAME"""
        risk_score = features.get('risk_score', 0)
        return risk_score > 0.5

    # Alias methods for backward compatibility
    def extract_all_features(self, email_content):
        """Alias for extract_features for backward compatibility"""
        return self.extract_features(email_content)
    
    def is_suspicious_email(self, features):
        """Alias for is_phishing for backward compatibility"""
        return self.is_phishing(features)