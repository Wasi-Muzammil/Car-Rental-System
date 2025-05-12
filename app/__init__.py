from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from apscheduler.schedulers.background import BackgroundScheduler
from .config import Config
from . import  scheduler

db = SQLAlchemy()
migrate = Migrate()
scheduler = BackgroundScheduler()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Init extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Import and register blueprints
    from app.routes import all_blueprints
    for bp in all_blueprints:
        app.register_blueprint(bp)

    # === PASS APP TO JOB ===
    from app.scheduler.booking_status import update_booking_status

    def job_with_app_context():
        with app.app_context():
            update_booking_status()

    scheduler.add_job(func=job_with_app_context, trigger='interval', hours=12)
    scheduler.start()

    return app
