from flask import Blueprint, request, jsonify

from app import db
from app.models import Task, Sample, Annotation
from app.utils.auth import token_required


bp = Blueprint('task', __name__)


def _ensure_admin(current_user):
    return current_user.role == 'admin'


@bp.route('', methods=['GET'])
@token_required
def list_tasks(current_user):
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', None, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    per_page = limit or per_page

    status = request.args.get('status')
    assigned_to = request.args.get('assigned_to', None, type=int)

    query = Task.query
    if status:
        query = query.filter(Task.status == status)

    if _ensure_admin(current_user):
        if assigned_to is not None:
            query = query.filter(Task.assignee_id == assigned_to)
    else:
        query = query.filter(Task.assignee_id == current_user.id)

    pagination = query.order_by(Task.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)

    items = []
    for t in pagination.items:
        items.append({
            'id': t.id,
            'name': t.name,
            'description': t.description,
            'status': t.status,
            'assignee_id': t.assignee_id,
            'created_at': t.created_at.isoformat()
        })

    return jsonify({'code': 200, 'message': '成功', 'data': {'items': items, 'total': pagination.total}})


@bp.route('/<int:task_id>', methods=['GET'])
@token_required
def get_task(current_user, task_id):
    task = Task.query.get_or_404(task_id)

    if not _ensure_admin(current_user) and task.assignee_id != current_user.id:
        return jsonify({'code': 403, 'message': '无权限', 'data': None}), 403

    total = Sample.query.filter_by(task_id=task.id).count()
    completed = Sample.query.filter(Sample.task_id == task.id, Sample.rumor_label.isnot(None), Sample.rumor_label != 'Unverified').count()

    return jsonify({
        'code': 200,
        'message': '成功',
        'data': {
            'id': task.id,
            'name': task.name,
            'description': task.description,
            'status': task.status,
            'assignee_id': task.assignee_id,
            'created_at': task.created_at.isoformat(),
            'updated_at': task.updated_at.isoformat(),
            'total': total,
            'completed': completed
        }
    })


@bp.route('', methods=['POST'])
@token_required
def create_task(current_user):
    if not _ensure_admin(current_user):
        return jsonify({'code': 403, 'message': '无权限', 'data': None}), 403

    data = request.get_json(silent=True) or {}
    name = data.get('name')
    description = data.get('description')
    sample_ids = data.get('sample_ids') or []
    assignees = data.get('assignees') or []

    if not name:
        return jsonify({'code': 400, 'message': '缺少必要参数', 'data': None}), 400

    assignee_id = None
    if isinstance(assignees, list) and assignees:
        assignee_id = assignees[0]

    task = Task(name=name, description=description, assignee_id=assignee_id, status='pending')
    db.session.add(task)
    db.session.flush()

    if not isinstance(sample_ids, list):
        return jsonify({'code': 400, 'message': '参数格式错误', 'data': None}), 400

    for sid in sample_ids:
        sample = Sample.query.get(sid)
        if not sample:
            continue
        sample.task_id = task.id

    db.session.commit()

    return jsonify({'code': 201, 'message': '创建成功', 'data': {'id': task.id}}), 201


@bp.route('/<int:task_id>', methods=['PUT'])
@token_required
def update_task(current_user, task_id):
    if not _ensure_admin(current_user):
        return jsonify({'code': 403, 'message': '无权限', 'data': None}), 403

    task = Task.query.get_or_404(task_id)
    data = request.get_json(silent=True) or {}

    if 'name' in data and data['name']:
        task.name = data['name']
    if 'description' in data:
        task.description = data.get('description')
    if 'status' in data and data.get('status'):
        task.status = data.get('status')
    if 'assignees' in data and isinstance(data.get('assignees'), list):
        assignees = data.get('assignees') or []
        task.assignee_id = assignees[0] if assignees else None
    if 'assigned_to' in data:
        task.assignee_id = data.get('assigned_to')

    if 'sample_ids' in data:
        sample_ids = data.get('sample_ids') or []
        if not isinstance(sample_ids, list):
            return jsonify({'code': 400, 'message': '参数格式错误', 'data': None}), 400

        Sample.query.filter_by(task_id=task.id).update({'task_id': None})
        for sid in sample_ids:
            sample = Sample.query.get(sid)
            if not sample:
                continue
            sample.task_id = task.id

    db.session.commit()
    return jsonify({'code': 200, 'message': '更新成功', 'data': None})


