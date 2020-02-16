""" Application configuration
"""
import os
from logging import Logger
from flask import Flask, Blueprint
from flask_cors import CORS

from . import settings
from .data import db
from .api.restplus import api
application: Flask = Flask(__name__)

logger: Logger = settings.get_logger(__name__)

logger.info('>>>>>ENABLING CORS <<<<<')
CORS(application, resources={r"/api/*": {"origins": "*"}})


def settings_to_config(flask_application: Flask) -> Flask:
    """ Maps settings to the flask application config

        :param flask.Flask flask_application:

        :return: modifed flask application
        :rtype: flask.Flask
    """

    flask_application.config['APPLICATION_PORT'] = settings.APPLICATION_PORT
    flask_application.config['APPLICATION_BIND'] = settings.APPLICATION_BIND
    flask_application.config['FLASK_DEBUG'] = settings.FLASK_DEBUG

    flask_application.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI
    flask_application.config['SQLALCHEMY_REBUILD'] = settings.SQLALCHEMY_REBUILD
    flask_application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = \
        settings.SQLALCHEMY_TRACK_MODIFICATIONS
    flask_application.config['SWAGGER_UI_DOC_EXPANSION'] = \
        settings.REST_PLUS_SWAGGER_UI_DOC_EXPANSION
    flask_application.config['RESTPLUS_VALIDATE'] = settings.REST_PLUS_VALIDATE
    flask_application.config['RESTPLUS_MASK_SWAGGER'] = settings.REST_PLUS_MASK_SWAGGER
    flask_application.config['ERROR_404_HELP'] = settings.REST_PLUS_ERROR_404_HELP

    flask_application.config['APP_DATA_FOLDER'] = settings.APP_DATA_FOLDER
    flask_application.config['CORS_ORIGIN'] = settings.CORS_ORIGIN
    flask_application.config['SQL_LITE_DATABASE_FILE'] = settings.SQL_LITE_DATABASE_FILE
    flask_application.config['SQL_LITE_DATABASE_FOLDER'] = settings.SQL_LITE_DATABASE_FOLDER
    flask_application.config['SQL_LITE_DATABASE_PATH'] = settings.SQL_LITE_DATABASE_PATH
    flask_application.config['LOCAL'] = settings.environment_is_local()
    flask_application.config['TITLE'] = settings.TITLE
    flask_application.config['FLASK_URL_PREFIX'] = settings.FLASK_URL_PREFIX

    return flask_application


def arguments_to_config(flask_application: Flask, **kwargs) -> Flask:
    """ Override settings with arguments

        :param flask.Flask flask_application:
        :return: modifed flask application
        :rtype: flask.Flask
    """
    for key, value in kwargs.items():
        flask_application.config[key] = value
    return flask_application


def touch(path: str) -> None:
    """ This is needed for windows as windows
        has no touch command

        :param str path: path to file that will be "touched"
        :return: None
        :rtype: None
    """
    with open(path, 'a'):
        os.utime(path, None)


def initialize_api(flask_application: Flask) -> Flask:
    """
        flask.Flask flask_application: starting context to add blueprint
            too.
        :return: modifed flask_application with blueprints added
        :rtype: Flask
    """
    if flask_application.config['TITLE'] not in flask_application.blueprints.keys():
        blueprint: Blueprint = Blueprint(
            flask_application.config['TITLE'],
            __name__, url_prefix=flask_application.config['FLASK_URL_PREFIX'])
        from .api import endpoints  # pylint: disable=unused-import,import-outside-toplevel
        api.init_app(blueprint)
        flask_application.register_blueprint(blueprint)
    return flask_application


def initialize_database(flask_application: Flask) -> Flask:
    """ Create a database sqlite file in persistant mode

        :param flask.Flask flask_application: this is where SQLAlchemy context
            will be bound to.
        :param bool rebuild: this will erase the data base and rebuild off of
            models, this is some times called code first generation.
    """
    with flask_application.app_context():
        from .data import models  # pylint: disable=import-outside-toplevel
        db.init_app(flask_application)

        if flask_application.config['SQLALCHEMY_REBUILD']:
            db.drop_all()
            db.create_all()
            from .data.access import DatabaseAccess  # pylint: disable=import-outside-toplevel
            person = models.Person('System', 'System', 'System')
            dal = DatabaseAccess(models.Person)
            dal.audit_create(1, person)
            dal.save(person)

    return flask_application


def initialize_local_data(flask_application: Flask) -> Flask:
    """ This setups up data in local mode
    """
    logger.info('>>>>>Initializing Local Data<<<<<')
    db_folder = flask_application.config['SQL_LITE_DATABASE_FOLDER']
    db_path = flask_application.config['SQL_LITE_DATABASE_PATH']

    # Check if directory is created
    os.makedirs(db_folder, exist_ok=True)
    # Make a db file
    touch(db_path)
    # Throw error if no db file, this should only happen if you don't have
    # write permission to the folder
    if not os.path.exists(db_path):
        logger.error("Unable to find sqlite db %s", db_path)
        raise SystemExit()
    return initialize_database(flask_application)


def initialize_data(flask_application: Flask) -> Flask:
    """ Initialize Database
    """
    logger.info('>>>>>Initializing Data<<<<<')
    if flask_application.config['LOCAL']:
        return initialize_local_data(flask_application)
    return initialize_database(flask_application)


def initialize(flask_application: Flask, **kwargs) -> Flask:
    """ initialize
    """
    logger.info('>>>>>Initializing Application<<<<<')
    flask_application = settings_to_config(flask_application)
    flask_application = arguments_to_config(flask_application, **kwargs)
    flask_application = initialize_data(flask_application)
    flask_application = initialize_api(flask_application)
    return flask_application


def local_main():
    """ For running on local machine Main Method
    """
    logger.info(">>>>>MAIN<<<<<")
    flask_application = initialize(application)
    bind: str = flask_application.config['APPLICATION_BIND']
    port: int = flask_application.config['APPLICATION_PORT']
    url_prefix: str = flask_application.config['FLASK_URL_PREFIX']
    logger.info("Starting Server http://%s:%s%s", bind, port, url_prefix)
    flask_application.run(
        host=bind,
        port=port,
        debug=flask_application.config['FLASK_DEBUG'])


def main(**kwargs) -> Flask:
    """ Main entry point for application

        :param **kwargs: will be mapped to application.config
    """
    return initialize(application, **kwargs)
