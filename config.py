import os
from datetime import timedelta

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'parikshavinyas-super-secure-stqa-key-2026')
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL', 
        f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'parikshavinyas.db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Session Configuration
    PERMANENT_SESSION_LIFETIME = timedelta(hours=4)
    SESSION_COOKIE_SECURE = False  # Set True in production HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Application Info
    APP_NAME = "ParikshaVinyas"
    APP_TAGLINE = "Plan Smart. Allocate Fairly. Examine Seamlessly."
    COLLEGE_NAME = os.environ.get('COLLEGE_NAME', 'UPL University of Sustainable Technology')
    ACADEMIC_YEAR = os.environ.get('ACADEMIC_YEAR', '2025-2026')
    
    # Uploads
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max limit
    ALLOWED_EXTENSIONS = {'csv', 'png', 'jpg', 'jpeg', 'pdf'}
    
    # AI Testing Config (Optional API key for STQA Workspace)
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '')


class TestConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SERVER_NAME = 'localhost.localdomain'

