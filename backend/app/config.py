import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev_key_secret'
    # Default to a local MySQL database, user needs to update this
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'mysql+pymysql://root:password@localhost/rumor_system'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
