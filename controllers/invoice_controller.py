from flask import Blueprint, request
from init import db
from models.invoice import Invoice, invoice_schema, invoices_schema
from models.reservation import Reservation
from datetime import date
from flask_jwt_extended import get_jwt_identity, jwt_required
import functools

# A Blueprint object named invoices_bp is created
invoices_bp = Blueprint('invoices', __name__, url_prefix='/invoices')

# The decorator function authorise_as_admin is defined to authorise a specific action as admin.
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

# The @invoices_bp.route('/') decorator is used to define an endpoint to retrieve all invoices accessible only to the administrator when accessing the /invoices endpoint.
@invoices_bp.route('/')
@jwt_required()
@authorise_as_admin
def get_all_invoices():
    stmt = db.select(Invoice).order_by(Invoice.payment_date.desc())
    invoices = db.session.scalars(stmt)
    return invoices_schema.dump(invoices)

# The @invoices_bp.route('/<int:id>') decorator is used to define an endpoint to retrieve the invoice for a given ID when accessing a URL such as /invoices/<id>.
@invoices_bp.route('/<int:id>')
@jwt_required()
def get_one_invoice(id):
    stmt = db.select(Invoice).filter_by(invoice_id = id)
    invoice = db.session.scalar(stmt)
    if invoice:
        return invoice_schema.dump(invoice)
    else :
        return {'error': f'Invoice is not found with id {id}'}, 404

# The @invoices_bp.route('/', methods=['POST']) decorator is used to define an endpoint for creating a new invoice when a POST request is sent to the /invoices endpoint.
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
    # add invoice to the session
    db.session.add(invoice)
    # commit
    db.session.commit()
    #respond to the client
    return invoice_schema.dump(invoice), 201

# @invoices_bp.route('/<int:id>', methods=['DELETE']) decorator to define an endpoint for deleting invoices for a given ID when a DELETE request is sent to the URL /invoices/<id The following is done.
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


