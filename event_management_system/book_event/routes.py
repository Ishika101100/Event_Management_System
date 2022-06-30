from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from event_management_system.book_event.forms import EventForm
from event_management_system.models import Venues, EventCategory

book_event = Blueprint('book_event', __name__)


@book_event.route("/book_event")
@login_required
def event():
    """
    if current user type is 1(User),then and only then book event page will be accessed.
    """
    if current_user.user_type == 1:
        form = EventForm()
        cate = EventCategory.query.all()
        venue_get = Venues.query.all()
        return render_template('book_event.html', cate=cate, venue_get=venue_get, form=form)
    else:
        flash("Only users can access this page", "warning")
        return redirect(url_for('main.home'))
