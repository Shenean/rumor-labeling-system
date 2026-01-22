from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from functools import wraps
from flask import request, jsonify, current_app
from app.models import User
from app.utils.response import fail

def _serializer():
    return URLSafeTimedSerializer(current_app.config['SECRET_KEY'], salt='auth-token')

def generate_token(user_id):
    return _serializer().dumps({'user_id': user_id})

def get_user_id_from_request():
    token = None
    if 'Authorization' in request.headers:
        auth_header = request.headers['Authorization']
        if auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
    if not token:
        return None
    try:
        data = _serializer().loads(token, max_age=60 * 60 * 24)
        return data.get('user_id')
    except (BadSignature, SignatureExpired, Exception):
        return None

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(" ")[1]
        
        if not token:
            return fail('未登录', http_status=401)

        try:
            data = _serializer().loads(token, max_age=60 * 60 * 24)
            current_user = User.query.get(data['user_id'])
            if not current_user:
                 return fail('用户不存在', http_status=401)
        except (BadSignature, SignatureExpired, Exception):
            return fail('令牌无效', http_status=401)

        return f(current_user, *args, **kwargs)

    return decorated
