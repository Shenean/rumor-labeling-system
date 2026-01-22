from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app.models import User
from app.utils.auth import generate_token, token_required


bp = Blueprint('auth', __name__)


@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json(silent=True) or {}
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'code': 400, 'message': '缺少必要参数', 'data': None}), 400

    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({'code': 401, 'message': '用户名或密码错误', 'data': None}), 401

    token = generate_token(user.id)
    return jsonify({
        'code': 200,
        'message': '成功',
        'data': {
            'token': token,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.role
            }
        }
    })


@bp.route('/user', methods=['GET'])
@token_required
def get_current_user(current_user):
    return jsonify({
        'code': 200,
        'message': '成功',
        'data': {
            'id': current_user.id,
            'username': current_user.username,
            'email': current_user.email,
            'role': current_user.role
        }
    })


@bp.route('/logout', methods=['POST'])
@token_required
def logout(current_user):
    return jsonify({'code': 200, 'message': '已登出', 'data': None})


@bp.route('/change_password', methods=['PUT'])
@token_required
def change_password(current_user):
    data = request.get_json(silent=True) or {}
    old_password = data.get('old_password')
    new_password = data.get('new_password')

    if not old_password or not new_password:
        return jsonify({'code': 400, 'message': '缺少必要参数', 'data': None}), 400

    if not check_password_hash(current_user.password_hash, old_password):
        return jsonify({'code': 400, 'message': '旧密码不正确', 'data': None}), 400

    current_user.password_hash = generate_password_hash(new_password)
    db.session.commit()

    return jsonify({'code': 200, 'message': '修改成功', 'data': None})


@bp.route('/register', methods=['POST'])
@token_required
def register(current_user):
    if current_user.role != 'admin':
        return jsonify({'code': 403, 'message': '无权限', 'data': None}), 403

    data = request.get_json(silent=True) or {}
    username = data.get('username')
    password = data.get('password')
    role = data.get('role', 'annotator')

    if not username or not password:
        return jsonify({'code': 400, 'message': '缺少必要参数', 'data': None}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({'code': 400, 'message': '用户名已存在', 'data': None}), 400

    new_user = User(
        username=username,
        password_hash=generate_password_hash(password),
        email=data.get('email'),
        role=role
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        'code': 201,
        'message': '创建成功',
        'data': {
            'id': new_user.id,
            'username': new_user.username,
            'email': new_user.email,
            'role': new_user.role
        }
    }), 201

