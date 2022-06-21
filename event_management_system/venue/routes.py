from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user

venue = Blueprint('venue', __name__)

@venue.route("/venue_check_event")
@login_required
def check_event():
    if current_user.user_type == 2:
        return render_template('venue_check_event.html')
    else:
        flash("Only venue can access this page")
        return redirect(url_for('main.home'))


@venue.route("/venue_info")
@login_required
def venue_info():
    if current_user.user_type == 2:
        return render_template('venue_info.html')
    else:
        flash("Only venue can access this page")
        return redirect(url_for('main.home'))

@venue.route("/venue_decorators")
@login_required
def venue_decorator():
    if current_user.user_type == 2:
        return render_template('venue_decorators.html')
    else:
        flash("Only venue can access this page")
        return redirect(url_for('main.home'))

@venue.route("/venue_catrers")
@login_required
def venue_catrer():
    if current_user.user_type == 2:
        return render_template('venue_catrers.html')
    else:
        flash("Only venue can access this page")
        return redirect(url_for('main.home'))