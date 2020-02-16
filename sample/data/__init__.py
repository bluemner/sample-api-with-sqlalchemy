""" Database information and instance
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

__all__ = ['models', 'access']
db: SQLAlchemy = SQLAlchemy()
