from flask import Blueprint, request
from init import db, bcrypt
from models.reservation import Reservation, reservation_schema, reservations_schema
from flask_jwt_extended import create_access_token
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from datetime import timedelta

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


# register is post method instead of get because we do not want to create but need to send extra data we normally use post 
@auth_bp.route('/register', methods=['POST'])
def auth_register():
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
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return{'error' : 'Phone number already in use'}, 409
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return{'error' : f'Please enter {err.orig.diag.column_name}' }, 409
        

@auth_bp.route('/login', methods=['POST'])
def auth_login():
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

        
        