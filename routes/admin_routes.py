from flask import Blueprint, render_template, request, redirect, url_for, session, flash, make_response
from app import db
from abc import abstractmethod ,ABC
from flask.views import MethodView
from app.models.car import Car
from app.models.user import User
from app.models.booking import Booking
from sqlalchemy import and_
from io import BytesIO, StringIO
from xhtml2pdf import pisa

admin_bp = Blueprint('admin', __name__)

class AdminView(MethodView,ABC):
    """
    Base class for admin views.
    Provides common functionality for admin routes.
    """

    def is_admin(self):
        return session.get('username') == 'admin' and session.get('role') == 'admin'
    
    @abstractmethod
    def get(self, *args, **kwargs):
        pass

    def post(self, *args, **kwargs):
        pass


class AdminAnalyticsView(AdminView):
    """
    Admin Analytics View
    Handles displaying analytics data for the admin dashboard.
    """

    def get(self):
        if not super().is_admin():
            flash('Unauthorized access!', 'error')
            return redirect(url_for('auth.login'))

        total_revenue = db.session.query(db.func.sum(Booking.total_price)).scalar() or 0
        available_cars = Car.query.filter_by(available="Available").count()
        active_rentals = Booking.query.filter_by(status='Booked').count()
        total_customers = User.query.filter().count() - 1

        return render_template(
            "analytics.html",
            total_revenue=total_revenue,
            available_cars=available_cars,
            active_rentals=active_rentals,
            total_customers=total_customers
        )
    
    
class CarListView(AdminView):
    """
    Car List View
    Handles displaying the list of cars in the admin dashboard.
    """
    def get(self):
        if not super().is_admin():
            return redirect(url_for('auth.login'))

        cars = Car.query.all()
        return render_template("cars.html", cars=cars)

class CarCreateView(AdminView):
    """
    Car Create View
    Handles displaying the form for adding a new car.
    """

    def get(self):
        if not super().is_admin():
            return redirect(url_for('auth.login'))
        return render_template('add_car_form.html')

    def post(self):
        if not super().is_admin():
            return redirect(url_for('auth.login'))

        form = request.form
        required_fields = ['brand', 'model', 'year', 'category', 'seating_capacity',
                           'transmission', 'fuel_type', 'price_per_day', 'description', 'image', 'available']
        if not all(form.get(field) for field in required_fields):
            flash('All fields are required!', 'error')
            return redirect(url_for('admin.add_car'))

        new_car = Car(
            brand=form.get('brand'),
            model=form.get('model'),
            year=int(form.get('year')),
            category=form.get('category'),
            seating_capacity=int(form.get('seating_capacity')),
            transmission=form.get('transmission'),
            fuel_type=form.get('fuel_type'),
            price_per_day=float(form.get('price_per_day')),
            description=form.get('description'),
            image=form.get('image'),
            available=form.get('available')
        )
        db.session.add(new_car)
        db.session.commit()
        flash("Car added successfully!", "success")
        return redirect(url_for('admin.cars'))

class CarDetailView(AdminView):
    """
    Car Detail View
    Handles displaying the details of a specific car.
    """

    def get(self, car_id):
        if not super().is_admin():
            return redirect(url_for('auth.login'))

        car = Car.query.get_or_404(car_id)
        return render_template('car_view.html', car=car)

class CarEditView(AdminView):
    """
    Car Edit View
    Handles displaying the form for editing a car's details.
    """

    def get(self, car_id):
        if not super().is_admin():
            return redirect(url_for('auth.login'))

        car = Car.query.get_or_404(car_id)
        return render_template("edit_car_form.html", car=car)

class CarUpdateView(AdminView):
    """
    Car Update View
    Handles updating a car's details in the database.
    """

    def get(self, car_id):
        if not super().is_admin():
            return redirect(url_for('auth.login'))
        
    def post(self, car_id):
        if not super().is_admin():
            return redirect(url_for('auth.login'))

        car = Car.query.get_or_404(car_id)
        form = request.form

        car.brand = form.get('brand')
        car.model = form.get('model')
        car.year = int(form.get('year'))
        car.category = form.get('category')
        car.seating_capacity = int(form.get('seating_capacity'))
        car.transmission = form.get('transmission')
        car.fuel_type = form.get('fuel_type')
        car.price_per_day = float(form.get('price_per_day'))
        car.description = form.get('description')
        car.image = form.get('image')
        car.available = form.get('available')

        db.session.commit()
        flash("Car updated successfully!", "success")
        return redirect(url_for('admin.cars'))

class CarDeleteView(AdminView):
    """
    Car Delete View
    Handles deleting a car from the database.
    """

    def get(self):
        if not super().is_admin():
            return redirect(url_for('auth.login'))
    def post(self):
        if not super().is_admin():
            return redirect(url_for('auth.login'))

        car_id = request.form.get('car_id')
        car = Car.query.get(car_id)
        if car:
            db.session.delete(car)
            db.session.commit()
            flash("Car deleted successfully!", "success")
        else:
            flash("Car not found!", "error")

        return redirect(url_for('admin.cars'))

class RentalListView(AdminView):
    """
    Rental List View
    Handles displaying the list of rentals in the admin dashboard.
    """

    def get(self):
        if not super().is_admin():
            flash('Unauthorized access!', 'error')
            return redirect(url_for('auth.login'))

        bookings = Booking.query.all()
        return render_template("rental.html", bookings=bookings)

