from flask import Blueprint, request
from init import db
from models.hotel import Hotel, hotel_schema, hotels_schema
from models.room import Room, room_schema, rooms_schema
from models.reservation import Reservation
from flask_jwt_extended import get_jwt_identity, jwt_required
import functools



#blueprint hotels/hotel_id/rooms is created
rooms_bp = Blueprint('rooms', __name__, url_prefix='/<int:hotel_id>/rooms')

def authorise_as_admin(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        reservation_id = get_jwt_identity()
        stmt = db.select(Reservation).filter_by(reservation_id=reservation_id)
        reservation = db.session.scalar(stmt)
        if reservation.is_admin:
            return fn(*args, **kwargs)
        else:
            return {'error':'Not authoriesd to perform this action'}, 403
    return wrapper 

# decorator is used to define an endpoint to retrieve information on all rooms belonging to a given hotel when a GET request is sent to the /rooms endpoint.
@rooms_bp.route('/')
def get_all_rooms(hotel_id):
    stmt = db.select(Room).filter(Room.hotel_id == hotel_id).order_by(Room.room_id.asc())
    rooms = db.session.execute(stmt).scalars().all()
    return rooms_schema.dump(rooms)

# decorator is used to define an endpoint to retrieve the room information corresponding to the specified hotel and room ID when a GET request is sent to a URL like /rooms/<room_id>. The following information is defined.
@rooms_bp.route('/<int:room_id>')
def get_one_room(hotel_id, room_id):
    stmt = db.select(Room).filter_by(Room.hotel_id == hotel_id, Room.room_id == room_id)
    room = db.session.scalar(stmt)
    if room:
        return room_schema.dump(room)
    else:
        return {'error': f'Room is not found with id {room_id}. Please try with different id'}, 404


@rooms_bp.route('/', methods = ['POST'])
@jwt_required()
@authorise_as_admin
def create_room(hotel_id):
    body_data = room_schema.load(request.get_json())
    stmt = db.select(Hotel).filter_by(hotel_id = hotel_id) # select * from hotels where id = hotel_id
    hotel = db.session.scalar(stmt)
    if hotel :
        room = Room (
            room_name = body_data.get('room_name'),
            bed_type = body_data.get('bed_type'),
            description = body_data.get('description'),
            reservation_id = get_jwt_identity(), 
            hotel=hotel
        )
        db.session.add(room)
        db.session.commit()
        return room_schema.dump(room), 201
    
    
@rooms_bp.route('/<int:room_id>', methods = ['DELETE'])
@jwt_required()
@authorise_as_admin
def delete_room(hotel_id, room_id):
    stmt = db.select(Room).filter_by(room_id = room_id)
    room = db.session.scalar(stmt)
    if room :
        db.session.delete(room)
        db.session.commit()
        return {'message': f'Room {room_id} is deleted successfully'}
    else : 
        return {'error': f'Room is not found with id{room_id}'}, 404
    

@rooms_bp.route('/<int:room_id>', methods = ['PUT','PATCH'])
@jwt_required()
@authorise_as_admin
def update_room(hotel_id, room_id):
    body_data = room_schema.load(request.get_json(), partial = True)
    stmt = db.select(Room).filter_by(room_id=room_id)
    room = db.session.scalar(stmt) # room from database that needs to be updated
    if room:
        # trying to update room_name, bed_type, description field of room
        room.room_name = body_data.get('room_name') or room.room_name
        room.bed_type = body_data.get('bed_type') or room.bed_type
        room.description = body_data.get('description') or room.description
        db.session.commit()
        return room_schema.dump(room)
    else:
        return {'error' :f'Room is not found with id{room_id}. Please try with different id'}, 404
    
