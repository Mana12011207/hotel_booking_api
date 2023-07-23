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



    
    

