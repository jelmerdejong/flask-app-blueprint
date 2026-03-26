import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.flaskenv'))
load_dotenv(os.path.join(basedir, '.env'))
TOP_LEVEL_DIR = os.path.abspath(os.curdir)


def _get_database_uri():
    database_uri = os.environ.get('DATABASE_URL')
    if database_uri and database_uri.startswith('postgres://'):
        return database_uri.replace('postgres://', 'postgresql://', 1)
    if database_uri:
        return database_uri
    return 'sqlite:///' + os.path.join(basedir, 'app.db')


def _get_bool_env(name, default=False):
    value = os.environ.get(name)
    if value is None:
        return default
    return value.strip().lower() in {'1', 'true', 'yes', 'on'}


def _get_int_env(name, default):
    value = os.environ.get(name)
    if value is None:
        return default
    return int(value)


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'add-your-random-key-here'
    SQLALCHEMY_DATABASE_URI = _get_database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BCRYPT_LOG_ROUNDS = 15
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.mandrillapp.com'
    MAIL_PORT = _get_int_env('MAIL_PORT', 587)
    MAIL_USE_TLS = _get_bool_env('MAIL_USE_TLS', False)
    MAIL_USE_SSL = _get_bool_env('MAIL_USE_SSL', False)
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'your-mandrill-username'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'your mandrill-password'
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER') or 'your@default-mail.com'
    MAIL_SEND_ASYNC = _get_bool_env('MAIL_SEND_ASYNC', True)


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    MAIL_SUPPRESS_SEND = True
    MAIL_SEND_ASYNC = False
    BCRYPT_LOG_ROUNDS = 4
