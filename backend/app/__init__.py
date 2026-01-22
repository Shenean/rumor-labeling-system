from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from app.config import Config
from app.utils.auth import get_user_id_from_request

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Init extensions
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app) # Enable CORS for all routes

    # Register Blueprints
    from app.routes import rumor, annotate, sample, event, export, user, auth, detection, task, review
    app.register_blueprint(rumor.bp, url_prefix='/api/rumor')
    app.register_blueprint(annotate.bp, url_prefix='/api/annotation')
    app.register_blueprint(sample.bp, url_prefix='/api/samples')
    app.register_blueprint(event.bp, url_prefix='/api/events')
    app.register_blueprint(export.bp, url_prefix='/api/export')
    app.register_blueprint(user.bp, url_prefix='/api/users')
    app.register_blueprint(auth.bp, url_prefix='/api/auth')
    app.register_blueprint(detection.bp, url_prefix='/api/detect')
    app.register_blueprint(task.bp, url_prefix='/api/tasks')
    app.register_blueprint(review.bp, url_prefix='/api/review')
    from app.routes import settings
    app.register_blueprint(settings.bp, url_prefix='/api/settings')

    @app.after_request
    def log_operation(response):
        try:
            if request.path.startswith('/api'):
                from app.models import OperationLog
                user_id = get_user_id_from_request()
                log = OperationLog(
                    user_id=user_id,
                    method=request.method,
                    path=request.path,
                    status_code=response.status_code,
                    query_string=request.query_string.decode('utf-8', errors='ignore') if request.query_string else None
                )
                db.session.add(log)
                db.session.commit()
        except Exception:
            try:
                db.session.rollback()
            except Exception:
                pass
        return response

    return app
