from flask import Blueprint
from init import db, bcrypt
from models.reservation import Reservation
from models.invoice import Invoice
from datetime import date
from models.hotel import Hotel
from models.room import Room


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
            firstname = 'admin',
            lastname = 'admin',
            phonenumber = '1234567'  ,
            check_in_date = '01012023',
            check_out_date = '01012026',
            number_of_guests = '1',
            password = bcrypt.generate_password_hash('admin123').decode('utf-8'),
            is_admin = True
        ),
        Reservation(
            firstname = 'Tayler',
            lastname = 'Swift',
            phonenumber = '98075437',
            check_in_date = '01012022',
            check_out_date = '03012022',
            number_of_guests = '2',
            password = bcrypt.generate_password_hash('tayler1').decode('utf-8')
        ),
        Reservation(
            firstname = 'Miranda',
            lastname = 'Kerr',
            phonenumber = '1355791',
            check_in_date = '01022022',
            check_out_date = '03022022',
            number_of_guests = '2',
            email = 'miranda@email.com',
            password = bcrypt.generate_password_hash('miranda2').decode('utf-8')
            ),
        Reservation(
            firstname = 'Ann',
            lastname = 'Hathaway',
            phonenumber = '2346534',
            check_in_date = '04042022',
            check_out_date = '06042022',
            number_of_guests = '4',
            password = bcrypt.generate_password_hash('ann2222').decode('utf-8')
        )
    ]
    
    db.session.add_all(reservations)
    
    invoices = [
        Invoice(
            amount = '300',
            description = 'roomcharge',
            payment_date = date.today(),
            payment_method = 'creditcard',
            reservation = reservations[0]
        ),
        Invoice(
            amount = '500',
            description = 'roomcharge',
            payment_date = date.today(),
            payment_method = 'debitcard',
            reservation = reservations[1]
        ),
        Invoice(
            amount = '1000',
            description = 'roomcharge',
            payment_date = date.today(),
            payment_method = 'creditcard',
            reservation = reservations[2]
        )
    ]
    
    db.session.add_all(invoices)
    
    hotels = [
        Hotel (
            hotel_name = 'sydney hotel',
            city = 'sydney',
            description = 'sydney hotel description',
            review = 'review for sydney hotel'
        ),
        Hotel (
            hotel_name = 'melborne hotel',
            city = 'melborne',
            description = 'melborne hotel description',
            review = 'review for meloborne hotel'
        ),
        Hotel (
            hotel_name = 'cairns hotel',
            city = 'cairns',
            description = 'cairns hotel description',
            review = 'review for carns hotel'
        )
    ]
    
    db.session.add_all(hotels)
    
    rooms = [
        Room (
            room_name = 'deluxe ciry room',
            bed_type = 'king',
            description = 'deluxe city room with description',
            reservation = reservations[0],
            hotel = hotels[0]
        ),
        Room (
            room_name = 'premier full harbour club room',
            bed_type = 'queen',
            description = 'Premier full harbour club room with description',
            reservation = reservations[1],
            hotel = hotels[1]
        ),
        Room (
            room_name = 'opera club suite',
            bed_type = 'twin',
            description = 'opera club suite',
            reservation = reservations[2],
            hotel = hotels[2]
        ),
        Room (
            room_name = 'five star Suite',
            bed_type = 'king',
            description = 'five star suite with description',
            reservation = reservations[2],
            hotel = hotels[2]
        )
    ]
    
    db.session.add_all(rooms)

    db.session.commit()
    
    print("Tables seeded")