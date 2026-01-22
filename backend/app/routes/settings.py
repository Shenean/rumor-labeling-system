import json

from flask import Blueprint, request

from app import db
from app.models import Setting, User, OperationLog
from app.utils.auth import token_required
from app.utils.response import ok, fail


bp = Blueprint('settings', __name__)


def _ensure_admin(current_user):
    return current_user.role == 'admin'


def _get_roles():
    roles_setting = Setting.query.filter_by(key='roles').first()
    if not roles_setting or not roles_setting.value:
        return [
            {'id': 'admin', 'name': 'admin', 'permissions': ['*']},
            {'id': 'annotator', 'name': 'annotator', 'permissions': []},
            {'id': 'reviewer', 'name': 'reviewer', 'permissions': []}
        ]

    try:
        roles = json.loads(roles_setting.value)
        if isinstance(roles, list):
            return roles
    except Exception:
        return []

    return []


def _save_roles(roles):
    roles_setting = Setting.query.filter_by(key='roles').first()
    if not roles_setting:
        roles_setting = Setting(key='roles', value='')
        db.session.add(roles_setting)
    roles_setting.value = json.dumps(roles, ensure_ascii=False)


@bp.route('/config', methods=['GET'])
@token_required
def get_config(current_user):
    if not _ensure_admin(current_user):
        return fail('无权限', http_status=403)

    settings = Setting.query.all()
    data = {}
    for s in settings:
        if s.key == 'roles':
            continue
        data[s.key] = s.value
    return ok(data)


@bp.route('/config', methods=['PUT'])
@token_required
def update_config(current_user):
    if not _ensure_admin(current_user):
        return fail('无权限', http_status=403)

    data = request.get_json(silent=True) or {}
    if not isinstance(data, dict):
        return fail('参数格式错误', http_status=400)

    for key, value in data.items():
        if not isinstance(key, str) or not key.strip():
            continue
        if key == 'roles':
            continue
        setting = Setting.query.filter_by(key=key).first()
        if not setting:
            setting = Setting(key=key, value=None)
            db.session.add(setting)
        setting.value = json.dumps(value, ensure_ascii=False) if not isinstance(value, str) else value

    db.session.commit()
    return ok(None, message='保存成功')


@bp.route('/roles', methods=['GET'])
@token_required
def list_roles(current_user):
    if not _ensure_admin(current_user):
        return fail('无权限', http_status=403)
    return ok(_get_roles())


@bp.route('/roles', methods=['POST'])
@token_required
def create_role(current_user):
    if not _ensure_admin(current_user):
        return fail('无权限', http_status=403)

    data = request.get_json(silent=True) or {}
    name = data.get('name')
    permissions = data.get('permissions') or []
    if not name:
        return fail('缺少必要参数', http_status=400)

    roles = _get_roles()
    if any(r.get('id') == name for r in roles):
        return fail('角色已存在', http_status=400)

    roles.append({'id': name, 'name': name, 'permissions': permissions if isinstance(permissions, list) else []})
    _save_roles(roles)
    db.session.commit()
    return ok({'id': name}, message='创建成功', http_status=201)


@bp.route('/roles/<string:role_id>', methods=['PUT'])
@token_required
def update_role(current_user, role_id):
    if not _ensure_admin(current_user):
        return fail('无权限', http_status=403)

    data = request.get_json(silent=True) or {}
    permissions = data.get('permissions')
    roles = _get_roles()
    updated = False
    for r in roles:
        if r.get('id') == role_id:
            if isinstance(permissions, list):
                r['permissions'] = permissions
            if isinstance(data.get('name'), str) and data.get('name'):
                r['name'] = data.get('name')
            updated = True
            break

    if not updated:
        return fail('角色不存在', http_status=404)

    _save_roles(roles)
    db.session.commit()
    return ok(None, message='更新成功')


@bp.route('/roles/<string:role_id>', methods=['DELETE'])
@token_required
def delete_role(current_user, role_id):
    if not _ensure_admin(current_user):
        return fail('无权限', http_status=403)

    roles = _get_roles()
    roles = [r for r in roles if r.get('id') != role_id]
    _save_roles(roles)
    db.session.commit()
    return ok(None, message='删除成功')


@bp.route('/users', methods=['GET'])
@token_required
def list_users(current_user):
    if not _ensure_admin(current_user):
        return fail('无权限', http_status=403)

    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', None, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    per_page = limit or per_page

    pagination = User.query.order_by(User.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    items = []
    for u in pagination.items:
        items.append({
            'id': u.id,
            'username': u.username,
            'email': u.email,
            'role': u.role,
            'created_at': u.created_at.isoformat()
        })

    return ok({'items': items, 'total': pagination.total})


@bp.route('/users/<int:user_id>/roles', methods=['PUT'])
@token_required
def update_user_roles(current_user, user_id):
    if not _ensure_admin(current_user):
        return fail('无权限', http_status=403)

    user = User.query.get_or_404(user_id)
    data = request.get_json(silent=True) or {}
    roles = data.get('roles') or []
    if not isinstance(roles, list) or not roles:
        return fail('缺少必要参数', http_status=400)

    user.role = str(roles[0])
    db.session.commit()
    return ok(None, message='更新成功')


@bp.route('/logs', methods=['GET'])
@token_required
def list_logs(current_user):
    if not _ensure_admin(current_user):
        return fail('无权限', http_status=403)

    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', None, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    per_page = limit or per_page

    user_id = request.args.get('user_id', None, type=int)
    action = request.args.get('action', None)

    query = OperationLog.query
    if user_id is not None:
        query = query.filter_by(user_id=user_id)
    if action:
        query = query.filter(OperationLog.path.like(f'%{action}%'))

    pagination = query.order_by(OperationLog.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    items = []
    for log in pagination.items:
        items.append({
            'id': log.id,
            'user_id': log.user_id,
            'method': log.method,
            'path': log.path,
            'status_code': log.status_code,
            'query_string': log.query_string,
            'created_at': log.created_at.isoformat()
        })

    return ok({'items': items, 'total': pagination.total})

