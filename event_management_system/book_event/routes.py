from flask import Blueprint, request, jsonify
from flask_login import login_required

from event_management_system.book_event.services import get_update_event, get_delete_event, getEventVenue, \
    getVenueDetails, get_book_event, get_view_event
from event_management_system.caterer.models import CatererGetFoodCategory
from event_management_system.decorator.models import DecoratorGetTypes
from event_management_system.users.utils import is_user

book_event = Blueprint('book_event', __name__,template_folder='templates/book_event',static_folder='static/book_event')


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
    if request.method == "POST":
        form_data = request.get_json()
        caterer_id = form_data['caterer_id']
        caterer_data = CatererGetFoodCategory.query.filter_by(caterer_id=caterer_id).all()
        caterer_details = []
        for caterer in caterer_data:
            data = {'id': caterer.caterer_id, 'charges': caterer.charges,
                    'food_category': caterer.caterer_get_foodcategory.food_type,
                    'food_type_id': caterer.food_category_id}
            caterer_details.append(data)
    return jsonify({'caterer_details': caterer_details})


@book_event.route('/findDecoratorDetails/', methods=['GET', 'POST'])
@login_required
def findDecoratorDetails():
    """Decorator details from AJAX call"""
    if request.method == "POST":
        form_data = request.get_json()
        decorator_id = form_data['decorator_id']
        decorator_data = DecoratorGetTypes.query.filter_by(decorator_id=decorator_id).all()
        decorator_details = []
        for decorator in decorator_data:
            data = {'id': decorator.decorator_id, 'charges': decorator.charges,
                    'decoration_type': decorator.decorator_get_decorationType.decoration_type,
                    'decoration_type_id': decorator.decoration_type_id}
            decorator_details.append(data)
    return jsonify({'decorator_details': decorator_details})


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
