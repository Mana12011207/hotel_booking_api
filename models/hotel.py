from init import db, ma 
from marshmallow import fields

class Hotel(db.Model):
    __tablename__ = 'hotels'
    # attributes for hotels_table 
    hotel_id = db.Column(db.Integer, primary_key = True)
    hotel_name = db.Column(db.String)
    city = db.Column(db.String)
    description = db.Column(db.Text)
    address = db.Column(db.String)
    phone = db.Column(db.Integer)
    
class HotelSchema(ma.Schema):
    class Meta:
        fields = ('hotel_id', 'hotel_name', 'city', 'description', 'address', 'phone')
        ordered = True
        
hotel_schema = HotelSchema()
hotels_schema = HotelSchema(many=True)