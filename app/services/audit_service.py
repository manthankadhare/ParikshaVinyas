from flask import request
from flask_login import current_user
from app import db
from app.models.audit import ActivityLog


def log_activity(action, module, details=None):
    """Log an audit entry in the activity_logs table."""
    try:
        user_id = current_user.id if current_user and current_user.is_authenticated else None
        user_name = current_user.username if current_user and current_user.is_authenticated else 'System / Anonymous'
        ip_addr = request.remote_addr if request else '127.0.0.1'

        entry = ActivityLog(
            user_id=user_id,
            user_name=user_name,
            action=action,
            module=module,
            details=details,
            ip_address=ip_addr
        )
        db.session.add(entry)
        db.session.commit()
    except Exception as e:
        # Don't fail the primary transaction if audit logging fails
        db.session.rollback()

