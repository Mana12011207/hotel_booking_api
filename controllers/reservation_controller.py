from flask import Blueprint, request
from init import db, bcrypt
from models.reservation import Reservation, reservation_schema, reservations_schema
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from datetime import timedelta 

reservation_bp = Blueprint('reservation', __name__, url_prefix='/reservation')


# register is post method instead of get because we do not want to create but need to send data to backend 
@reservation_bp.route('/register', methods=['POST'])
def reservation_register():
    try:
# to access body in the postman 
# body_date has the following json data in postman{"firstname": "Ann", "lastname":"Hathaway","phone": "9786533", "check_in_date" : "03042022", "check_out_date" : "06042022","number_of_guests" : "4","password": "ann123"}
        body_data = request.get_json()
    # Create a new reservation model instance from the reservation info
        reservation = Reservation() # Instance of the Reservation class which is in turn a SQLAlchemy model
        reservation.firstname = body_data.get('firstname')
        reservation.lastname = body_data.get('lastname')
        reservation.phonenumber = body_data.get('phonenumber')
        reservation.email = body_data.get('email')
        reservation.check_in_date = body_data.get('check_in_date')
        reservation.check_out_date = body_data.get('check_out_date')
        reservation.number_of_guests = body_data.get('number_of_guests')
        if body_data.get('password'):
            reservation.password = bcrypt.generate_password_hash(body_data.get('password')).decode('utf-8')
        # Add the reservation to the session
        db.session.add(reservation)
        #commit to add the user to the database
        db.session.commit()
        # Respond to the client
        return reservation_schema.dump(reservation), 201
    # sqlalchemy c
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return{'error' : 'Phone number already in use'}, 409
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return{'error' : f'Please enter {err.orig.diag.column_name}' }, 409
        

@reservation_bp.route('/login', methods=['POST'])
def reservation_login():
    body_data = request.get_json()
    # Find the reservation by phonenumber
    stmt = db.select(Reservation).filter_by(phonenumber=body_data.get('phonenumber'))
    reservation = db.session.scalar(stmt)
    #if reservation exists and password is correct
    if reservation and bcrypt.check_password_hash(reservation.password, body_data.get('password')):
        token = create_access_token(identity=str(reservation.reservation_id), expires_delta=timedelta(days=3))
        return {'phonenumber':reservation.phonenumber, 'token': token }
    else:
        return{'error': 'Invalid phonenumber or password'}, 401



@reservation_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_one_reservation(id):
    stmt = db.select(Reservation).filter_by(reservation_id=id)
    reservation = db.session.scalar(stmt)
    if reservation:
        db.session.delete(reservation)
        db.session.commit()
        return {'message' : f'Reservation{reservation.reservation_id} deleted successfully'}
    else : 
        return {'error' : f'Reservation is not found with Reservation_id{id}'}, 404
    
@reservation_bp.route('/<int:id>', methods=['PUT','PATCH'])
@jwt_required()
def update_one_reservation(id):
    body_data = request.get_json()
    stmt = db.select(Reservation).filter_by(reservation_id = id)
    reservation = db.session.scalar(stmt)
    if reservation:
        reservation.number_of_guests = body_data.get('number_of_guest') or reservation.number_of_guests
        reservation.check_in_date = body_data.get('check_in_date') or reservation.check_in_date
        reservation.check_out_date = body_data.get('check_out_date') or reservation.check_out_date
        db.session.commit()
        return reservation_schema.dump(reservation)
    else:
        return {'error': f'Reservation is not found with reservation_id {id}'}, 404