import json
from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from app import db
from app.models.qa import TestCase, DefectReport
from app.forms.qa_forms import TestCaseForm, DefectReportForm, AIGeneratorForm
from app.services.ai_qa_service import AIQAService
from app.utils.decorators import admin_required
from app.services.audit_service import log_activity

qa_bp = Blueprint('qa', __name__)


@qa_bp.route('/')
@admin_required
def index():
    # STQA Testing Hub Dashboard
    total_cases = TestCase.query.count()
    passed_cases = TestCase.query.filter_by(status='Pass').count()
    failed_cases = TestCase.query.filter_by(status='Fail').count()
    blocked_cases = TestCase.query.filter_by(status='Blocked').count()
    unexecuted_cases = TestCase.query.filter_by(status='Not Executed').count()

    total_executed = passed_cases + failed_cases + blocked_cases
    pass_rate = round((passed_cases / total_executed * 100), 1) if total_executed > 0 else 0

    # Defects count
    total_defects = DefectReport.query.count()
    open_defects = DefectReport.query.filter(DefectReport.status.in_(['New', 'Open', 'In Progress'])).count()
    critical_defects = DefectReport.query.filter_by(severity='Critical').count()

    recent_cases = TestCase.query.order_by(TestCase.id.desc()).limit(8).all()
    recent_defects = DefectReport.query.order_by(DefectReport.id.desc()).limit(6).all()

    return render_template(
        'qa/index.html',
        total_cases=total_cases,
        passed_cases=passed_cases,
        failed_cases=failed_cases,
        blocked_cases=blocked_cases,
        unexecuted_cases=unexecuted_cases,
        pass_rate=pass_rate,
        total_defects=total_defects,
        open_defects=open_defects,
        critical_defects=critical_defects,
        recent_cases=recent_cases,
        recent_defects=recent_defects
    )


@qa_bp.route('/test-cases')
@admin_required
def test_cases():
    module_filter = request.args.get('module', '')
    status_filter = request.args.get('status', '')
    type_filter = request.args.get('type', '')
    page = request.args.get('page', 1, type=int)

    query = TestCase.query
    if module_filter:
        query = query.filter_by(module=module_filter)
    if status_filter:
        query = query.filter_by(status=status_filter)
    if type_filter:
        query = query.filter_by(test_type=type_filter)

    cases = query.order_by(TestCase.id).paginate(page=page, per_page=15, error_out=False)
    modules = [m[0] for m in db.session.query(TestCase.module).distinct().all()]

    return render_template(
        'qa/test_cases.html',
        cases=cases,
        modules=modules,
        module_filter=module_filter,
        status_filter=status_filter,
        type_filter=type_filter
    )


@qa_bp.route('/test-cases/add', methods=['GET', 'POST'])
@admin_required
def add_test_case():
    form = TestCaseForm()
    if form.validate_on_submit():
        code = form.case_code.data.strip().upper()
        if TestCase.query.filter_by(case_code=code).first():
            flash(f"Test Case ID '{code}' already exists.", 'danger')
            return render_template('qa/test_case_form.html', form=form, title='Add Test Case')

        tc = TestCase(
            case_code=code,
            module=form.module.data,
            scenario=form.scenario.data.strip(),
            preconditions=form.preconditions.data,
            test_input=form.test_input.data,
            expected_result=form.expected_result.data,
            actual_result=form.actual_result.data,
            test_technique=form.test_technique.data,
            test_type=form.test_type.data,
            status=form.status.data,
            tester_name=form.tester_name.data.strip(),
            execution_date=datetime.utcnow() if form.status.data != 'Not Executed' else None
        )
        db.session.add(tc)
        db.session.commit()
        log_activity('Add Test Case', 'STQA Hub', f"Registered test case {tc.case_code}")
        flash(f"Test Case '{tc.case_code}' added successfully.", 'success')
        return redirect(url_for('qa.test_cases'))

    return render_template('qa/test_case_form.html', form=form, title='Add Test Case')


