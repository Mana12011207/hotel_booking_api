from flask import Blueprint
from init import db, bcrypt
from models.reservation import Reservation
from models.invoice import Invoice
from datetime import date
from models.hotel import Hotel


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
            phonenumber = '00000000',
            check_in_date = '02022020',
            check_out_date = '02022023',
            number_of_guests = '1',
            password = bcrypt.generate_password_hash('admin123').decode('utf-8')
        ),
        Reservation(
            firstname = 'Tayler',
            lastname = 'Swift',
            phonenumber = '1234567',
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
            amount = '300.50',
            description = 'roomcharge',
            payment_date = date.today(),
            payment_method = 'creditcard',
            reservation = reservations[0]
        ),
        Invoice(
            amount = '500.50',
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
            hotel_name = 'Sydney Hotel',
            city = 'Sydney',
            description = 'Sydney hotel description',
            address = '199 George St, The Rocks NSW',
            phone = '1234567890'
        ),
        Hotel (
            hotel_name = 'Melborne Hotel',
            city = 'Melborne',
            description = 'Melborne hotel description',
            address = '200 Lonsdale St, Melbourne VIC',
            phone = '0987654321'
        ),
        Hotel (
            hotel_name = 'Cairns Hotel',
            city = 'Cairns',
            description = 'Cairns hotel description',
            address = 'Pier Point Rd, Cairns City QLD 4870',
            phone = '121212121'
        )
    ]
    
    db.session.add_all(hotels)
    
    # rooms = [
    #     Room (
    #         room_name = 'Deluxe ciry room',
    #         bed_type = 'King',
    #         description = 'Ideally suited to the modern traveller, these newly remodelled guest rooms are situated on higher floors providing striking view of skyline',
    #         reservation = reservations[1],
    #         hotel = hotels[1]
    #     ),
    #     Room (
    #         room_name = 'Premier full harbour club room',
    #         bed_type = 'king and sofabed',
    #         description = 'the remodelled residential_style corner studio evoke a sense of the city with stunning views',
    #         reservation = reservations[2],
    #         hotel = hotels[2]
    #     ),
    #     Room (
    #         room_name = 'One-bedroom opera club suite',
    #         bed_type = 'king or twin',
    #         description = 'Beautiful parquet floors, timber wall panelling and a palette of soft blues and greys exude sophistication in this luxe suite',
    #         reservation = reservations[3],
    #         hotel = hotels[3]
    #     )
    # ]
    
    # db.session.add_all(rooms)

    db.session.commit()
    

    
    print("Tables seeded")