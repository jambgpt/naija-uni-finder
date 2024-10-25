# app/models/base.py
from datetime import datetime
from ..extensions import db

class BaseModel(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)