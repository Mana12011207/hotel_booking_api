from flask import Flask
import os 
from init import db, ma, bcrypt,jwt 
from controllers.cli_controller import db_commands
from controllers.reservation_controller import reservation_bp
from controllers.invoice_controller import invoices_bp
from controllers.hotel_controller import hotels_bp

def create_app():
    app = Flask(__name__)
    
    app.json.sort_keys = False
    
    app.config["SQLALCHEMY_DATABASE_URI"]=os.environ.get("DATABASE_URL")
    app.config["JWT_SECRET_KEY"]=os.environ.get("JWT_SECRET_KEY")
    
    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    
    app.register_blueprint(db_commands)
    app.register_blueprint(reservation_bp)
    app.register_blueprint(invoices_bp)
    app.register_blueprint(hotels_bp)
    
    return app