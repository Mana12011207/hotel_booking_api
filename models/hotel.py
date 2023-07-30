from init import db, ma 
from marshmallow import fields
from marshmallow.validate import Length, NoneOf
class Hotel(db.Model):
    __tablename__ = 'hotels'
    # attributes for hotels_table 
    hotel_id = db.Column(db.Integer, primary_key = True)
    hotel_name = db.Column(db.String)
    city = db.Column(db.String)
    description = db.Column(db.Text)
    review = db.Column(db.Text)
    rooms = db.relationship('Room', back_populates = 'hotel', cascade = 'all,delete')
    
# defines the hotelschema class, which is a marshmallow schema for serialising information from hotel model    
class HotelSchema(ma.Schema):
    description = fields.String(required = True, validate=Length(min=20, error='description must be at least 20 characters long'))
    review = fields.String(validate=Length(min=2, error='Review must be at least 2 characters long'))
    hotel_name = fields.String(required = True, validate=NoneOf(["Sydney Hotel", "Melborne Hotel", "Cairns Hotel"], error='Hotel name must be unique'))
    city = fields.String(required=True, validate=Length(min=3, error='City must be at least 3 characters '))
    rooms = fields.List(fields.Nested('RoomSchema', exclude = ['hotel']))
    
 # Meta class is used to define meta-information associated with marshmallow schema   
    class Meta:
        fields = ('hotel_id', 'hotel_name', 'city', 'description', 'review','rooms')
        ordered = True
        
# creates an instance of the hotelschema class and used to serialise multipe hotel information in a list format
hotel_schema = HotelSchema()
hotels_schema = HotelSchema(many=True)