@qa_bp.route('/test-cases/<int:case_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_test_case(case_id):
    tc = TestCase.query.get_or_404(case_id)
    form = TestCaseForm(obj=tc)

    if form.validate_on_submit():
        code = form.case_code.data.strip().upper()
        dup = TestCase.query.filter(TestCase.case_code == code, TestCase.id != tc.id).first()
        if dup:
            flash(f"Test Case ID '{code}' is already used.", 'danger')
            return render_template('qa/test_case_form.html', form=form, title='Edit Test Case', tc=tc)

        tc.case_code = code
        tc.module = form.module.data
        tc.scenario = form.scenario.data.strip()
        tc.preconditions = form.preconditions.data
        tc.test_input = form.test_input.data
        tc.expected_result = form.expected_result.data
        tc.actual_result = form.actual_result.data
        tc.test_technique = form.test_technique.data
        tc.test_type = form.test_type.data

        old_status = tc.status
        tc.status = form.status.data
        tc.tester_name = form.tester_name.data.strip()
        if form.status.data != old_status and form.status.data != 'Not Executed':
            tc.execution_date = datetime.utcnow()

        db.session.commit()
        log_activity('Update Test Case', 'STQA Hub', f"Updated test case {tc.case_code} to status {tc.status}")
        flash(f"Test case '{tc.case_code}' updated successfully.", 'success')
        return redirect(url_for('qa.test_cases'))

    return render_template('qa/test_case_form.html', form=form, title='Edit Test Case', tc=tc)


@qa_bp.route('/test-cases/<int:case_id>/update-status', methods=['POST'])
@admin_required
def quick_status_update(case_id):
    tc = TestCase.query.get_or_404(case_id)
    status = request.form.get('status')
    actual = request.form.get('actual_result', '')

    if status in ['Pass', 'Fail', 'Blocked', 'Not Executed']:
        tc.status = status
        tc.actual_result = actual
        tc.execution_date = datetime.utcnow()
        db.session.commit()
        flash(f"Test case {tc.case_code} marked as {status}.", 'success')

    return redirect(request.referrer or url_for('qa.test_cases'))


@qa_bp.route('/defects')
@admin_required
def defects():
    status_filter = request.args.get('status', '')
    severity_filter = request.args.get('severity', '')

    query = DefectReport.query
    if status_filter:
        query = query.filter_by(status=status_filter)
    if severity_filter:
        query = query.filter_by(severity=severity_filter)

    all_defects = query.order_by(DefectReport.created_date.desc()).all()
    return render_template('qa/defects.html', defects=all_defects, status_filter=status_filter, severity_filter=severity_filter)


@qa_bp.route('/defects/add', methods=['GET', 'POST'])
@admin_required
def add_defect():
    form = DefectReportForm()
    test_cases_list = TestCase.query.order_by(TestCase.case_code).all()
    form.test_case_id.choices = [(0, '-- None / Ad-hoc Defect --')] + [(t.id, f"{t.case_code}: {t.scenario[:50]}") for t in test_cases_list]

    # Pre-populate if case_id passed
    pre_case_id = request.args.get('case_id', type=int)
    if pre_case_id and request.method == 'GET':
        tc = TestCase.query.get(pre_case_id)
        if tc:
            form.test_case_id.data = tc.id
            form.title.data = f"Defect in {tc.case_code}: {tc.scenario}"
            form.expected_result.data = tc.expected_result
            form.actual_result.data = tc.actual_result or ''

    if form.validate_on_submit():
        code = form.bug_code.data.strip().upper()
        if DefectReport.query.filter_by(bug_code=code).first():
            flash(f"Bug ID '{code}' already exists.", 'danger')
            return render_template('qa/defect_form.html', form=form, title='Log Defect')

        tc_id = form.test_case_id.data if form.test_case_id.data != 0 else None

        defect = DefectReport(
            bug_code=code,
            test_case_id=tc_id,
            title=form.title.data.strip(),
            description=form.description.data,
            steps_to_reproduce=form.steps_to_reproduce.data,
            expected_result=form.expected_result.data,
            actual_result=form.actual_result.data,
            severity=form.severity.data,
            priority=form.priority.data,
            status=form.status.data,
            assigned_to=form.assigned_to.data.strip()
        )
        db.session.add(defect)
        db.session.commit()
        log_activity('Log Defect', 'STQA Hub', f"Logged defect {defect.bug_code} ({defect.severity})")
        flash(f"Defect '{defect.bug_code}' registered successfully.", 'warning')
        return redirect(url_for('qa.defects'))

    return render_template('qa/defect_form.html', form=form, title='Log Defect')


@qa_bp.route('/defects/<int:defect_id>/resolve', methods=['POST'])
@admin_required
def resolve_defect(defect_id):
    defect = DefectReport.query.get_or_404(defect_id)
    defect.status = 'Resolved'
    defect.resolved_date = datetime.utcnow()
    db.session.commit()
    log_activity('Resolve Defect', 'STQA Hub', f"Marked defect {defect.bug_code} as Resolved")
    flash(f"Defect '{defect.bug_code}' marked as Resolved.", 'success')
    return redirect(url_for('qa.defects'))


@qa_bp.route('/ai-workspace', methods=['GET', 'POST'])
@admin_required
def ai_workspace():
    form = AIGeneratorForm()
    generated_cases = None
    defect_analysis = None

    if request.method == 'POST' and form.validate_on_submit():
        mod = form.module_name.data
        req_text = form.requirement_text.data
        t_type = form.test_type.data

        generated_cases = AIQAService.generate_test_scenarios(mod, req_text, t_type)
        flash(f"AI Engine generated {len(generated_cases)} test scenarios for '{mod}'.", 'info')

    # Analyze defect action
    if request.args.get('action') == 'analyze_defect':
        bug_id = request.args.get('bug_id', type=int)
        if bug_id:
            bug = DefectReport.query.get(bug_id)
            if bug:
                defect_analysis = AIQAService.analyze_defect(
                    bug.title, bug.steps_to_reproduce, bug.actual_result, bug.expected_result
                )

    return render_template(
        'qa/ai_workspace.html',
        form=form,
        generated_cases=generated_cases,
        defect_analysis=defect_analysis
    )


@qa_bp.route('/ai-workspace/import-case', methods=['POST'])
@admin_required
def import_ai_case():
    """Allows 1-click import of an AI-generated test scenario into persistent TestCase table."""
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'message': 'No data provided'}), 400

    code = data.get('case_code', '').strip().upper()
    # Ensure unique code
    base_code = code
    counter = 1
    while TestCase.query.filter_by(case_code=code).first():
        code = f"{base_code}_{counter}"
        counter += 1

    tc = TestCase(
        case_code=code,
        module=data.get('module', 'Allocation Engine'),
        scenario=data.get('scenario', ''),
        preconditions=data.get('preconditions', ''),
        test_input=data.get('test_input', ''),
        expected_result=data.get('expected_result', ''),
        test_technique=data.get('test_technique', 'Equivalence Partitioning (EP)'),
        test_type=data.get('test_type', 'Positive'),
        status='Not Executed',
        tester_name='AI Test Synthesizer'
    )
    db.session.add(tc)
    db.session.commit()
    log_activity('Import AI Test Case', 'STQA Hub', f"Imported test case {tc.case_code}")
    return jsonify({'success': True, 'message': f"Test case {tc.case_code} imported successfully into repository!"})

