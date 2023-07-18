from flask import Blueprint, request
from init import db
from models.invoice import Invoice, invoice_schema, invoices_schema


invoices_bp = Blueprint('invoices', __name__, url_prefix='/invoices')

@invoices_bp.route('/')
def get_all_invoices():
    stmt = db.select(Invoice).order_by(Invoice.payment_date.desc())
    invoices = db.session.scalars(stmt)
    return invoices_schema.dump(invoices)