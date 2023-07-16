from init import db, ma

class Reservation(db.Model):
    __tablename__ = 'reservations'
    
    reservation_id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String, nullable=False)
    lastname = db.Column(db.String, nullable=False)
    phone = db.Column(db.Integer, nullable=False, unique=True)
    email = db.Column(db.String)
    check_in_date = db.Column(db.Integer, nullable=False)
    check_out_date = db.Column(db.Integer, nullable=False)
    number_of_guests = db.Column(db.Integer, nullable=False)
    password = db.Column(db.String, nullable=False)
    
class ReservationSchema(ma.Schema):
    class Meta:
        fields = ('reservation_id', 'firstname', 'lastname', 'phone', 'email', 'check_in_date', 'check_out_date', 'number_of_guests', 'password')

reservation_schema = ReservationSchema(exclude=['password'])
reservations_shcema = ReservationSchema(many=True, exclude=['password'])