class CustomerListView(AdminView):
    """
    Customer List View
    Handles displaying the list of customers in the admin dashboard.
    """

    def get(self):
        if not super().is_admin():
            flash('Unauthorized access!', 'error')
            return redirect(url_for('auth.login'))

        users = User.query.filter(
            and_(User.username != 'admin', User.password != 'admin@123')
        ).all()

        return render_template('customers.html', users=users)
    
class CustomerDeleteView(AdminView):
    """
    Customer Delete View
    Handles deleting a customer from the database.
    """

    def get(self):
        if not super().is_admin():
            flash('Unauthorized access!', 'error')
            return redirect(url_for('auth.login'))
        return render_template('delete_user_form.html')
    def post(self):
        if not super().is_admin():
            flash('Unauthorized access!', 'error')
            return redirect(url_for('auth.login'))

        user_id = request.form.get('user_id')
        user = User.query.get(user_id)

        if user:
            # FIRST: Check if the user has an active booking
            active_booking = Booking.query.filter_by(user_id=user.id, status='Booked').first()
            inactive_booking = Booking.query.filter_by(user_id=user.id, status="Not Booked").all()

            if active_booking:
                car = Car.query.get(active_booking.car_id)
                if car:
                    car.available = 'Available'
                    db.session.delete(active_booking)
                    db.session.commit()

                else:
                    flash('Car not found for active booking!', 'error')

            if inactive_booking:
                for booking in inactive_booking:
                    db.session.delete(booking)
                    db.session.commit()
            else:
                flash('No inactive bookings found for this user!', 'error')
                

            # SECOND: Now safely delete the user
            db.session.delete(user)
            db.session.commit()
            flash('User deleted successfully!', 'success')
        else:
            flash('User not found!', 'error')

        return redirect(url_for('admin.customers'))

class BasePDFView(AdminView):
    """
    Base class for generating PDF reports.
    Provides common functionality for PDF generation.
    """

    pdf_template = None
    filename = "report.pdf"

    def get_pdf_data(self):
        return {}

    def get(self):
        if not super().is_admin():
            flash("Unauthorized", "error")
            return redirect(url_for("auth.login"))

        html = render_template(self.pdf_template, **self.get_pdf_data())
        pdf_stream = BytesIO()
        pisa_status = pisa.CreatePDF(html, dest=pdf_stream)

        if pisa_status.err:
            return "PDF generation failed", 500

        response = make_response(pdf_stream.getvalue())
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'attachment; filename={self.filename}'
        return response

class RentalReportPDFView(BasePDFView):
    """
    Rental Report PDF View
    Handles generating a PDF report of all rentals,
    with customer details.
    """

    pdf_template = "rental_report.html"
    filename = "rental_report.pdf"

    def get_pdf_data(self):
        users = User.query.all()
        customer_rentals = [
            {"user": u, "rentals": Booking.query.filter_by(user_id=u.id).all()}
            for u in users if Booking.query.filter_by(user_id=u.id).count()
        ]
        return {"customer_rentals": customer_rentals}
    
class ReservedCarsPDFView(BasePDFView):
    """
    Reserved Cars PDF View
    Handles generating a PDF report of all reserved cars.
    """

    pdf_template = "reserved_car_report.html"
    filename = "reserved_cars_report.pdf"

    def get_pdf_data(self):
        reserved_cars = Car.query.filter_by(available="Not Available").all()
        return {"reserved_cars": reserved_cars}

# Registering the routes with the blueprint

admin_bp.add_url_rule(
    '/admin/analytics',
    view_func=AdminAnalyticsView.as_view('analytics')
)
admin_bp.add_url_rule(
    '/admin_base/cars',
    view_func=CarListView.as_view('cars')
)

admin_bp.add_url_rule(
    '/admin_base/cars/add',
    view_func=CarCreateView.as_view('add_car')
)

admin_bp.add_url_rule(
    '/admin_base/cars/view/<int:car_id>',
    view_func=CarDetailView.as_view('car_view')
)

admin_bp.add_url_rule(
    '/admin_base/cars/edit/<int:car_id>',
    view_func=CarEditView.as_view('edit_car_form')
)

admin_bp.add_url_rule(
    '/admin_base/cars/update/<int:car_id>',
    view_func=CarUpdateView.as_view('update_car')
)

admin_bp.add_url_rule(
    '/admin_base/cars/delete',
    view_func=CarDeleteView.as_view('delete_car'),
    methods=["POST"]
)
admin_bp.add_url_rule(
    '/admin/rental',
    view_func=RentalListView.as_view('rental')
)
admin_bp.add_url_rule(
    '/admin/customers',
    view_func=CustomerListView.as_view('customers')
)

admin_bp.add_url_rule(
    '/delete_user',
    view_func=CustomerDeleteView.as_view('delete_user'),
    methods=["POST"]
)
admin_bp.add_url_rule(
    '/admin/rental-report/pdf',
    view_func=RentalReportPDFView.as_view('rental_report_pdf')
)

admin_bp.add_url_rule(
    '/admin/reports/reserved_cars_pdf',
    view_func=ReservedCarsPDFView.as_view('reserved_cars_pdf')
)
