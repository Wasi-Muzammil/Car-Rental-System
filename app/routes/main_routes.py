from flask import Blueprint, render_template, redirect, url_for, request, session
from app.models.car import Car
from flask.views import MethodView

main_bp = Blueprint('main', __name__)

class MainView(MethodView):
    """
    Main View
    Handles displaying the main page with car listings.
    """

    def get(self):
        category = request.args.get('category', 'sedan')
        cars = Car.query.filter_by(category=category).all()
        return render_template('main.html', cars=cars, selected_category=category)

class AboutView(MethodView):
    """
    About View
    Handles displaying the about page.
    """

    def get(self):
        return render_template('about.html')
    
class ServicesView(MethodView):
    """
    Services View
    Handles displaying the services page.
    """

    def get(self):
        return render_template('services.html')

class ContactView(MethodView):
    """
    Contact View
    Handles displaying the contact page.
    """

    def get(self):
        return render_template('contact.html')

# Register the routes with the blueprint

main_bp.add_url_rule('/',view_func=MainView.as_view('main'))
main_bp.add_url_rule('/about', view_func=AboutView.as_view('about'))
main_bp.add_url_rule('/services', view_func=ServicesView.as_view('services'))
main_bp.add_url_rule('/contact', view_func=ContactView.as_view('contact'))

