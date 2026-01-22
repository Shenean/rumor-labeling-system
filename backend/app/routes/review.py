from flask import Blueprint, request, jsonify

from app import db
from app.models import Task, Event, Sample, Annotation, ReviewLog
from app.utils.auth import token_required


bp = Blueprint('review', __name__)


def _ensure_reviewer(current_user):
    return current_user.role in ['admin', 'reviewer']


@bp.route('/tasks', methods=['GET'])
@token_required
def list_review_tasks(current_user):
    if not _ensure_reviewer(current_user):
        return jsonify({'code': 403, 'message': '无权限', 'data': None}), 403

    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', None, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    per_page = limit or per_page

    pagination = Task.query.filter_by(status='pending_review').order_by(Task.updated_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    items = []
    for t in pagination.items:
        total = Sample.query.filter_by(task_id=t.id).count()
        completed = Sample.query.filter(Sample.task_id == t.id, Sample.rumor_label.isnot(None), Sample.rumor_label != 'Unverified').count()
        items.append({
            'id': t.id,
            'name': t.name,
            'description': t.description,
            'assignee_id': t.assignee_id,
            'status': t.status,
            'total': total,
            'completed': completed,
            'updated_at': t.updated_at.isoformat()
        })

    return jsonify({'code': 200, 'message': '成功', 'data': {'items': items, 'total': pagination.total}})


@bp.route('/tasks/<int:task_id>', methods=['GET'])
@token_required
def review_task_detail(current_user, task_id):
    if not _ensure_reviewer(current_user):
        return jsonify({'code': 403, 'message': '无权限', 'data': None}), 403

    task = Task.query.get_or_404(task_id)
    samples = Sample.query.filter_by(task_id=task.id).order_by(Sample.created_at.desc()).all()

    sample_items = []
    for s in samples:
        annotations = Annotation.query.filter_by(sample_id=s.id).order_by(Annotation.annotated_at.desc()).all()
        ann_items = []
        for ann in annotations:
            ann_items.append({
                'id': ann.id,
                'user_id': ann.user_id,
                'label': ann.label,
                'comment': ann.comment,
                'annotated_at': ann.annotated_at.isoformat()
            })
        sample_items.append({
            'id': s.id,
            'content': s.content,
            'source': s.source,
            'language': s.language,
            'label': s.rumor_label,
            'annotations': ann_items
        })

    return jsonify({
        'code': 200,
        'message': '成功',
        'data': {
            'id': task.id,
            'name': task.name,
            'description': task.description,
            'assignee_id': task.assignee_id,
            'status': task.status,
            'samples': sample_items
        }
    })


@bp.route('/tasks/<int:task_id>', methods=['POST'])
@token_required
def submit_task_review(current_user, task_id):
    if not _ensure_reviewer(current_user):
        return jsonify({'code': 403, 'message': '无权限', 'data': None}), 403

    task = Task.query.get_or_404(task_id)
    data = request.get_json(silent=True) or {}
    approved = data.get('approved')
    comments = data.get('comments') or data.get('comment')

    if not isinstance(approved, bool):
        return jsonify({'code': 400, 'message': '缺少必要参数', 'data': None}), 400

    task.status = 'done' if approved else 'rejected'
    log = ReviewLog(
        object_type='task',
        object_id=task.id,
        reviewer_id=current_user.id,
        approved=approved,
        comments=comments
    )
    db.session.add(log)
    db.session.commit()

    return jsonify({'code': 200, 'message': '操作成功', 'data': None})


@bp.route('/events', methods=['GET'])
@token_required
def list_review_events(current_user):
    if not _ensure_reviewer(current_user):
        return jsonify({'code': 403, 'message': '无权限', 'data': None}), 403

    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', None, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    per_page = limit or per_page

    pagination = Event.query.filter_by(status='pending_review').order_by(Event.updated_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    items = []
    for e in pagination.items:
        sample_count = Sample.query.filter_by(event_id=e.id).count()
        items.append({
            'id': e.id,
            'name': e.title,
            'description': e.description,
            'status': e.status,
            'sample_count': sample_count,
            'updated_at': e.updated_at.isoformat()
        })

    return jsonify({'code': 200, 'message': '成功', 'data': {'items': items, 'total': pagination.total}})


@bp.route('/events/<int:event_id>', methods=['GET'])
@token_required
def review_event_detail(current_user, event_id):
    if not _ensure_reviewer(current_user):
        return jsonify({'code': 403, 'message': '无权限', 'data': None}), 403

    event = Event.query.get_or_404(event_id)
    samples = Sample.query.filter_by(event_id=event.id).order_by(Sample.created_at.desc()).all()

    sample_items = []
    for s in samples:
        sample_items.append({
            'id': s.id,
            'content': s.content,
            'source': s.source,
            'language': s.language,
            'label': s.rumor_label
        })

    return jsonify({
        'code': 200,
        'message': '成功',
        'data': {
            'id': event.id,
            'name': event.title,
            'description': event.description,
            'status': event.status,
            'samples': sample_items
        }
    })


@bp.route('/events/<int:event_id>', methods=['POST'])
@token_required
def submit_event_review(current_user, event_id):
    if not _ensure_reviewer(current_user):
        return jsonify({'code': 403, 'message': '无权限', 'data': None}), 403

    event = Event.query.get_or_404(event_id)
    data = request.get_json(silent=True) or {}
    approved = data.get('approved')
    comments = data.get('comments') or data.get('comment')

    if not isinstance(approved, bool):
        return jsonify({'code': 400, 'message': '缺少必要参数', 'data': None}), 400

    event.status = 'approved' if approved else 'rejected'
    log = ReviewLog(
        object_type='event',
        object_id=event.id,
        reviewer_id=current_user.id,
        approved=approved,
        comments=comments
    )
    db.session.add(log)
    db.session.commit()

    return jsonify({'code': 200, 'message': '操作成功', 'data': None})

