from flask import Blueprint, request, jsonify
from app import db
from app.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from app.utils.auth import generate_token
from app.utils.response import ok, fail

bp = Blueprint('user', __name__)

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json(silent=True) or {}
    if not data.get('username') or not data.get('password'):
        return fail('缺少必要参数', http_status=400)
    
    if User.query.filter_by(username=data['username']).first():
        return fail('用户名已存在', http_status=400)
    
    hashed_password = generate_password_hash(data['password'])
    new_user = User(
        username=data['username'],
        password_hash=hashed_password,
        email=data.get('email'),
        role=data.get('role', 'annotator')
    )
    
    db.session.add(new_user)
    db.session.commit()
    
    return ok({'id': new_user.id}, message='创建成功', http_status=201)

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json(silent=True) or {}
    if not data.get('username') or not data.get('password'):
        return fail('缺少必要参数', http_status=400)
        
    user = User.query.filter_by(username=data['username']).first()
    
    if not user or not check_password_hash(user.password_hash, data['password']):
        return fail('用户名或密码错误', http_status=401)
        
    token = generate_token(user.id)
    
    return ok({
        'token': token,
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role
        }
    })
