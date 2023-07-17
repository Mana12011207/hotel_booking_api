from flask import Blueprint
from init import db, bcrypt
from models.reservation import Reservation


db_commands = Blueprint('db',__name__)

@db_commands.cli.command('create')
def create_all():
    db.create_all()
    print("Tables Created")
    

@db_commands.cli.command('drop')
def drop_all():
    db.drop_all()
    print("Tables dropped")

@db_commands.cli.command('seed')
def seed_db():
    reservations = [
        Reservation(
            firstname = 'Tayler',
            lastname = 'Swift',
            phonenumber = '1234567',
            check_in_date = '01012022',
            check_out_date = '03012022',
            number_of_guests = '2',
            password = bcrypt.generate_password_hash('tayler1').decode('utf-8')
        ),
            Reservation (
            firstname = 'Miranda',
            lastname = 'Kerr',
            phonenumber = '1355791',
            check_in_date = '01022022',
            check_out_date = '03022022',
            number_of_guests = '2',
            email = 'miranda@email.com',
            password = bcrypt.generate_password_hash('miranda2').decode('utf-8')
            ),
    ]
    
    db.session.add_all(reservations)
    db.session.commit()
    
    print("Tables seeded")