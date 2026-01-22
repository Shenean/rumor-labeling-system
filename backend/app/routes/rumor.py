from flask import Blueprint

bp = Blueprint('rumor', __name__)

@bp.route('/detect', methods=['POST'])
def detect():
    return {"message": "Rumor detection endpoint"}
