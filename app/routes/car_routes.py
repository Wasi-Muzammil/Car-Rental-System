from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from datetime import datetime
from flask.views import MethodView
from app import db
from app.models.car import Car
from app.models.user import User
from app.models.booking import Booking

car_bp = Blueprint('car', __name__)

class CarDetailsView(MethodView):
    """
    Car Details View
    Handles displaying car details and booking functionality.
    
    """
    
    def get(self, car_id):
        try:
            car = Car.query.get_or_404(car_id)
            user_id = session.get('user_id')
            user = db.session.get(User, user_id) if user_id else None
            balance = user.balance if user else None

            return render_template(
                'details page.html',
                car=car,
                price_per_day=car.price_per_day,
                total_price=session.get('total_price'),
                rental_duration=session.get('rental_duration'),
                reservation_date=session.get('reservation_date'),
                return_date=session.get('return_date'),
                booking_success=False,
                balance=balance
            )
        except Exception as e:
            flash("An error occurred while processing your request", "error")
            print(f"Error: {e}")
            return redirect(url_for('car.car_details', car_id=car_id))

    def post(self, car_id):
        try:
            user_id = session.get('user_id')

            # Check at the beginning if user not logged in
            if not user_id:
                flash("User not logged in. Please log in first.", "error")
                return redirect(url_for('car.car_details', car_id=car_id))

            user = db.session.get(User, user_id)
            if not user:
                flash("User not found.", "error")
                return redirect(url_for("car.car_details", car_id=car_id))

            car = Car.query.get_or_404(car_id)
            balance = user.balance

            form_action = request.form.get("form_action")

            reservation_date_str = request.form.get("reservation_date") or session.get("reservation_date")
            return_date_str = request.form.get("return_date") or session.get("return_date")

            if form_action == "calculate_total":
                if not reservation_date_str or not return_date_str:
                    flash("Reservation date and return date are required.", "error")
                    return redirect(url_for('car.car_details', car_id=car_id))

                try:
                    reservation_date = datetime.strptime(reservation_date_str, "%Y-%m-%d").date()
                    return_date = datetime.strptime(return_date_str, "%Y-%m-%d").date()
                except ValueError:
                    flash("Invalid date format. Please use YYYY-MM-DD.", "error")
                    return redirect(url_for('car.car_details', car_id=car_id))

                rental_duration = (return_date - reservation_date).days
                if rental_duration <= 0:
                    flash("Return date must be after reservation date.", "error")
                    return redirect(url_for('car.car_details', car_id=car_id))

                total_price = car.price_per_day * rental_duration

                session['reservation_date'] = reservation_date_str
                session['return_date'] = return_date_str
                session['total_price'] = total_price
                session['rental_duration'] = rental_duration

                flash("Total price calculated successfully!", "success")
                return redirect(url_for('car.car_details', car_id=car_id))

            if form_action == "rent_now":
                existing_booking = Booking.query.filter_by(user_id=user_id, status="Booked").first()
                if existing_booking:
                    flash("You cannot book more than one car at a time.", "error")
                    return redirect(url_for('car.car_details', car_id=car_id))

                if not reservation_date_str or not return_date_str:
                    flash("Please calculate the total before booking.", "error")
                    return redirect(url_for('car.car_details', car_id=car_id))

                reservation_date = datetime.strptime(reservation_date_str, "%Y-%m-%d").date()
                return_date = datetime.strptime(return_date_str, "%Y-%m-%d").date()
                total_price = session.get('total_price')

                if total_price is None or total_price <= 0:
                    flash("Invalid total price. Please recalculate.", "error")
                    return redirect(url_for('car.car_details', car_id=car_id))

                if user.balance >= total_price:
                    user.balance -= total_price

                    new_booking = Booking(
                        user_id=user_id,
                        username=user.username,
                        car_id=car_id,
                        car_brand=car.brand,
                        car_model=car.model,
                        car_category=car.category,
                        car_transmission=car.transmission,
                        car_seating_capacity=car.seating_capacity,
                        reservation_date=reservation_date,
                        return_date=return_date,
                        total_price=total_price,
                        rental_duration=session.get('rental_duration'),
                        balance=user.balance,
                        status="Booked"
                    )
                    db.session.add(new_booking)
                    car.available = "Not Available"
                    user.booking_info = "Booked"
                    db.session.commit()

                    session.pop('reservation_date', None)
                    session.pop('return_date', None)
                    session.pop('total_price', None)
                    session.pop('rental_duration', None)

                    flash("Car booked successfully!", "success")
                else:
                    flash("Insufficient balance.", "error")

                return redirect(url_for('car.car_details', car_id=car_id))

        except Exception as e:
            flash("An error occurred while processing your request.", "error")
            print(f"Error: {e}")
            return redirect(url_for('car.car_details', car_id=car_id))

class BookingHistoryView(MethodView):
    """
    Booking History View
    Handles displaying the booking history of the logged-in user.
    
    """
    
    def get(self):
        user_id = session.get('user_id')
        if not user_id:
            flash("User not logged in", "error")
            return redirect(url_for('main.main'))

        bookings = Booking.query.filter_by(user_id=user_id).all()
        return render_template('booking_history.html', bookings=bookings)

car_bp.add_url_rule(
    '/car/<int:car_id>',
    view_func=CarDetailsView.as_view('car_details')
)
car_bp.add_url_rule(
    '/booking_history',
    view_func=BookingHistoryView.as_view('booking_history')
)