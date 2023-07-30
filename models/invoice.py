from init import db, ma 
from marshmallow import fields
from marshmallow.validate import OneOf, Length, Range

class Invoice(db.Model):
    __tablename__ = 'invoices'
    invoice_id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer)
    payment_date = db.Column(db.Date) # Date created
    payment_method = db.Column(db.String)
    description = db.Column(db.Text)
    
    reservation_id = db.Column(db.Integer, db.ForeignKey('reservations.reservation_id'), nullable = False)
    
    
    reservation = db.relationship('Reservation', back_populates = 'invoices')
    
class InvoiceSchema(ma.Schema):
    reservation = fields.Nested('ReservationSchema', exclude= ['password','number_of_guests', 'email', 'phonenumber'])
    payment_method = fields.String(required = True, validate=OneOf(['creditcard', 'debitcard']), error='We accept credit or debit card payment')
    description = fields.String(required =True, validate=Length(min=20, error='Description must be at least 2 characters long'))
    amount = fields.Integer(requred = True,validate=Range(min=1, error = 'amount must be greater than 0'))
    fields = ('invoice_id', 'amount', 'payment_date', 'payment_method', 'reservation')
    ordered = True

invoice_schema = InvoiceSchema()
invoices_schema = InvoiceSchema(many = True)