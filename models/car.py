from app import db

class Car(db.Model):
    __bind_key__ = 'cars'
    __tablename__ = 'car'

    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    seating_capacity = db.Column(db.Integer, nullable=False)
    transmission = db.Column(db.String(50), nullable=False)
    fuel_type = db.Column(db.String(50), nullable=False)
    price_per_day = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(500))
    description = db.Column(db.Text)
    year = db.Column(db.Integer, nullable=False)
    available = db.Column(db.String(30), nullable=False)

