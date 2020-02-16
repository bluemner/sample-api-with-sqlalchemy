""" Data Access Types
"""

from abc import ABC
from datetime import date, datetime

from dateutil import parser
from sqlalchemy.orm.exc import NoResultFound

from .. import db
from ..models import Model


class DataAccess(ABC):  # pylint: disable=too-few-public-methods
    """
        Abstract class that diffrent data acccess types will extend.

        Examples:
            Database
            File
            AWS - S3
            AWS - SNS
            Apache - Kafka
            Etc...

        The point of a Data Access is to create an abastact layer that will be
        used to hide what underlying storage is used.
    """


class DatabaseAccess(DataAccess):
    """ Database Access
    """

    def __init__(
            self,
            model: Model = None):
        self.model = model

    def get(self, entity_id: int = None):
        """ Here
        """
        result = self.model.query.filter(self.model.id == entity_id).first() \
            if entity_id else self.model.query.all()
        if not result and entity_id:
            raise NoResultFound()

        return result

    def dict_to_entity(self, entity: Model, data: dict) -> None:
        """ Implement the conversion needed from
            dict to entity, entity will need to be
            mutated
            entity is mutable,
                entity.<field> = data['field']
        """
        for column in entity.__table__.columns:
            field: str = column.name
            print(column)
            if field in dir(Model) or field == 'id':
                continue
            python_type: type = column.type.impl.python_type \
                if hasattr(column.type, 'impl') else column.type.python_type
            if field not in data.keys():
                continue
            value = data[field]
            if python_type is datetime or python_type is date:
                if value:
                    value = parser.parse(str(value))
            setattr(entity, field, value)

    def create(self, user_id: int, data: dict):
        """ Create
        """
        entity = self.model()
        self.dict_to_entity(entity, data)
        self.audit_create(user_id, entity)
        self.save(entity)
        return self.model.query.filter(self.model.id == entity.id).first()

    def update(self, user_id: int, entity_id: int, data: dict) -> Model:
        """ update entity based on entity_id
        """
        entity = self.model.query.filter(self.model.id == entity_id).first()
        if not entity:
            raise NoResultFound()
        self.dict_to_entity(entity, data)
        self.audit_modify(user_id, entity)
        self.save(entity)

    def delete(self, user_id: int, entity_id: int, persistant=True):
        """ Delete
        """
        if persistant:
            self.persistant_delete(user_id, entity_id)
        else:
            self.non_persistant_delete(user_id, entity_id)

        return self.non_persistant_delete(user_id, entity_id)

    def persistant_delete(self, user_id: int, entity_id: int) -> Model:
        """ Changes the active record to active
        """
        entity = self.model.query.filter(self.model.id == entity_id).first()
        self.audit_modify(user_id, entity)
        entity.active = False
        self.save(entity)
        return entity

    def non_persistant_delete(self, user_id: int, entity: Model):
        """ This method will need to be implemented with necessary
            recursion
        """
        raise Exception("Not Implemented")

    def audit_create(self, user_id: int, entity: Model) -> None:
        """ Sets the correct 'created on' fields on entity
        """
        entity.created_by_id = user_id
        entity.active = True
        entity.created_on = datetime.now()
        self.audit_modify(user_id, entity)

    def audit_modify(self, user_id: int, entity: Model) -> None:
        """ Sets the correct modifed fields on entity
        """
        entity.modified_by_id = user_id
        entity.modified_on = datetime.now()

    def save(self, entity: Model) -> Model:
        """ Save the entity to database
        """
        db.session.add(entity)  # pylint: disable=E1101
        db.session.commit()  # pylint: disable=E1101
        return entity
