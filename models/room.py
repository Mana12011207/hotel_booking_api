from init import db, ma
from marshmallow import fields
from marshmallow.validate import Length, OneOf


class Room(db.Model):
    __tablename__ = 'rooms'
    room_id = db.Column(db.Integer, primary_key = True)
    room_name = db.Column(db.String, nullable=False)
    bed_type = db.Column(db.String)
    description = db.Column(db.String)
    
    reservation_id = db.Column(db.Integer, db.ForeignKey('reservations.reservation_id'), nullable=False, )
    hotel_id = db.Column(db.Integer, db.ForeignKey('hotels.hotel_id'), nullable=False)
    
    reservation = db.relationship('Reservation', back_populates = 'rooms')
    hotel = db.relationship('Hotel', back_populates='rooms')


class RoomSchema(ma.Schema):
    room_name = fields.String(required = True, validate=Length(min=5, error= 'room_name must be at least 5 characters long'))
    description = fields.String(required = True, validate= Length(min=20, error='description must be at least 20 characters long'))
    bed_type = fields.String(required=True, validate=OneOf(['King', 'queen', 'twin']),  error='bed type must be king, queen or twin')
    reservation = fields.Nested('ReservationSchema', exclude = ['password'])
    hotel = fields.Nested('HotelSchema', only = ['hotel_name'])
    
    class Meta:
        fields = ('room_id', 'room_name', 'bed_type', 'description', 'reservation', 'hotel')

room_schema = RoomSchema()
rooms_schema = RoomSchema(many=True)    

    