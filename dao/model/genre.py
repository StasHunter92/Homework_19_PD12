from marshmallow import Schema, fields

from utils.setup_db import db


# ----------------------------------------------------------------------------------------------------------------------
# Genre model for database
class Genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


# ----------------------------------------------------------------------------------------------------------------------
# Schema for genre model
class GenreSchema(Schema):
    id = fields.Int()
    name = fields.Str()
