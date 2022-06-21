from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user

caterer = Blueprint('caterer', __name__)

@caterer.route("/caterer_check_event")
@login_required
def check_event():
    if current_user.user_type == 4:
        return render_template('caterer_check_events.html')
    else:
        flash("Only caterer can access this page")
        return redirect(url_for('main.home'))

@caterer.route("/caterer_venues")
@login_required
def venues():
    if current_user.user_type == 4:
        return render_template('caterer_venues.html')
    else:
        flash("Only caterer can access this page")
        return redirect(url_for('main.home'))

@caterer.route("/caterer_category")
@login_required
def category():
    if current_user.user_type == 4:
        return render_template('caterer_category.html')
    else:
        flash("Only caterer can access this page")
        return redirect(url_for('main.home'))