""" Person Endpoint
"""
import logging

from http import HTTPStatus
from flask import request
from flask_restplus import Resource
from ..restplus import api, name_space
from ..swagger import api_model_factory

from ...data.access import PersonAccess
from ...data.models import Person
from ..authentication import user_id, token_validation

ENTITY = api_model_factory.get_entity(Person.__tablename__)
NAME_SPACE = name_space(Person.__tablename__)

@NAME_SPACE.route('')
@NAME_SPACE.response(401, "Unauthorized") # Tell Users endpoint is protected.
class PersonCollection(Resource):
    """ PersonCollection
    """
    log = logging.getLogger(__name__)
    person_access: PersonAccess = PersonAccess()

    @token_validation # Protects the endpoint
    @api.marshal_list_with(ENTITY)
    def get(self):
        """
        Returns list of persons.
        """
        return self.person_access.get(), HTTPStatus.OK

    @token_validation # Protects the endpoint
    @api.response(HTTPStatus.CREATED, 'Created person')
    @api.expect(ENTITY)
    def post(self):
        """ Creates a new person
        """
        return self.person_access.create(user_id(), request.json), HTTPStatus.CREATED


@NAME_SPACE.route('/<int:id>')
@NAME_SPACE.response(404, "Could not find person")
@NAME_SPACE.response(401, "Unauthorized")
class PersonItem(Resource):
    """ PersonItem
    """
    log = logging.getLogger(__name__)
    person_access: PersonAccess = PersonAccess()

    @token_validation
    @api.marshal_list_with(ENTITY)
    @api.response(HTTPStatus.NOT_FOUND, 'Cant find person')
    def get(self, id: int):
        """ Returns a single person.
        """
        return self.person_access.get(id), HTTPStatus.OK

    @token_validation
    @api.response(HTTPStatus.NO_CONTENT, 'Update classed person information')
    @api.expect(ENTITY)
    def put(self, id):
        """ Updates a person
        """
        self.person_access.update(
            user_id=user_id(),
            entity_id=id,
            data=request.json)
        return None, HTTPStatus.NO_CONTENT

    @api.response(HTTPStatus.NO_CONTENT, 'Deleted person information')
    def delete(self, id):
        """ Delete a new person
        """
        self.person_access.delete(user_id(), id)
        return None, HTTPStatus.NO_CONTENT
