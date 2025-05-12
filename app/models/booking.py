from app import db

class Booking(db.Model):
    __tablename__ = 'bookings'
    __bind_key__ = 'bookings'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    car_id = db.Column(db.Integer, nullable=False)
    username = db.Column(db.String(80), nullable=False)
    car_brand = db.Column(db.String(100), nullable=False)
    car_model = db.Column(db.String(100), nullable=False)
    car_category = db.Column(db.String(50), nullable=False)
    car_seating_capacity = db.Column(db.Integer, nullable=False)
    car_transmission = db.Column(db.String(50), nullable=False)
    reservation_date = db.Column(db.Date, nullable=False)
    return_date = db.Column(db.Date, nullable=False)
    total_price = db.Column(db.Integer, nullable=False)
    balance = db.Column(db.Integer, nullable=False)
    rental_duration = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), default="Not Booked")
