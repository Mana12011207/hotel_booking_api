from init import db
from marshmallow import fields


class Room(db.Model):
    __tablename__ = 'rooms'
    room_id = db.Column(db.Integer, primary_key = True)
    room_name = db.Column(db.String, nullable=False)
    bed_type = db.Column(db.String)
    description = db.Column(db.String)
    