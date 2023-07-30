from init import db, ma
from marshmallow import fields
from marshmallow.validate import Length

# reservation model equivalent to a table by using SQLALchemy
class Reservation(db.Model):
    __tablename__ = 'reservations'
# attributes for reservations_table
    reservation_id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String, nullable=False)
    lastname = db.Column(db.String, nullable=False)
    phonenumber = db.Column(db.Integer, nullable=False, unique=True)
    email = db.Column(db.String)
    check_in_date = db.Column(db.Integer, nullable=False)
    check_out_date = db.Column(db.Integer, nullable=False)
    number_of_guests = db.Column(db.Integer, nullable=False)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    invoices = db.relationship('Invoice', back_populates = 'reservation', cascade='all, delete')
    rooms = db.relationship('Room', back_populates = 'reservation', cascade='all, delete')

# fields marshmallo to convert 
class ReservationSchema(ma.Schema):
    number_of_guests = fields.Integer(required = True, validate=Length(max=4, error='the hotel is allowed to sleep up to 4 guests to a room'))
    invoices = fields.List(fields.Nested('InvoiceSchema', exclude=['reservation']))
    rooms = fields.List(fields.Nested('RoomSchema', exclude=['reservation']))
    class Meta:
        fields = ('reservation_id', 'firstname', 'lastname', 'phonenumber', 'email', 'check_in_date', 'check_out_date', 'number_of_guests', 'password','is_admin', 'invoices', 'rooms')
        ordered = True
        
reservation_schema = ReservationSchema(exclude=['password']) 
reservations_schema = ReservationSchema(many=True, exclude=['password'])