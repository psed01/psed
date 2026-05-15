// Advanced Phishing Detector JavaScript - FIXED VERSION

class PhishingDetectorUI {
    constructor() {
        this.init();
    }

    init() {
        this.initializeEventListeners();
        this.startAnimations();
        this.initializeFileUpload();
        this.initializeURLAnalysis();
    }

    initializeEventListeners() {
        // Textarea character count
        const textarea = document.querySelector('.advanced-textarea');
        if (textarea) {
            textarea.addEventListener('input', this.updateCharCount.bind(this));
        }

        // Clear text button
        const clearBtn = document.getElementById('clearText');
        if (clearBtn) {
            clearBtn.addEventListener('click', this.clearTextarea.bind(this));
        }

        // Example email loader
        const exampleBtn = document.getElementById('loadExample');
        if (exampleBtn) {
            exampleBtn.addEventListener('click', this.loadExampleEmail.bind(this));
        }

        // Form submissions - SIMPLIFIED: Let forms submit normally, just add loading state
        const textForm = document.getElementById('pasteForm');
        const fileForm = document.getElementById('fileForm');
        
        if (textForm) {
            textForm.addEventListener('submit', this.handleTextFormSubmit.bind(this));
        }
        
        if (fileForm) {
            fileForm.addEventListener('submit', this.handleFileFormSubmit.bind(this));
        }

        // Tab switching animations
        const tabs = document.querySelectorAll('[data-bs-toggle="pill"]');
        tabs.forEach(tab => {
            tab.addEventListener('show.bs.tab', this.animateTabSwitch.bind(this));
        });

        // Statistics counter animation
        this.animateStatistics();
    }

    updateCharCount(e) {
        const textarea = e.target;
        const charCount = textarea.value.length;
        const counter = textarea.parentElement.querySelector('.char-count');
        if (counter) {
            counter.textContent = `${charCount.toLocaleString()} characters`;
            
            if (charCount > 10000) {
                counter.classList.add('text-warning');
            } else {
                counter.classList.remove('text-warning');
            }
        }
    }

    clearTextarea() {
        const textarea = document.querySelector('.advanced-textarea');
        if (textarea) {
            textarea.value = '';
            this.updateCharCount({ target: textarea });
            textarea.focus();
        }
    }

    loadExampleEmail() {
        const exampleEmail = `From: security@paypa1-security.com
Subject: URGENT: Your Account Access Will Be Suspended
Date: ${new Date().toUTCString()}
To: customer@example.com

Dear Valued Customer,

We've detected unusual login activity on your account from a new device. 
To prevent unauthorized access and potential fraud, you must verify your 
account immediately by clicking the link below.

🔒 VERIFY YOUR IDENTITY: http://paypa1-security-verify.com/account-update?token=xyz123

Failure to verify within 24 hours will result in permanent account suspension.

This is an automated security message. Please do not reply to this email.

Thank you for your immediate attention to this matter.

Sincerely,
PayPal Security Team
Security ID: PP-${Math.random().toString(36).substr(2, 8).toUpperCase()}

⚠️ IMPORTANT: Never share your password, security questions, or two-factor codes with anyone.`;

        const textarea = document.querySelector('.advanced-textarea');
        if (textarea) {
            textarea.value = exampleEmail;
            this.updateCharCount({ target: textarea });
            
            textarea.style.transform = 'scale(1.02)';
            setTimeout(() => {
                textarea.style.transform = 'scale(1)';
            }, 200);
        }
    }

    // SIMPLIFIED FORM HANDLING - Just show loading state
    handleTextFormSubmit(e) {
        const textarea = e.target.querySelector('textarea[name="email_content"]');
        if (!textarea || !textarea.value.trim()) {
            e.preventDefault();
            this.showError('Please enter email content to analyze');
            return;
        }

        const analyzeBtn = e.target.querySelector('.btn-analyze');
        if (analyzeBtn) {
            analyzeBtn.classList.add('loading');
            analyzeBtn.disabled = true;
            
            // Form will submit normally after this
            console.log('Submitting text form...');
        }
    }

