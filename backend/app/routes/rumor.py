from flask import Blueprint, request, jsonify
from app import db
from app.models import Sample, ModelLog
from app.utils.model_mock import model
from app.utils.auth import token_required
from app.utils.response import ok, fail

bp = Blueprint('rumor', __name__)

@bp.route('/detect', methods=['POST'])
@token_required
def detect(current_user):
    data = request.get_json(silent=True) or {}
    text = data.get('text')
    if not text:
        return fail('缺少必要参数', http_status=400)
        
    # Call mock model
    result = model.predict(text)
    
    # Save to samples if requested (optional) or just log
    # Here we log the invocation
    log = ModelLog(
        model_name='MockBERT',
        input_data=text[:500], # truncate if too long
        output_label=result['label'],
        confidence=result['confidence'],
        user_id=current_user.id
    )
    db.session.add(log)
    db.session.commit()
    
    return ok({
        'label': result.get('label'),
        'confidence': result.get('confidence'),
        'explanation': result.get('explanation')
    })
