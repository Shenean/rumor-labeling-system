from flask import Blueprint, request, jsonify
from app import db
from app.models import Task, Sample, Annotation
from app.utils.auth import token_required
from app.utils.response import ok, fail

bp = Blueprint('annotate', __name__)

@bp.route('/tasks', methods=['GET'])
@token_required
def get_tasks(current_user):
    # For simplicity, return samples that need annotation (rumor_label is Unverified or NULL)
    # In a real system, this would query the 'Task' table assigned to the user
    
    # Check if user has explicit tasks
    tasks = Task.query.filter_by(assignee_id=current_user.id, status='pending').all()
    task_list = []
    
    if tasks:
        for t in tasks:
            task_list.append({
                'id': t.id,
                'name': t.name,
                'description': t.description,
                'status': t.status
            })
    else:
        # Fallback: find unverified samples
        samples = Sample.query.filter((Sample.rumor_label == None) | (Sample.rumor_label == 'Unverified')).limit(10).all()
        for s in samples:
            task_list.append({
                'id': s.id, # Using sample ID as task ID proxy for this simple logic
                'name': f'Annotate Sample #{s.id}',
                'description': s.content[:50],
                'status': 'pending',
                'sample_id': s.id
            })
            
    return ok({'items': task_list, 'total': len(task_list)})

@bp.route('/submit', methods=['POST'])
@token_required
def submit_annotation(current_user):
    data = request.get_json(silent=True) or {}
    sample_id = data.get('sample_id')
    label = data.get('label')
    
    if not sample_id or not label:
        return fail('缺少必要参数', http_status=400)
        
    # Save annotation
    annotation = Annotation(
        sample_id=sample_id,
        user_id=current_user.id,
        label=label,
        comment=data.get('comment')
    )
    db.session.add(annotation)
    
    # Update sample label (simple logic: latest annotation wins)
    sample = Sample.query.get(sample_id)
    if sample:
        sample.rumor_label = label
        
    db.session.commit()
    
    return ok(None, message='标注提交成功')
