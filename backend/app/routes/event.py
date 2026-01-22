from flask import Blueprint, request, jsonify
from app import db
from app.models import Event, Sample
from app.utils.auth import token_required

bp = Blueprint('event', __name__)

@bp.route('/', methods=['GET'])
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
            'sample_count': sample_count,
            'created_at': e.created_at.isoformat()
        })
    return jsonify({'events': result})

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
    
    return jsonify({'message': f'Clustered {count} samples into events'})
