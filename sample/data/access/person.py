""" Person data operations
"""
from .accessible import DatabaseAccess
from ..models import Person


class PersonAccess(DatabaseAccess):
    """ Data Access for a person

        .. note::
            Due to the nature of inheritance from DatabaseAccess we have
            basic crud operations implemented

    """

    def __init__(self):
        super().__init__(model=Person)
