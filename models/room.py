from init import db, ma
from marshmallow import fields


class Room(db.Model):
    __tablename__ = 'rooms'
    room_id = db.Column(db.Integer, primary_key=True)
    room_name =db.Column(db.String, nullable=False)
    bed_type = db.Column(db.String)
    description = db.Column(db.text)
    
    reservation_id = db.Column(db.Integer, db.ForeignKey('reservations.reservation_id'), nullable=False)
    hotel_id = db.Column(db.Integer. db.ForeignKey('hotels.hotel_id'), nullable = False)

    reservation = db.relationship('Reservation', back_populates = 'rooms')
    hotel = db.relationship('Hotel', back_ppopulates = 'rooms') 
    

class RoomSchema(ma.Schema):
    reservation = fields.Nested('ReservationSchema', exclude = 'password' )
    hotel = fields.Nested('HotelSchema')
    
    class Meta:
        fields = ('room_id', 'room_name', 'bed-type', 'description', 'hotel', 'reservation')
room_schema = RoomSchema()
rooms_schema = RoomSchema(many=True)
