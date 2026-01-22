from flask import Blueprint

bp = Blueprint('export', __name__)

@bp.route('/', methods=['GET'])
def export_data():
    return {"message": "Data exported"}
