from flask import Blueprint

bp = Blueprint('annotate', __name__)

@bp.route('/tasks', methods=['GET'])
def get_tasks():
    return {"tasks": []}

@bp.route('/submit', methods=['POST'])
def submit_annotation():
    return {"message": "Annotation submitted"}
