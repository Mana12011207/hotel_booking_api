from flask import Blueprint, request
from init import db
from models.room import Room, room_schema, rooms_schema
from flask_jwt_extended import get_jwt_identity, jwt_required



rooms_bp = Blueprint('rooms', __name__, url_prefix='/rooms')


@rooms_bp.route('/')
def get_all_rooms():
    stmt = db.select(Room).order_by(Room.room_id.asc())
    rooms = db.session.scalars(stmt)
    return rooms_schema.dump(rooms)

