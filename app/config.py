class Config:
    SECRET_KEY = 'your_secret_key_here'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///main.db'
    SQLALCHEMY_BINDS = {
        'users': 'sqlite:///users.db',
        'cars': 'sqlite:///cars.db',
        'bookings': 'sqlite:///bookings.db',
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False
