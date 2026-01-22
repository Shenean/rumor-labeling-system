from flask import Blueprint

bp = Blueprint('sample', __name__)

@bp.route('/', methods=['GET'])
def get_samples():
    return {"samples": []}

@bp.route('/', methods=['POST'])
def create_sample():
    return {"message": "Sample created"}
