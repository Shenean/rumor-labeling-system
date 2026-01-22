from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints
    from app.routes import rumor, annotate, sample, event, export, user
    app.register_blueprint(rumor.bp, url_prefix='/api/rumor')
    app.register_blueprint(annotate.bp, url_prefix='/api/annotation')
    app.register_blueprint(sample.bp, url_prefix='/api/samples')
    app.register_blueprint(event.bp, url_prefix='/api/events')
    app.register_blueprint(export.bp, url_prefix='/api/export')
    app.register_blueprint(user.bp, url_prefix='/api/users')

    return app
