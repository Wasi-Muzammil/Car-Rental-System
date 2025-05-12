# Register all blueprints here for convenience

from .main_routes import main_bp
from .car_routes import car_bp
from .admin_routes import admin_bp
from .payment_routes import payment_bp
from .auth_routes import auth_bp


all_blueprints = [main_bp, auth_bp, car_bp, admin_bp, payment_bp]
