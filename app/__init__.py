import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate

from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()
migrate = Migrate()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Ensure required directories exist
    try:
        if not os.environ.get('VERCEL'):
            os.makedirs(os.path.join(app.root_path, '..', 'instance'), exist_ok=True)
        os.makedirs(app.config.get('UPLOAD_FOLDER', 'uploads'), exist_ok=True)
    except OSError:
        pass

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app, db)

    # Login Manager settings
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'warning'

    from app.models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    # Register Blueprints
    from app.routes.auth import auth_bp
    from app.routes.admin import admin_bp
    from app.routes.student import student_bp
    from app.routes.academic import academic_bp
    from app.routes.hall import hall_bp
    from app.routes.exam import exam_bp
    from app.routes.allocation import allocation_bp
    from app.routes.reports import reports_bp
    from app.routes.invigilator import invigilator_bp
    from app.routes.student_portal import student_portal_bp
    from app.routes.qa import qa_bp
    from app.routes.settings import settings_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(student_bp, url_prefix='/admin/students')
    app.register_blueprint(academic_bp, url_prefix='/admin/academic')
    app.register_blueprint(hall_bp, url_prefix='/admin/halls')
    app.register_blueprint(exam_bp, url_prefix='/admin/exams')
    app.register_blueprint(allocation_bp, url_prefix='/admin/allocation')
    app.register_blueprint(reports_bp, url_prefix='/admin/reports')
    app.register_blueprint(invigilator_bp, url_prefix='/invigilator')
    app.register_blueprint(student_portal_bp, url_prefix='/student')
    app.register_blueprint(qa_bp, url_prefix='/admin/qa')
    app.register_blueprint(settings_bp, url_prefix='/admin/settings')

    # Context processors for navigation and global settings
    @app.context_processor
    def inject_global_vars():
        from app.models.audit import SystemSetting
        college_setting = SystemSetting.query.filter_by(key='college_name').first()
        academic_year = SystemSetting.query.filter_by(key='academic_year').first()
        return {
            'APP_NAME': app.config.get('APP_NAME', 'ParikshaVinyas'),
            'APP_TAGLINE': app.config.get('APP_TAGLINE', 'Plan Smart. Allocate Fairly. Examine Seamlessly.'),
            'COLLEGE_NAME': college_setting.value if college_setting else app.config.get('COLLEGE_NAME'),
            'ACADEMIC_YEAR': academic_year.value if academic_year else app.config.get('ACADEMIC_YEAR')
        }

    # Defense-in-depth HTTP security headers
    @app.after_request
    def set_security_headers(response):
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        return response

    # Auto-seed database when running in Vercel serverless environment
    if os.environ.get('VERCEL'):
        try:
            with app.app_context():
                db.create_all()
                from app.models.user import User
                if User.query.count() == 0:
                    from scripts.seed_database import seed
                    seed(app=app)
        except Exception as e:
            app.logger.warning(f"Vercel auto-seed: {e}")

    return app

