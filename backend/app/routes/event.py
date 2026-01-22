from flask import Blueprint, request
from app import db
from app.models import Event, Sample
from app.utils.auth import token_required
from app.utils.response import ok, fail

bp = Blueprint('event', __name__)

def _ensure_admin(current_user):
    return current_user.role == 'admin'

@bp.route('', methods=['GET'])
@token_required
def get_events(current_user):
    events = Event.query.order_by(Event.created_at.desc()).all()
    result = []
    for e in events:
        sample_count = Sample.query.filter_by(event_id=e.id).count()
        result.append({
            'id': e.id,
            'title': e.title,
            'description': e.description,
            'status': e.status,
            'sample_count': sample_count,
            'created_at': e.created_at.isoformat()
        })
    return ok({'items': result, 'total': len(result)})


@bp.route('/<int:event_id>', methods=['GET'])
@token_required
def get_event_detail(current_user, event_id):
    event = Event.query.get_or_404(event_id)
    sample_count = Sample.query.filter_by(event_id=event.id).count()
    return ok({
        'id': event.id,
        'name': event.title,
        'description': event.description,
        'status': event.status,
        'sample_count': sample_count,
        'created_at': event.created_at.isoformat(),
        'updated_at': event.updated_at.isoformat()
    })


@bp.route('', methods=['POST'])
@token_required
def create_event(current_user):
    if not _ensure_admin(current_user):
        return fail('无权限', http_status=403)

    data = request.get_json(silent=True) or {}
    name = data.get('name') or data.get('title')
    description = data.get('description')
    sample_ids = data.get('sample_ids') or []
    task_ids = data.get('task_ids') or []

    if not name:
        return fail('缺少必要参数', http_status=400)

    event = Event(title=name, description=description, status=data.get('status') or 'active')
    db.session.add(event)
    db.session.flush()

    if isinstance(sample_ids, list):
        for sid in sample_ids:
            sample = Sample.query.get(sid)
            if sample:
                sample.event_id = event.id

    if isinstance(task_ids, list) and task_ids:
        Sample.query.filter(Sample.task_id.in_(task_ids)).update({'event_id': event.id}, synchronize_session=False)

    db.session.commit()
    return ok({'id': event.id}, message='创建成功', http_status=201)


@bp.route('/<int:event_id>', methods=['PUT'])
@token_required
def update_event(current_user, event_id):
    if not _ensure_admin(current_user):
        return fail('无权限', http_status=403)

    event = Event.query.get_or_404(event_id)
    data = request.get_json(silent=True) or {}

    if 'name' in data and data['name']:
        event.title = data['name']
    if 'title' in data and data['title']:
        event.title = data['title']
    if 'description' in data:
        event.description = data.get('description')
    if 'status' in data and data.get('status'):
        event.status = data.get('status')

    db.session.commit()
    return ok(None, message='更新成功')


@bp.route('/<int:event_id>', methods=['DELETE'])
@token_required
def delete_event(current_user, event_id):
    if not _ensure_admin(current_user):
        return fail('无权限', http_status=403)

    event = Event.query.get_or_404(event_id)
    Sample.query.filter_by(event_id=event.id).update({'event_id': None})
    db.session.delete(event)
    db.session.commit()
    return ok(None, message='删除成功')


@bp.route('/cluster', methods=['POST'])
@token_required
def cluster_events(current_user):
    # Mock clustering logic
    # Group samples by "source" as a simple heuristic
    
    samples = Sample.query.filter(Sample.event_id == None).all()
    count = 0
    
    # Simple logic: Create event for each unique source if not exists
    for s in samples:
        if not s.source:
            continue
            
        # Find existing event with title = source
        event = Event.query.filter(Event.title.like(f"%{s.source}%")).first()
        if not event:
            event = Event(title=f"Events from {s.source}", description="Auto-clustered event")
            db.session.add(event)
            db.session.flush() # get ID
            
        s.event_id = event.id
        count += 1
        
    db.session.commit()
    
    return ok({'count': count}, message='聚合完成')
