""" Abstract models to help minimize the work needed to create
    sqlalchemy Models for the database
"""
from sqlalchemy import BigInteger, Boolean, Column, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declared_attr

from .. import db


class Model(db.Model):  # pylint: disable=too-few-public-methods
    """ Place any code that all models
        share or will inherit
    """
    __abstract__ = True


class AuditModel(Model):  # pylint: disable=too-few-public-methods
    """ Audit entity fields, theses fields should be on every table.
    """
    __abstract__ = True
    active: Column = Column(Boolean, nullable=False)

# """
#     Deactivate column, this bit is a soft delete where the record is no
#     longer active but still available for audit"""
    @declared_attr
    def created_by_id(self):
        """ method is used to create a ForeignKey in an abstract class in sqlalchemy
        """
        return Column(BigInteger, ForeignKey('person.id'), nullable=False)
# """
#         Created by is who created the row and links back, Foreign
#         Key (FK) to a person.

#         Note: you will have to bootstrap a System/Operator person row else other.
#         """
    created_on: Column = Column(DateTime, nullable=False)
