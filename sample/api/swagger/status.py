""" Status swagger documentation
"""
from flask_restplus import fields
from ..restplus import api

STATUS_SCHEMA = {
    'message': fields.String(
        readOnly=True,
        description='Current Application Status')
}
STATUS = api.model('status', STATUS_SCHEMA)
