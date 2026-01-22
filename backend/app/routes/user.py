from flask import Blueprint

bp = Blueprint('user', __name__)

@bp.route('/login', methods=['POST'])
def login():
    return {"message": "Login successful"}
