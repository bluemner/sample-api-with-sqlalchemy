"""
    Here is where the models for flask-restplus get loaded

    .. note::
        1) api_model_factory should be loaded first so you can use in other file
        2) Don't mode api_model_factory into this __init__ file as this may
           interfer with the call stack and load before the database is ready

"""
from .factory import api_model_factory
from .status import STATUS