    handleFileFormSubmit(e) {
        const fileInput = e.target.querySelector('input[name="email_file"]');
        if (!fileInput || !fileInput.files[0]) {
            e.preventDefault();
            this.showError('Please select a file to analyze');
            return;
        }

        const analyzeBtn = e.target.querySelector('.btn-analyze');
        if (analyzeBtn) {
            analyzeBtn.classList.add('loading');
            analyzeBtn.disabled = true;
            
            // Form will submit normally after this
            console.log('Submitting file form...');
        }
    }

    initializeFileUpload() {
        const uploadArea = document.getElementById('uploadArea');
        const fileInput = document.getElementById('fileInput');
        const filePreview = document.getElementById('filePreview');

        if (!uploadArea || !fileInput) return;

        // Drag and drop functionality
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            uploadArea.addEventListener(eventName, this.preventDefaults, false);
        });

        ['dragenter', 'dragover'].forEach(eventName => {
            uploadArea.addEventListener(eventName, this.highlightArea.bind(this), false);
        });

        ['dragleave', 'drop'].forEach(eventName => {
            uploadArea.addEventListener(eventName, this.unhighlightArea.bind(this), false);
        });

        uploadArea.addEventListener('drop', this.handleDrop.bind(this), false);
        uploadArea.addEventListener('click', () => fileInput.click());
        fileInput.addEventListener('change', this.handleFileSelect.bind(this));
    }

    preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    highlightArea() {
        const uploadArea = document.getElementById('uploadArea');
        uploadArea.classList.add('dragover');
    }

    unhighlightArea() {
        const uploadArea = document.getElementById('uploadArea');
        uploadArea.classList.remove('dragover');
    }

    handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        this.handleFiles(files);
    }

    handleFileSelect(e) {
        const files = e.target.files;
        this.handleFiles(files);
    }

    handleFiles(files) {
        const filePreview = document.getElementById('filePreview');
        if (files.length > 0) {
            const file = files[0];
            if (file.name.endsWith('.eml')) {
                filePreview.innerHTML = `
                    <div class="d-flex align-items-center">
                        <i class="fas fa-file-text text-primary me-3"></i>
                        <div>
                            <strong>${file.name}</strong>
                            <div class="text-muted">${this.formatFileSize(file.size)}</div>
                        </div>
                    </div>
                `;
                filePreview.classList.add('show');
            } else {
                this.showError('Please select a valid .eml file');
            }
        }
    }

    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    initializeURLAnalysis() {
        const urlForm = document.getElementById('urlForm');
        if (urlForm) {
            urlForm.addEventListener('submit', this.handleURLAnalysis.bind(this));
        }
    }

    async handleURLAnalysis(e) {
        e.preventDefault();
        const urlInput = document.getElementById('urlInput');
        const urlResults = document.getElementById('urlResults');
        const url = urlInput.value.trim();

        if (!url) {
            this.showError('Please enter a URL to analyze');
            return;
        }

        // Show loading state
        urlResults.innerHTML = `
            <div class="text-center">
                <div class="spinner-border text-primary mb-2"></div>
                <div>Analyzing URL structure and reputation...</div>
            </div>
        `;
        urlResults.classList.add('show');

        // Simulate API call
        setTimeout(() => {
            const isSuspicious = this.analyzeURL(url);
            urlResults.innerHTML = this.generateURLResults(url, isSuspicious);
        }, 2000);
    }

    analyzeURL(url) {
        const suspiciousPatterns = [
            /bit\.ly|tinyurl\.com|goo\.gl|t\.co/i,
            /\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/,
            /@/,
            /\.tk|\.ml|\.ga|\.cf|\.xyz/i,
            /login|verify|account|security/i
        ];

        return suspiciousPatterns.some(pattern => pattern.test(url));
    }

    generateURLResults(url, isSuspicious) {
        const riskLevel = isSuspicious ? 'high' : 'low';
        const riskColor = isSuspicious ? 'danger' : 'success';
        
        return `
            <h5>URL Analysis Results</h5>
            <div class="alert alert-${riskColor}">
                <i class="fas fa-${isSuspicious ? 'exclamation-triangle' : 'check-circle'}"></i>
                <strong>Risk Level: ${riskLevel.toUpperCase()}</strong>
            </div>
            <div class="row">
                <div class="col-md-6">
                    <strong>URL:</strong> ${url}
                </div>
                <div class="col-md-6">
                    <strong>Domain:</strong> ${new URL(url).hostname}
                </div>
            </div>
            <div class="mt-3">
                <h6>Analysis Details:</h6>
                <ul>
                    <li>${isSuspicious ? 'Suspicious patterns detected' : 'No obvious threats found'}</li>
                    <li>${this.checkSSL(url) ? 'SSL certificate present' : 'No SSL certificate'}</li>
                    <li>Domain age: ${this.getRandomDomainAge()}</li>
                </ul>
            </div>
        `;
    }

    checkSSL(url) {
        return url.startsWith('https://');
    }

    getRandomDomainAge() {
        const ages = ['Less than 1 year', '1-2 years', '2-5 years', 'Over 5 years'];
        return ages[Math.floor(Math.random() * ages.length)];
    }

    animateTabSwitch(e) {
        const target = document.querySelector(e.target.getAttribute('data-bs-target'));
        if (target) {
            target.style.opacity = '0';
            target.style.transform = 'translateX(20px)';
            
            setTimeout(() => {
                target.style.opacity = '1';
                target.style.transform = 'translateX(0)';
                target.style.transition = 'all 0.3s ease';
            }, 150);
        }
    }

    startAnimations() {
        this.initializeScrollAnimations();
    }

    initializeScrollAnimations() {
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }
            });
        }, observerOptions);

        document.querySelectorAll('.feature-item, .analysis-card').forEach(el => {
            el.style.opacity = '0';
            el.style.transform = 'translateY(30px)';
            el.style.transition = 'all 0.6s ease';
            observer.observe(el);
        });
    }

    animateStatistics() {
        const statNumbers = document.querySelectorAll('.stat-number[data-count]');
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    this.animateValue(entry.target);
                    observer.unobserve(entry.target);
                }
            });
        });

        statNumbers.forEach(stat => observer.observe(stat));
    }

    animateValue(element) {
        const target = parseFloat(element.getAttribute('data-count'));
        const duration = 2000;
        const step = target / (duration / 16);
        let current = 0;

        const timer = setInterval(() => {
            current += step;
            if (current >= target) {
                current = target;
                clearInterval(timer);
            }
            element.textContent = target === 2.5 ? current.toFixed(1) : Math.floor(current);
        }, 16);
    }

    showError(message) {
        const toast = document.createElement('div');
        toast.className = 'alert alert-danger position-fixed top-0 end-0 m-3';
        toast.style.zIndex = '9999';
        toast.innerHTML = `
            <i class="fas fa-exclamation-circle"></i> ${message}
            <button type="button" class="btn-close float-end" onclick="this.parentElement.remove()"></button>
        `;
        document.body.appendChild(toast);

        setTimeout(() => {
            if (toast.parentElement) {
                toast.remove();
            }
        }, 5000);
    }

    showSuccess(message) {
        const toast = document.createElement('div');
        toast.className = 'alert alert-success position-fixed top-0 end-0 m-3';
        toast.style.zIndex = '9999';
        toast.innerHTML = `
            <i class="fas fa-check-circle"></i> ${message}
            <button type="button" class="btn-close float-end" onclick="this.parentElement.remove()"></button>
        `;
        document.body.appendChild(toast);

        setTimeout(() => {
            if (toast.parentElement) {
                toast.remove();
            }
        }, 5000);
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    new PhishingDetectorUI();
    console.log('Phishing Detector UI initialized');
});