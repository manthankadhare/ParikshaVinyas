from flask import Blueprint, render_template, request, flash, redirect, url_for
from app import db
from app.models.audit import SystemSetting
from app.utils.decorators import admin_required
from app.services.audit_service import log_activity

settings_bp = Blueprint('settings', __name__)


@settings_bp.route('/', methods=['GET', 'POST'])
@admin_required
def index():
    if request.method == 'POST':
        college_name = request.form.get('college_name', '').strip()
        academic_year = request.form.get('academic_year', '').strip()
        allocation_strategy = request.form.get('default_allocation_strategy', 'Sequential')
        helpline = request.form.get('helpline', '').strip()

        _set_or_update('college_name', college_name, 'Institution Name displayed on examination admit cards and reports')
        _set_or_update('academic_year', academic_year, 'Current active academic year')
        _set_or_update('default_allocation_strategy', allocation_strategy, 'Default algorithm for auto seat allocation')
        _set_or_update('helpline', helpline, 'Examination support desk contact number')

        db.session.commit()
        log_activity('Update Settings', 'System Settings', 'Updated system preferences and college identity')
        flash('System settings updated successfully.', 'success')
        return redirect(url_for('settings.index'))

    settings_dict = {s.key: s.value for s in SystemSetting.query.all()}
    return render_template('settings/index.html', settings=settings_dict)


def _set_or_update(key, value, description):
    setting = SystemSetting.query.filter_by(key=key).first()
    if setting:
        setting.value = value
    else:
        setting = SystemSetting(key=key, value=value, description=description)
        db.session.add(setting)

