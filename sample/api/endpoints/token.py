
""" Status endpoint
"""
import logging
from http import HTTPStatus
from flask_restplus import Resource
from ..restplus import name_space
from ..authentication import _token_factory
NAME_SPACE = name_space('token')

@NAME_SPACE.route('')
class Token(Resource):
    """
        Jwt Token Operation(s)
    """
    log = logging.getLogger(__name__)
    def get(self):
        """
            Generates a JWT Toke for you to use on protected endpoints
        """
        return {"token": _token_factory.make_token()}, HTTPStatus.OK
