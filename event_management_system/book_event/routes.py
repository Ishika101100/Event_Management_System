from flask import Blueprint
from flask_login import login_required

from event_management_system.book_event.services import get_update_event, get_delete_event, getEventVenue, \
    getVenueDetails, get_book_event, get_view_event, getCatererDetails, get_decorator_details
from event_management_system.users.utils import is_user

book_event = Blueprint('book_event', __name__, template_folder='templates/book_event',
                       static_folder='static/book_event')


@book_event.route("/update_event/<int:event_id>", methods=['GET', 'POST'])
@login_required
def update_event(event_id):
    """User can update his/her booked events"""
    return get_update_event(event_id)


@book_event.route("/delete_event/<int:event_id>", methods=['GET', 'POST'])
@login_required
def delete_event(event_id):
    """User can delete his/her events"""
    return get_delete_event(event_id)


@book_event.route("/findEventVenue/", methods=['GET', 'POST'])
@login_required
def findEventVenue():
    """Event venues from AJAX call"""
    return getEventVenue()


@book_event.route('/findVenueDetails/', methods=['GET', 'POST'])
@login_required
def findVenueDetails():
    """Venue details from AJAX call"""
    return getVenueDetails()


@book_event.route('/findCatererDetails/', methods=['GET', 'POST'])
@login_required
def findCatererDetails():
    """Caterer details from AJAX call"""
    return getCatererDetails()


@book_event.route('/findDecoratorDetails/', methods=['GET', 'POST'])
@login_required
def findDecoratorDetails():
    """Decorator details from AJAX call"""
    return get_decorator_details()


@book_event.route("/book_event", methods=['GET', 'POST'])
@login_required
@is_user
def event():
    """
    if current user type is 1(User),then and only then book event page will be accessed.
    """
    return get_book_event()


@book_event.route("/view_event", methods=['GET', 'POST'])
@login_required
@is_user
def view_event():
    """View event details"""
    return get_view_event()
