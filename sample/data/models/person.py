""" Person
"""
from sqlalchemy import BigInteger, Column, Integer, String

from .model import AuditModel


class Person(AuditModel): #pylint: disable=too-few-public-methods
    """ Person Entity

        .. note::
            Because we use inheritance we have the all the audit model fields
            added, we just need to add the other columns not part of audit
    """
    __tablename__ = "person"
    id: Column = Column(
        BigInteger().with_variant(Integer, "sqlite"),
        primary_key=True,
        nullable=False
    )
    first_name: Column = Column(String(100), nullable=False)
    middle_name: Column = Column(String(100), nullable=True)
    last_name: Column = Column(String(100), nullable=False)

    def __init__(
            self,
            first_name: str = None,
            last_name: str = None,
            middle_name: str = None) -> None:

        self.first_name = first_name
        self.last_name = last_name
        self.middle_name = middle_name
        self.active = True
