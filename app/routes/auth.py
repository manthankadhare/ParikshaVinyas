from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime
from app import db
from app.models.user import User
from app.models.student import Student
from app.forms.auth_forms import LoginForm
from app.services.audit_service import log_activity

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/')
def index():
    if current_user.is_authenticated:
        if current_user.is_admin():
            return redirect(url_for('admin.dashboard'))
        elif current_user.is_invigilator():
            return redirect(url_for('invigilator.dashboard'))
        elif current_user.is_student():
            return redirect(url_for('student_portal.dashboard'))
    return redirect(url_for('auth.login'))


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('auth.index'))

    form = LoginForm()
    if form.validate_on_submit():
        login_input = form.username.data.strip()
        password = form.password.data

        # Check by username first
        user = User.query.filter_by(username=login_input).first()

        # If not found, check if it matches a student's enrollment number
        if not user:
            student = Student.query.filter_by(enrollment_no=login_input).first()
            if student and student.user:
                user = student.user

        if user and user.check_password(password):
            if not user.is_active:
                flash('Your account has been deactivated. Please contact the administrator.', 'danger')
                return render_template('auth/login.html', form=form)

            login_user(user, remember=form.remember.data)
            user.last_login = datetime.utcnow()
            db.session.commit()

            log_activity('User Login', 'Authentication', f"Successful login for user '{user.username}' ({user.role})")
            flash(f'Welcome back, {user.username}!', 'success')

            # Role-based redirection (Sanitized against CWE-601 Open Redirects)
            import urllib.parse
            next_page = request.args.get('next')
            if next_page:
                parsed_next = urllib.parse.urlsplit(next_page)
                if (
                    parsed_next.netloc == ''
                    and next_page.startswith('/')
                    and not next_page.startswith('//')
                    and not next_page.startswith('/auth')
                ):
                    return redirect(next_page)

            if user.is_admin():
                return redirect(url_for('admin.dashboard'))
            elif user.is_invigilator():
                return redirect(url_for('invigilator.dashboard'))
            else:
                return redirect(url_for('student_portal.dashboard'))
        else:
            flash('Invalid username/enrollment number or password.', 'danger')
            log_activity('Failed Login Attempt', 'Authentication', f"Failed attempt with identifier: {login_input}")

    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    uname = current_user.username
    log_activity('User Logout', 'Authentication', f"User '{uname}' logged out.")
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('auth.login'))

