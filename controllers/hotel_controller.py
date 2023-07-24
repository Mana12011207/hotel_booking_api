from flask import Blueprint, request
from init import db
from models.hotel import Hotel, hotel_schema, hotels_schema
from flask_jwt_extended import get_jwt_identity, jwt_required


hotels_bp = Blueprint('hotels', __name__, url_prefix='/hotels')


@hotels_bp.route('/')
def get_all_hotels():
    stmt = db.select(Hotel).order_by(Hotel.hotel_id.asc())
    hotels = db.session.scalars(stmt)
    return hotels_schema.dump(hotels)


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
def create_hotels():
    body_data = request.get_json()
    hotel = Hotel(
        hotel_name = body_data.get('hotel_name'),
        city = body_data.get('city'),
        description = body_data.get('description'),
        address = body_data.get('address'),
        phone =  body_data.get('phone')
    )
    db.session.add(hotel)
    db.session.commit()
    return hotel_schema.dump(hotel), 201



@hotels_bp.route('/<int:id>', methods = ['DELETE'])
@jwt_required()
def delete_one_hotel(id):
    stmt = db.select(Hotel).filter_by(hotel_id = id)
    hotel = db.session.scalar(stmt)
    if hotel:
        db.session.delete(hotel)
        db.session.commit()
        return {'message': f'Hotel{hotel.hotel_id} is deleted successfully' }
    else:
        return {'error': f'Hotel is not found with id {id}. Please try with different id again'}
    
    
    
@hotels_bp.route('/<int:id>', methods = ['PUT', 'PATCH'])
@jwt_required()
def update_one_hotel(id):
    body_data = request.get_json()
    stmt = db.select(Hotel).filter_by(hotel_id = id)
    hotel = db.session.scalar(stmt)
    if hotel :
        hotel.hotel_name = body_data.get('hotel_name') or hotel.hotel_name
        hotel.description = body_data.get('description') or hotel.description
        return hotel_schema.dump(hotel)
    else:
        return {'error':f'Hotel is not found with id{id}. Please try different id'}, 404
