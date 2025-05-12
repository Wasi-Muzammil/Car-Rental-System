from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.models.user import User
from flask.views import MethodView
from app import db

payment_bp = Blueprint('payment', __name__)

class PaymentView(MethodView):
    """
    Payment View
    Handles displaying the payment page and processing balance updates.
    """

    def get(self):
        user_id = session.get('user_id')
        if not user_id:
            flash("You must be logged in to access the payment page.", "error")
            return redirect(url_for('main.main'))

        user = db.session.get(User, user_id)
        if not user:
            flash("User not found.", "error")
            return redirect(url_for('auth.login'))

        return render_template("payment.html", balance=user.balance)

    def post(self):
        user_id = session.get('user_id')
        if not user_id:
            flash("You must be logged in to access the payment page.", "error")
            return redirect(url_for('auth.login'))

        user = db.session.get(User, user_id)
        if not user:
            flash("User not found.", "error")
            return redirect(url_for('auth.login'))

        add_balance = request.form.get("add_balance")
        withdraw_balance = request.form.get("withdraw_balance")

        if add_balance:
            try:
                add_amount = float(add_balance)
                if add_amount > 0:
                    user.balance += add_amount
                    db.session.commit()
                    flash(f"${add_amount} added to your account!", "success")
                else:
                    flash("Enter a valid amount to deposit.", "error")
            except ValueError:
                flash("Invalid deposit amount.", "error")

        if withdraw_balance:
            try:
                withdraw_amount = float(withdraw_balance)
                if 0 < withdraw_amount <= user.balance:
                    user.balance -= withdraw_amount
                    db.session.commit()
                    flash(f"${withdraw_amount} withdrawn from your account!", "success")
                elif withdraw_amount > user.balance:
                    flash("Insufficient balance!", "error")
                else:
                    flash("Enter a valid amount to withdraw.", "error")
            except ValueError:
                flash("Invalid withdrawal amount.", "error")

        return redirect(url_for('payment.payment'))
    
# Register the PaymentView with the payment blueprint

payment_bp.add_url_rule(
    '/payment',
    view_func=PaymentView.as_view('payment')
    )