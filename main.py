from flask import Flask
import os 
from init import db, ma, bcrypt,jwt 
from controllers.cli_controller import db_commands
from controllers.reservation_controller import reservations_bp
from controllers.invoice_controller import invoices_bp
from controllers.hotel_controller import hotels_bp
from controllers.room_controller import rooms_bp
from marshmallow.exceptions import ValidationError

# create flask app
def create_app():
    app = Flask(__name__)
#  The order of the keys in the JSON response is set to unsorted
    app.json.sort_keys = False
# The database connection information and the secret key used to sign the JSON Web Token are retrieved from environment variables and set
    app.config["SQLALCHEMY_DATABASE_URI"]=os.environ.get("DATABASE_URL")
    app.config["JWT_SECRET_KEY"]=os.environ.get("JWT_SECRET_KEY")

# Decorators are defined for error handling when a ValidationError occurs in the app
    @app.errorhandler(ValidationError)
    def validation_error(err):
        return{'error':err.messages}, 400
    
    
    @app.errorhandler(400)
    def bad_request(err):
        return {'error':str(err)}, 400
    
    @app.errorhandler(404)
    def not_found(err):
        return {'error':str(err)}, 404
        
    
    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

# set up blueprints 
    app.register_blueprint(db_commands)
    app.register_blueprint(reservations_bp)
    app.register_blueprint(invoices_bp)
    app.register_blueprint(hotels_bp)
    app.register_blueprint(rooms_bp)
    
    return app