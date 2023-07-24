from init import db, ma 
from marshmallow import fields

class Invoice(db.Model):
    __tablename__ = 'invoices'
    invoice_id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float)
    payment_date = db.Column(db.Date) # Date created
    payment_method = db.Column(db.String)
    description = db.Column(db.Text)
    
    reservation_id = db.Column(db.Integer, db.ForeignKey('reservations.reservation_id'), nullable = False)
    
    
    reservation = db.relationship('Reservation', back_populates = 'invoices')
    
class InvoiceSchema(ma.Schema):
    reservation = fields.Nested('ReservationSchema', exclude= ['password','number_of_guests', 'email', 'phonenumber'])
    
    class Meta:
        fields = ('invoice_id', 'amount', 'payment_date', 'payment_method', 'reservation')
        ordered = True

invoice_schema = InvoiceSchema()
invoices_schema = InvoiceSchema(many = True)