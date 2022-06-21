from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user

decorator = Blueprint('decorator', __name__)

@decorator.route("/decorator_check_event")
@login_required
def check_event():
    if current_user.user_type == 3:
        return render_template('decorator_check_event.html')
    else:
        flash("Only decorator can access this page")
        return redirect(url_for('main.home'))

@decorator.route("/decorator_venues")
@login_required
def venues():
    if current_user.user_type == 3:
        return render_template('decorator_venues.html')
    else:
        flash("Only decorator can access this page")
        return redirect(url_for('main.home'))

@decorator.route("/decorator_category")
@login_required
def category():
    if current_user.user_type == 3:
        return render_template('decorator_category.html')
    else:
        flash("Only decorator can access this page")
        return redirect(url_for('main.home'))