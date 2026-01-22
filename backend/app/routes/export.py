from flask import Blueprint, request, send_file
from app import db
from app.models import Annotation, Sample, User, ReviewLog, ModelLog, Task, Event
from app.utils.auth import token_required
import pandas as pd
import io

bp = Blueprint('export', __name__)

def _ensure_admin(current_user):
    return current_user.role == 'admin'


def _send_excel(rows, filename, sheet_name):
    df = pd.DataFrame(rows)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name=sheet_name)
    output.seek(0)
    return send_file(
        output,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name=filename
    )


@bp.route('/samples', methods=['GET'])
@token_required
def export_samples(current_user):
    if not _ensure_admin(current_user):
        return {'code': 403, 'message': '无权限', 'data': None}, 403

    samples = Sample.query.order_by(Sample.created_at.desc()).all()
    rows = []
    for s in samples:
        rows.append({
            'id': s.id,
            'content': s.content,
            'source': s.source,
            'language': s.language,
            'label': s.rumor_label,
            'event_id': s.event_id,
            'task_id': s.task_id,
            'created_at': s.created_at.isoformat(),
            'updated_at': s.updated_at.isoformat()
        })

    return _send_excel(rows, filename='samples_export.xlsx', sheet_name='Samples')


@bp.route('/annotations', methods=['GET'])
@token_required
def export_annotations(current_user):
    if not _ensure_admin(current_user):
        return {'code': 403, 'message': '无权限', 'data': None}, 403

    query = db.session.query(Annotation, Sample, User).join(Sample, Annotation.sample_id == Sample.id).join(
        User, Annotation.user_id == User.id
    )
    task_id = request.args.get('task_id', None, type=int)
    if task_id is not None:
        query = query.filter(Sample.task_id == task_id)

    rows = []
    for ann, sample, user in query.order_by(Annotation.annotated_at.desc()).all():
        rows.append({
            'annotation_id': ann.id,
            'sample_id': sample.id,
            'task_id': sample.task_id,
            'content': sample.content,
            'label': ann.label,
            'annotator': user.username,
            'annotated_at': ann.annotated_at.isoformat(),
            'comment': ann.comment
        })

    return _send_excel(rows, filename='annotations_export.xlsx', sheet_name='Annotations')


@bp.route('/audits', methods=['GET'])
@token_required
def export_audits(current_user):
    if not _ensure_admin(current_user):
        return {'code': 403, 'message': '无权限', 'data': None}, 403

    logs = ReviewLog.query.order_by(ReviewLog.created_at.desc()).all()
    rows = []
    for log in logs:
        rows.append({
            'id': log.id,
            'object_type': log.object_type,
            'object_id': log.object_id,
            'reviewer_id': log.reviewer_id,
            'approved': bool(log.approved),
            'comments': log.comments,
            'created_at': log.created_at.isoformat()
        })

    return _send_excel(rows, filename='audits_export.xlsx', sheet_name='Audits')


@bp.route('/reports', methods=['POST'])
@token_required
def export_reports(current_user):
    if not _ensure_admin(current_user):
        return {'code': 403, 'message': '无权限', 'data': None}, 403

    data = request.get_json(silent=True) or {}
    report_type = data.get('type') or 'summary'

    if report_type == 'summary':
        rows = [{
            'users': User.query.count(),
            'samples': Sample.query.count(),
            'tasks': Task.query.count(),
            'events': Event.query.count(),
            'annotations': Annotation.query.count(),
            'model_calls': ModelLog.query.count(),
            'reviews': ReviewLog.query.count()
        }]
        return _send_excel(rows, filename='report_summary.xlsx', sheet_name='Summary')

    return {'code': 400, 'message': '未知报表类型', 'data': None}, 400


@bp.route('/', methods=['GET'])
@token_required
def export_data(current_user):
    return export_annotations(current_user)
