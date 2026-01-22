from flask import Blueprint, request, jsonify

from app import db
from app.models import ModelLog
from app.utils.auth import token_required
from app.utils.model_mock import model


bp = Blueprint('detection', __name__)


@bp.route('', methods=['POST'])
@token_required
def detect(current_user):
    data = request.get_json(silent=True) or {}
    text = data.get('text')
    if not text:
        return jsonify({'code': 400, 'message': '缺少必要参数', 'data': None}), 400

    result = model.predict(text)
    log = ModelLog(
        model_name='MockBERT',
        input_data=text[:500],
        output_label=result.get('label'),
        confidence=result.get('confidence'),
        user_id=current_user.id
    )
    db.session.add(log)
    db.session.commit()

    return jsonify({
        'code': 200,
        'message': '成功',
        'data': {
            'label': result.get('label'),
            'confidence': result.get('confidence'),
            'explanation': result.get('explanation')
        }
    })


@bp.route('/history', methods=['GET'])
@token_required
def history(current_user):
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', None, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    per_page = limit or per_page

    pagination = ModelLog.query.filter_by(user_id=current_user.id).order_by(ModelLog.called_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    items = []
    for log in pagination.items:
        items.append({
            'text': log.input_data,
            'label': log.output_label,
            'confidence': log.confidence,
            'time': log.called_at.isoformat()
        })

    return jsonify({
        'code': 200,
        'message': '成功',
        'data': {
            'items': items,
            'total': pagination.total
        }
    })

