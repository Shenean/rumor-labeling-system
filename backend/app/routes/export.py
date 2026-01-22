from flask import Blueprint, request, send_file
from app.models import Annotation, Sample, User
from app.utils.auth import token_required
import pandas as pd
import io

bp = Blueprint('export', __name__)

@bp.route('/', methods=['GET'])
@token_required
def export_data(current_user):
    # Export annotations
    query = db.session.query(Annotation, Sample, User).\
        join(Sample, Annotation.sample_id == Sample.id).\
        join(User, Annotation.user_id == User.id).all()
        
    data = []
    for ann, sample, user in query:
        data.append({
            'Annotation ID': ann.id,
            'Sample Content': sample.content,
            'Label': ann.label,
            'Annotator': user.username,
            'Time': ann.annotated_at,
            'Comment': ann.comment
        })
        
    df = pd.DataFrame(data)
    
    # Create Excel in memory
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Annotations')
        
    output.seek(0)
    
    return send_file(
        output,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name='annotations_export.xlsx'
    )
