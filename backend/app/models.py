from datetime import datetime
from app import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(100))
    role = db.Column(db.String(20), default='annotator')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Sample(db.Model):
    __tablename__ = 'samples'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    source = db.Column(db.String(100))
    language = db.Column(db.String(20), default='zh')
    rumor_label = db.Column(db.String(20))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Annotation(db.Model):
    __tablename__ = 'annotations'
    id = db.Column(db.Integer, primary_key=True)
    sample_id = db.Column(db.Integer, db.ForeignKey('samples.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    label = db.Column(db.String(20), nullable=False)
    comment = db.Column(db.Text)
    annotated_at = db.Column(db.DateTime, default=datetime.utcnow)

class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    assignee_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ModelLog(db.Model):
    __tablename__ = 'model_logs'
    id = db.Column(db.Integer, primary_key=True)
    model_name = db.Column(db.String(50))
    input_data = db.Column(db.Text)
    output_label = db.Column(db.String(20))
    confidence = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    called_at = db.Column(db.DateTime, default=datetime.utcnow)


class ReviewLog(db.Model):
    __tablename__ = 'review_logs'
    id = db.Column(db.Integer, primary_key=True)
    object_type = db.Column(db.String(20), nullable=False)
    object_id = db.Column(db.Integer, nullable=False)
    reviewer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    approved = db.Column(db.Boolean, nullable=False)
    comments = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Setting(db.Model):
    __tablename__ = 'settings'
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False)
    value = db.Column(db.Text)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class OperationLog(db.Model):
    __tablename__ = 'operation_logs'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    method = db.Column(db.String(10))
    path = db.Column(db.String(255))
    status_code = db.Column(db.Integer)
    query_string = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
