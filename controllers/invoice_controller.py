from flask import Blueprint, request
from init import db
from models.invoice import Invoice, invoice_schema, invoices_schema
from datetime import date
from flask_jwt_extended import get_jwt_identity, jwt_required


invoices_bp = Blueprint('invoices', __name__, url_prefix='/invoices')

@invoices_bp.route('/')
def get_all_invoices():
    stmt = db.select(Invoice).order_by(Invoice.payment_date.desc())
    invoices = db.session.scalars(stmt)
    return invoices_schema.dump(invoices)

@invoices_bp.route('/<int:id>')
def get_one_invoice(id):
    stmt = db.select(Invoice).filter_by(invoice_id = id)
    invoice = db.session.scalar(stmt)
    if invoice:
        return invoice_schema.dump(invoice)
    else :
        return {'error': f'Invoice not found with id {id}'}, 404

@invoices_bp.route('/', methods = ['POST'])
@jwt_required()
def create_invoices():
    body_data = request.get_json()
    # Create a new invoice model instance
    invoice = Invoice(
        amount = body_data.get('amount'),
        description = body_data.get('description'),
        payment_date=date.today(),
        payment_method = body_data.get('payment_method'),
        reservation_id=get_jwt_identity()
    )
    
    # Add that card to the session
    db.session.add(invoice)
    # commit
    db.session.commit()
    #Respond to the client
    return invoice_schema.dump(invoice), 201