from flask import Blueprint, request, jsonify
from app import db
from app.models import Sample
from app.utils.auth import token_required

bp = Blueprint('sample', __name__)

@bp.route('/', methods=['GET'])
@token_required
def get_samples(current_user):
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', None, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    per_page = limit or per_page
    search = request.args.get('query', '') or request.args.get('search', '')
    
    query = Sample.query
    if search:
        query = query.filter(Sample.content.like(f'%{search}%'))
        
    pagination = query.order_by(Sample.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    
    items = []
    for s in pagination.items:
        items.append({
            'id': s.id,
            'content': s.content,
            'source': s.source,
            'language': s.language,
            'label': s.rumor_label,
            'event_id': s.event_id,
            'task_id': s.task_id,
            'created_at': s.created_at.isoformat()
        })
        
    return jsonify({
        'code': 200,
        'message': '成功',
        'data': {
            'items': items,
            'total': pagination.total
        }
    })

@bp.route('/', methods=['POST'])
@token_required
def create_sample(current_user):
    data = request.get_json()
    if not data.get('content'):
        return jsonify({'code': 400, 'message': '缺少必要参数', 'data': None}), 400
        
    new_sample = Sample(
        content=data['content'],
        source=data.get('source'),
        language=data.get('language', 'zh'),
        rumor_label=data.get('rumor_label', 'Unverified')
    )
    
    db.session.add(new_sample)
    db.session.commit()
    
    return jsonify({
        'code': 201,
        'message': '创建成功',
        'data': {
            'id': new_sample.id
        }
    }), 201


@bp.route('/<int:id>', methods=['GET'])
@token_required
def get_sample_detail(current_user, id):
    sample = Sample.query.get_or_404(id)
    return jsonify({
        'code': 200,
        'message': '成功',
        'data': {
            'id': sample.id,
            'content': sample.content,
            'source': sample.source,
            'language': sample.language,
            'label': sample.rumor_label,
            'event_id': sample.event_id,
            'task_id': sample.task_id,
            'created_at': sample.created_at.isoformat(),
            'updated_at': sample.updated_at.isoformat()
        }
    })


@bp.route('/<int:id>', methods=['PUT'])
@token_required
def update_sample(current_user, id):
    sample = Sample.query.get_or_404(id)
    data = request.get_json(silent=True) or {}

    if current_user.role not in ['admin', 'annotator']:
        return jsonify({'code': 403, 'message': '无权限', 'data': None}), 403

    if 'content' in data and data['content']:
        sample.content = data['content']
    if 'source' in data:
        sample.source = data.get('source')
    if 'language' in data:
        sample.language = data.get('language') or sample.language
    if 'label' in data:
        sample.rumor_label = data.get('label')
    if 'rumor_label' in data:
        sample.rumor_label = data.get('rumor_label')
    if 'event_id' in data:
        sample.event_id = data.get('event_id')
    if 'task_id' in data:
        sample.task_id = data.get('task_id')

    db.session.commit()

    return jsonify({'code': 200, 'message': '更新成功', 'data': None})

@bp.route('/<int:id>', methods=['DELETE'])
@token_required
def delete_sample(current_user, id):
    if current_user.role != 'admin':
        return jsonify({'code': 403, 'message': '无权限', 'data': None}), 403
        
    sample = Sample.query.get_or_404(id)
    db.session.delete(sample)
    db.session.commit()
    
    return jsonify({'code': 200, 'message': '删除成功', 'data': None})


@bp.route('/batch_import', methods=['POST'])
@token_required
def batch_import(current_user):
    if current_user.role != 'admin':
        return jsonify({'code': 403, 'message': '无权限', 'data': None}), 403

    data = request.get_json(silent=True) or {}
    samples = data.get('samples')
    if not isinstance(samples, list):
        return jsonify({'code': 400, 'message': '参数格式错误', 'data': None}), 400

    success = 0
    failed = 0
    for item in samples:
        if not isinstance(item, dict) or not item.get('content'):
            failed += 1
            continue

        new_sample = Sample(
            content=item['content'],
            source=item.get('source'),
            language=item.get('language', 'zh'),
            rumor_label=item.get('label') or item.get('rumor_label') or 'Unverified'
        )
        db.session.add(new_sample)
        success += 1

    db.session.commit()

    return jsonify({
        'code': 200,
        'message': '导入完成',
        'data': {
            'success': success,
            'failed': failed
        }
    })
