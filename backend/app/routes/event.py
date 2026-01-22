from flask import Blueprint

bp = Blueprint('event', __name__)

@bp.route('/cluster', methods=['POST'])
def cluster_events():
    return {"message": "Events clustered"}
