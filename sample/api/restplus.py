""" Api Creation
"""
import logging
from http import HTTPStatus
from flask_restplus import Api, Namespace
from werkzeug.exceptions import Unauthorized
from sqlalchemy.orm.exc import NoResultFound
from .. import __version__
log = logging.getLogger(__name__)

authorizations = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    },
}

api: Api = Api(
    version=__version__,
    title='Flask Sample API',
    default='status',
    default_label='Checking the default status of application',
    description='Rest Api for Sample',
    security='Bearer Auth',
    authorizations=authorizations)


def format_uri(entity_name: str) -> str:
    """ Format url from entity name.
        :param str entity_name:
        :return: string with uri style format.
        :rtype: Flask
    """
    return entity_name.replace('_', '/')


def explode_entity_name(entity_name: str) -> str:
    """ replaces _ with space
    """
    return entity_name.replace('_', ' ')


def name_space(entity_name) -> Namespace:
    """ Get a formatted namespace.
        Multiple words will be delimited with slashes

        :param str entity_name:
        :return: Name space for a given end point
        :rtype: flask_restplus.Namespace
    """
    return api.namespace(
        format_uri(entity_name),
        description=f'Operations related to {explode_entity_name(entity_name)}')


@api.errorhandler
def default_error_handler(e):
    """ By default all errors will be handeled here
    """
    message = 'An Unhandled exception has occurred'
    log.exception(e)
    log.exception(message)
    return {'message': e}, 500


@api.errorhandler(NoResultFound)
def database_not_found_error_handler(e):
    """ Database not found
    """
    log.debug(e)
    return {'message': 'A database result was not found'}, HTTPStatus.NOT_FOUND


@api.errorhandler(Unauthorized)
def unauthorized_error_handler(e):
    """ Unauthorized Exception thrown
    """
    log.warning(
        "Unauthorized access attempt has been made on the system %s",
        str(e))
    return None, HTTPStatus.UNAUTHORIZED
