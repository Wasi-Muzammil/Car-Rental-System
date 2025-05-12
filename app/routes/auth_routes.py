from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash, generate_password_hash
from flask.views import MethodView
from app.models.user import User
from app import db

auth_bp = Blueprint('auth', __name__)

class LoginView(MethodView):
    """
    Login View
    Handles user login functionality.
    """

    def get(self):
        return render_template('login.html')

    def post(self):
        username = request.form.get('username')
        password = request.form.get('password')

        if username == 'admin' and password == 'admin@123':
            session['username'] = username
            session['role'] = 'admin'
            return redirect(url_for('admin.analytics'))

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['username'] = username
            session['user_id'] = user.id
            session['role'] = 'user'
            flash('Login successful!', 'success')
            return redirect(url_for('main.main'))
        else:
            flash('Invalid username or password', 'error')
            return render_template('login.html')

class RegisterView(MethodView):
    """
    Register View
    Handles user registration functionality.
    """

    def get(self):
        return render_template('register.html')

    def post(self):
        form = request.form
        required_fields = ['first_name', 'last_name', 'username', 'password', 'address']
        if not all(form.get(field) for field in required_fields):
            flash('All fields are required!', 'error')
            return redirect(url_for('auth.register'))

        if User.query.filter_by(username=form.get('username')).first():
            flash('Username already exists!', 'error')
            return redirect(url_for('auth.register'))

        if form.get('email') and User.query.filter_by(email=form.get('email')).first():
            flash('Email already exists!', 'error')
            return redirect(url_for('auth.register'))

        new_user = User(
            first_name=form.get('first_name'),
            last_name=form.get('last_name'),
            username=form.get('username'),
            password=generate_password_hash(form.get('password')),
            email=form.get('email'),
            address=form.get('address'),
            balance=float(form.get('balance', 0)),
            booking_info=form.get('booking_info', 'Not Booked')
        )
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('auth.login'))

class LogoutView(MethodView):
    """
    Loginout View
    Handles user logout functionality.
    """

    def get(self):
        session.clear()
        flash('Logged out successfully!', 'success')
        return redirect(url_for('main.main'))

# Register the views with the blueprint


auth_bp.add_url_rule(
    '/logout',
    view_func=LogoutView.as_view('logout')
)
    

auth_bp.add_url_rule(
    '/login',
    view_func=LoginView.as_view('login')
)

auth_bp.add_url_rule(
    '/register',
    view_func=RegisterView.as_view('register')
)