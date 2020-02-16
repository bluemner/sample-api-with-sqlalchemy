""" Application Configuration settings
    converts from environment variable to
    python
"""
import os
import sys
import tempfile
import logging
from logging import Logger


def get_logger(name: str = __name__) -> Logger:
    """ Gets a logger that will output to sys out by default
    """
    root: Logger = logging.getLogger(name)
    level: int = logging.DEBUG if environment_is_local() else logging.INFO
    root.setLevel(level)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    root.addHandler(handler)
    return root


def environment_is_local() -> bool:
    """  Returns true if running locally
    """
    return os.getenv('PYTHON_ENV', 'LOCAL').lower() in ['local', 'dev']


def to_bool(value: str) -> bool:
    """ Converts string to bool
    """
    return str(value).lower() == 'true' if value is not None else False


TITLE: str = os.getenv('TITLE', 'Sample App')

################################################################################
# Flask / WSGI Settings
################################################################################
APPLICATION_PORT: int = int(os.getenv('APPLICATION_PORT', '5000'))
APPLICATION_BIND: str = os.getenv('APPLICATION_BIND', '127.0.0.1')

FLASK_DEBUG: bool = to_bool(os.getenv('FLASK_DEBUG', 'False'))
FLASK_URL_PREFIX: str = os.getenv('FLASK_URL_PREFIX', '/api')
################################################################################
# Flask - Rest Plus Seetings
################################################################################
REST_PLUS_SWAGGER_UI_DOC_EXPANSION: bool = to_bool(
    os.getenv('REST_PLUS_SWAGGER_UI_DOC_EXPANSION'))
REST_PLUS_VALIDATE: bool = to_bool(
    os.getenv('REST_PLUS_VALIDATE'))
REST_PLUS_MASK_SWAGGER: bool = to_bool(
    os.getenv('REST_PLUS_MASK_SWAGGER'))
REST_PLUS_SWAGGER: bool = to_bool(
    os.getenv('REST_PLUS_SWAGGER'))
REST_PLUS_ERROR_404_HELP: bool = to_bool(
    os.getenv('REST_PLUS_ERROR_404_HELP'))


################################################################################
# CORS
################################################################################
CORS_ORIGIN: str = os.getenv('CORS_ORIGIN', '*')


################################################################################
# Data
################################################################################
APP_DATA_FOLDER: bool = os.getenv('APP_DATA_FOLDER', tempfile.gettempdir())

# Setup SQL_LITE
SQL_LITE_DATABASE_FILE: str = 'local.db'
SQL_LITE_DATABASE_FOLDER: str = os.path.abspath(APP_DATA_FOLDER)
SQL_LITE_DATABASE_PATH: str = \
    f'{SQL_LITE_DATABASE_FOLDER}/{SQL_LITE_DATABASE_FILE}'
SQL_LITE_DATABASE_CONNECTION_URI: str = f'sqlite:///{SQL_LITE_DATABASE_PATH}'

# Setup Sqlalchemy
SQLALCHEMY_REBUILD: bool = to_bool(os.getenv('SQLALCHEMY_REBUILD', 'True'))
SQLALCHEMY_DATABASE_URI: str = SQL_LITE_DATABASE_CONNECTION_URI \
    if environment_is_local() else os.getenv('SQLALCHEMY_DATABASE_URI')
SQLALCHEMY_TRACK_MODIFICATIONS: bool = to_bool(
    os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', 'False'))
