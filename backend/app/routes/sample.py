from flask import Blueprint, request, jsonify
from app import db
from app.models import Sample
from app.utils.auth import token_required

bp = Blueprint('sample', __name__)

@bp.route('/', methods=['GET'])
@token_required
def get_samples(current_user):
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    search = request.args.get('search', '')
    
    query = Sample.query
    if search:
        query = query.filter(Sample.content.like(f'%{search}%'))
        
    pagination = query.order_by(Sample.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    
    samples = []
    for s in pagination.items:
        samples.append({
            'id': s.id,
            'content': s.content,
            'source': s.source,
            'language': s.language,
            'rumor_label': s.rumor_label,
            'created_at': s.created_at.isoformat()
        })
        
    return jsonify({
        'samples': samples,
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    })

@bp.route('/', methods=['POST'])
@token_required
def create_sample(current_user):
    data = request.get_json()
    if not data.get('content'):
        return jsonify({'message': 'Content is required'}), 400
        
    new_sample = Sample(
        content=data['content'],
        source=data.get('source'),
        language=data.get('language', 'zh'),
        rumor_label=data.get('rumor_label', 'Unverified')
    )
    
    db.session.add(new_sample)
    db.session.commit()
    
    return jsonify({'message': 'Sample created', 'id': new_sample.id}), 201

@bp.route('/<int:id>', methods=['DELETE'])
@token_required
def delete_sample(current_user, id):
    if current_user.role != 'admin':
        return jsonify({'message': 'Permission denied'}), 403
        
    sample = Sample.query.get_or_404(id)
    db.session.delete(sample)
    db.session.commit()
    
    return jsonify({'message': 'Sample deleted'})
