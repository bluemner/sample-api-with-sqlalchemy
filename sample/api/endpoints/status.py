""" Status endpoint
"""
import logging
from http import HTTPStatus
from flask_restplus import Resource
from ..restplus import api, name_space
from ..swagger import STATUS

NAME_SPACE = name_space('status')

@NAME_SPACE.route('')
class StatusCollection(Resource):
    """ StatusCollection
    """
    log = logging.getLogger(__name__)
    @api.marshal_list_with(STATUS)
    def get(self):
        """
        Returns the status.
        """
        return {"message":"Online"}, HTTPStatus.OK
