from flask import jsonify


def ok(data=None, message='成功', http_status=200, code=None):
    return jsonify({
        'code': code if code is not None else http_status,
        'message': message,
        'data': data
    }), http_status


def fail(message='失败', http_status=400, code=None, data=None):
    return jsonify({
        'code': code if code is not None else http_status,
        'message': message,
        'data': data
    }), http_status

