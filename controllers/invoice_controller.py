from flask import Blueprint, request
from init import db
from models.invoice import Invoice, invoice_schema, invoices_schema
from models.reservation import Reservation
from datetime import date
from flask_jwt_extended import get_jwt_identity, jwt_required
import functools

invoices_bp = Blueprint('invoices', __name__, url_prefix='/invoices')

def authorise_as_admin(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        reservation_id = get_jwt_identity()
        stmt = db.select(Reservation).filter_by(reservation_id=reservation_id)
        reservation = db.session.scalar(stmt)
        if reservation.is_admin:
            return fn(*args, **kwargs)
        else:
            return {'error':'Not authoriesd to perform this action'}, 403
    return wrapper 


@invoices_bp.route('/')
@jwt_required()
@authorise_as_admin
def get_all_invoices():
    is_admin = authorise_as_admin()
    if not is_admin:
        return{'error': 'Not authorised to access invoices'}, 403
    stmt = db.select(Invoice).order_by(Invoice.payment_date.desc())
    invoices = db.session.scalars(stmt)
    return invoices_schema.dump(invoices)

@invoices_bp.route('/<int:id>')
@jwt_required()
def get_one_invoice(id):
    stmt = db.select(Invoice).filter_by(invoice_id = id)
    invoice = db.session.scalar(stmt)
    if invoice:
        return invoice_schema.dump(invoice)
    else :
        return {'error': f'Invoice is not found with id {id}'}, 404


@invoices_bp.route('/', methods = ['POST'])
@jwt_required()
@authorise_as_admin
def create_invoices():
    body_data = invoice_schema.load(request.get_json())
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

@invoices_bp.route('/<int:id>', methods =['DELETE'])
@jwt_required()
@authorise_as_admin
def delete_one_invoice(id):
    stmt = db.select(Invoice).filter_by(invoice_id = id)
    invoice = db.session.scalar(stmt)
    if invoice:
        db.session.delete(invoice)
        db.session.commit()
        return {'message': f'Invoice {invoice.invoice_id} is deleted successfully'}
    else :
        return {'error' : f'Invoice is not found with id{id}. Please try with different id again'}, 404


@invoices_bp.route('/<int:id>', methods = ['PUT','PATCH'])
@jwt_required()
@authorise_as_admin
def update_one_invoice(id):
    is_admin = authorise_as_admin()
    if not is_admin:
        return{'error': 'Not authorised to update invoices'}, 403
    body_data = invoice_schema.load(request.get_json())
    stmt = db.select(Invoice).filter_by(invoice_id = id)
    invoice = db.session.scalar(stmt)
    if invoice:
        invoice.amount = body_data.get('amount') or invoice.amount
        invoice.description = body_data.get('description') or invoice.description
        db.session.commit()
        return invoice_schema.dump(invoice)
    else:
        return {'error': f'Invoice is not found with Invoice_id{id}'}, 404