@bp.route('/<int:task_id>', methods=['DELETE'])
@token_required
def delete_task(current_user, task_id):
    if not _ensure_admin(current_user):
        return jsonify({'code': 403, 'message': '无权限', 'data': None}), 403

    task = Task.query.get_or_404(task_id)
    Sample.query.filter_by(task_id=task.id).update({'task_id': None})
    db.session.delete(task)
    db.session.commit()
    return jsonify({'code': 200, 'message': '删除成功', 'data': None})


@bp.route('/<int:task_id>/claim', methods=['POST'])
@token_required
def claim_task(current_user, task_id):
    task = Task.query.get_or_404(task_id)
    if task.assignee_id and task.assignee_id != current_user.id:
        return jsonify({'code': 400, 'message': '任务已被领取', 'data': None}), 400

    task.assignee_id = current_user.id
    db.session.commit()
    return jsonify({'code': 200, 'message': '领取成功', 'data': None})


@bp.route('/<int:task_id>/unclaim', methods=['POST'])
@token_required
def unclaim_task(current_user, task_id):
    task = Task.query.get_or_404(task_id)
    if not _ensure_admin(current_user) and task.assignee_id != current_user.id:
        return jsonify({'code': 403, 'message': '无权限', 'data': None}), 403

    task.assignee_id = None
    db.session.commit()
    return jsonify({'code': 200, 'message': '已取消领取', 'data': None})


@bp.route('/<int:task_id>/samples', methods=['GET'])
@token_required
def get_task_samples(current_user, task_id):
    task = Task.query.get_or_404(task_id)
    if not _ensure_admin(current_user) and task.assignee_id != current_user.id:
        return jsonify({'code': 403, 'message': '无权限', 'data': None}), 403

    samples = Sample.query.filter_by(task_id=task.id).order_by(Sample.created_at.desc()).all()
    data = []
    for s in samples:
        data.append({
            'id': s.id,
            'content': s.content,
            'source': s.source,
            'language': s.language,
            'label': s.rumor_label,
            'event_id': s.event_id
        })

    return jsonify({'code': 200, 'message': '成功', 'data': data})


@bp.route('/<int:task_id>/samples/<int:sample_id>/label', methods=['POST'])
@token_required
def submit_sample_label(current_user, task_id, sample_id):
    task = Task.query.get_or_404(task_id)
    if not _ensure_admin(current_user) and task.assignee_id != current_user.id:
        return jsonify({'code': 403, 'message': '无权限', 'data': None}), 403

    sample = Sample.query.get_or_404(sample_id)
    if sample.task_id != task.id:
        return jsonify({'code': 400, 'message': '样本不属于该任务', 'data': None}), 400

    data = request.get_json(silent=True) or {}
    label = data.get('label')
    comments = data.get('comments') or data.get('comment')
    if not label:
        return jsonify({'code': 400, 'message': '缺少必要参数', 'data': None}), 400

    annotation = Annotation(sample_id=sample.id, user_id=current_user.id, label=label, comment=comments)
    db.session.add(annotation)
    sample.rumor_label = label
    db.session.flush()

    total = Sample.query.filter_by(task_id=task.id).count()
    completed = Sample.query.filter(Sample.task_id == task.id, Sample.rumor_label.isnot(None), Sample.rumor_label != 'Unverified').count()
    if total > 0 and completed >= total and task.status == 'pending':
        task.status = 'pending_review'

    db.session.commit()
    return jsonify({'code': 200, 'message': '标注提交成功', 'data': None})


@bp.route('/<int:task_id>/progress', methods=['GET'])
@token_required
def task_progress(current_user, task_id):
    task = Task.query.get_or_404(task_id)
    if not _ensure_admin(current_user) and task.assignee_id != current_user.id:
        return jsonify({'code': 403, 'message': '无权限', 'data': None}), 403

    total = Sample.query.filter_by(task_id=task.id).count()
    completed = Sample.query.filter(Sample.task_id == task.id, Sample.rumor_label.isnot(None), Sample.rumor_label != 'Unverified').count()
    return jsonify({'code': 200, 'message': '成功', 'data': {'total': total, 'completed': completed}})

