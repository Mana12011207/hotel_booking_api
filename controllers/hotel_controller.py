from flask import Blueprint, request
from init import db
from models.reservation import Reservation
from models.hotel import Hotel, hotel_schema, hotels_schema
from flask_jwt_extended import get_jwt_identity, jwt_required
from .room_controller import  rooms_bp
import functools

# since room_controller is the same level of hotel_controller in the directory so '.'is the need in front of the controller
hotels_bp = Blueprint('hotels', __name__, url_prefix='/hotels')
hotels_bp.register_blueprint(rooms_bp)


# The decorator function authorise_as_admin is defined to authorise a specific action as admin.
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

# The @hotels_bp.route('/') decorator is used to define an endpoint to retrieve information about all hotels when a GET request is sent to the /hotels endpoint.
@hotels_bp.route('/')
def get_all_hotels():
    stmt = db.select(Hotel).order_by(Hotel.hotel_id.asc())
    hotels = db.session.scalars(stmt)
    return hotels_schema.dump(hotels)

# decorator is used to define an endpoint to retrieve information about the hotel with the specified ID when a GET request is sent to a URL like /hotels/<id>.
@hotels_bp.route('/<int:id>')
def get_one_hotel(id):
    stmt = db.select(Hotel).filter_by(hotel_id=id)
    hotel = db.session.scalar(stmt)
    if hotel:
        return hotel_schema.dump(hotel)
    else:
        return {'error': f'Hotel is not found with id {id}. Please try other ids'}, 404


@hotels_bp.route('/', methods=['POST'])
@jwt_required()
@authorise_as_admin
def create_hotels():
    body_data = hotel_schema.load(request.get_json())
    # Create a new hotel model instance
    hotel = Hotel(
        hotel_name = body_data.get('hotel_name'),
        city = body_data.get('city'),
        description = body_data.get('description'),
        review = body_data.get('review')
    )
    # add hotel to the session
    db.session.add(hotel)
    # commit
    db.session.commit()
    # respond to the client
    return hotel_schema.dump(hotel), 201


# @hotels_bp.route('/<int:id>', methods=['DELETE']) decorator is used to define an endpoint for deleting hotels with a given ID when a DELETE request is sent to a URL like /hotels/<id>. The following table shows the endpoints.
@hotels_bp.route('/<int:id>', methods = ['DELETE'])
@jwt_required()
@authorise_as_admin
def delete_one_hotel(id):
    stmt = db.select(Hotel).filter_by(hotel_id = id)
    hotel = db.session.scalar(stmt)
    if hotel:
        db.session.delete(hotel)
        db.session.commit()
        return {'message': f'Hotel{hotel.hotel_id} is deleted successfully' }
    else:
        return {'error': f'Hotel is not found with id {id}. Please try with different id again'}
    
    
# decorator to update the hotel with the given ID when a PUT or PATCH request is sent to a URL like /hotels/<id>. Defining endpoints.
@hotels_bp.route('/<int:id>', methods = ['PUT', 'PATCH'])
@jwt_required()
@authorise_as_admin
def update_one_hotel(id):
    body_data = hotel_schema.load(request.get_json(),partial = True )
    stmt = db.select(Hotel).filter_by(hotel_id = id)
    hotel = db.session.scalar(stmt)
    if hotel :
        hotel.hotel_name = body_data.get('hotel_name') or hotel.hotel_name
        hotel.description = body_data.get('description') or hotel.description
        return hotel_schema.dump(hotel)
    else:
        return {'error':f'Hotel is not found with id{id}. Please try different id'}, 404
