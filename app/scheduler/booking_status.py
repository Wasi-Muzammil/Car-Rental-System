 
def update_booking_status():
    from app import db
    from app.models.booking import Booking
    from app.models.car import Car
    from app.models.user import User
    from datetime import datetime

    today = datetime.today().date()

    expired_bookings = Booking.query.filter(
        Booking.return_date < today,
        Booking.status == "Booked"
    ).all()

    for booking in expired_bookings:
        booking.status = "Not Booked"

        car = Car.query.get(booking.car_id)
        if car:
            car.available = "Available"

        user = User.query.get(booking.user_id)
        if user:
            user.booking_info = "Not Booked"

    db.session.commit()
    print(f"[Scheduler] {len(expired_bookings)} bookings updated to 'Not Booked'.")
