""" ApiModelFactory implementation
"""
from flask_restplus_sqlalchemy import ApiModelFactory
from ...data import db
from ..restplus import api
api_model_factory: ApiModelFactory = ApiModelFactory(api=api, db=db)
