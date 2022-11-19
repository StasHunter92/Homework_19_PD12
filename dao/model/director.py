from marshmallow import Schema, fields

from utils.setup_db import db


# ----------------------------------------------------------------------------------------------------------------------
# Director model for database
class Director(db.Model):
    __tablename__ = 'director'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


# ----------------------------------------------------------------------------------------------------------------------
# Schema for director model
class DirectorSchema(Schema):
    id = fields.Int()
    name = fields.Str()
