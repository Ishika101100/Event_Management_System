from datetime import date

from flask import Blueprint, render_template, flash, redirect, request, url_for, jsonify
from flask_login import login_required, current_user

from event_management_system import db
from event_management_system.book_event.forms import EventForm, UpdateForm
from event_management_system.models import Venues, EventCategory, Caterer, Decorator, Event, VenueGetCaterer, \
    VenueGetDecorator, CatererGetFoodCategory, DecoratorGetTypes
from event_management_system.users.utils import is_user

book_event = Blueprint('book_event', __name__)


@book_event.route("/update_event/<int:event_id>", methods=['GET', 'POST'])
@login_required
@is_user
def update_event(event_id):
    """User can update his/her booked events"""

    form = UpdateForm()
    event_obj = Event.query.filter_by(id=event_id).first()

    if form.validate_on_submit():
        if current_user.id == event_obj.user_id:
            event_obj.title = form.title.data
            event_obj.no_of_guests = form.no_of_guests.data
            event_obj.date = form.date.data
            event_obj.start_time = form.start_time.data
            event_obj.end_time = form.end_time.data
            db.session.commit()
        return render_template('update_event.html', form=form)
    elif request.method == 'GET':
        form.title.data = event_obj.title
        form.no_of_guests.data = event_obj.no_of_guests
        form.date.data = event_obj.date
        form.start_time.data = event_obj.start_time
        form.end_time.data = event_obj.end_time
    return render_template('update_event.html', form=form)



@book_event.route("/delete_event/<int:event_id>", methods=['GET', 'POST'])
@login_required
@is_user
def delete_event(event_id):
    """User can delete his/her events"""

    form = UpdateForm()
    event_obj = Event.query.filter_by(id=event_id).first()
    db.session.delete(event_obj)
    db.session.commit()
    return render_template('view_events.html', form=form)


@book_event.route("/findEventVenue/", methods=['GET', 'POST'])
@login_required
def findEventVenue():
    """Event venues from AJAX call"""
    if request.method == 'POST':
        form_data = request.get_json()
        event_type_id = form_data['event_type']
        ######Query for retriving venues######

        venue_get = Venues.query.join(EventCategory, Venues.venue_type == event_type_id).filter(
            Venues.venue_type == EventCategory.id).all()
        venue_name = []
        for venue in venue_get:
            data = {'id': venue.id, 'name': venue.venue_name.username}
            venue_name.append(data)
    return jsonify({'venue_name': venue_name})


@book_event.route('/findVenueDetails/', methods=['GET', 'POST'])
@login_required
def findVenueDetails():
    """Venue details from AJAX call"""
    if request.method == "POST":
        form_data = request.get_json()
        venue_id = form_data['venue_id']
        venue_data = Venues.query.filter_by(id=venue_id).first()
        venue_list = {'capacity': venue_data.capacity, 'charges': venue_data.charges}
        caterer = VenueGetCaterer.query.join(Caterer, VenueGetCaterer.caterer_id == Caterer.id).filter(
            VenueGetCaterer.caterer_id == Caterer.id).filter(VenueGetCaterer.venue_id == venue_id).filter(
            VenueGetCaterer.is_approved_caterer == True).all()
        caterer_list = []
        for caterer_details in caterer:
            caterer_data = VenueGetCaterer.query.filter_by(caterer_id=caterer_details.caterer_id).first()
            data = {'id': caterer_data.caterer_id, 'name': caterer_data.venue_get_caterer.user_get_caterer.username}
            caterer_list.append(data)

        decorator = VenueGetDecorator.query.join(Decorator, VenueGetDecorator.decorator_id == Decorator.id).filter(
            VenueGetDecorator.decorator_id == Decorator.id).filter(VenueGetDecorator.venue_id == venue_id).filter(
            VenueGetDecorator.is_approved_decorator == True).all()
        decorator_list = []
        for decorator_details in decorator:
            decorator_data = VenueGetDecorator.query.filter_by(decorator_id=decorator_details.decorator_id).first()
            data = {'id': decorator_data.decorator_id,
                    'name': decorator_data.venue_get_decorators.user_get_decorator.username}
            decorator_list.append(data)
    return jsonify({'venue_data': venue_list, 'caterer_list': caterer_list, 'decorator_list': decorator_list})


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

    cate = EventCategory.query.all()
    venue_get = Venues.query.join(EventCategory, Venues.venue_type == EventCategory.id).filter(
        Venues.venue_type == EventCategory.id).all()
    caterer = VenueGetCaterer.query.join(Caterer, VenueGetCaterer.caterer_id == Caterer.id).filter(
        VenueGetCaterer.caterer_id == Caterer.id).all()
    decorator = VenueGetDecorator.query.join(Decorator, VenueGetDecorator.decorator_id == Decorator.id).filter(
        VenueGetDecorator.decorator_id == Decorator.id).all()
    form = EventForm()
    category = request.form.get('event_location')

    if category == "1":
        event = Event.query.filter_by(user_id=current_user.id).filter_by(
            venue_id=request.form.get('venue_select')).filter(Event.date >= date.today()).first()
        if not event:
            if form.validate_on_submit():
                event = Event(user_id=current_user.id, title=form.title.data,
                              category=request.form.get('event_location'), date=request.form.get('date'),
                              venue_id=request.form.get('venue_select'),
                              decorator_id=request.form.get('decorator_select'),
                              caterer_id=request.form.get('caterer_select'),
                              start_time=request.form.get('start_time'),
                              end_time=request.form.get('end_time'), no_of_guests=form.no_of_guests.data,
                              venue_charge=request.values.get("id_venue_charge"),
                              decorator_charge=request.values.get("id_decoration_charge"),
                              caterer_charge=request.values.get("id_caterer_charge"),
                              Total_charge=request.values.get("id_total_charge"))
                db.session.add(event)
                db.session.commit()
                flash(f"Your request is sent to Venue!", "alert alert-primary")
                return redirect(url_for('main.home'))
        else:
            flash("You have already registered event on this day at this venue. Please try any other date or venue",
                  "danger")
    else:
        event = Event.query.filter_by(user_id=current_user.id).filter_by(
            venue_id=request.form.get('venue_select')).filter(Event.date >= date.today()).first()
        if not event:
            if form.validate_on_submit():
                event = Event(user_id=current_user.id, title=form.title.data,
                              category=request.form.get('event_location'), date=request.form.get('date'),
                              venue_id=request.form.get('venue_select'),
                              caterer_id=request.form.get('caterer_select'),
                              start_time=request.form.get('start_time'), end_time=request.form.get('end_time'),
                              no_of_guests=form.no_of_guests.data,
                              venue_charge=request.values.get("id_venue_charge"),
                              caterer_charge=request.values.get("id_caterer_charge"),
                              Total_charge=request.values.get("id_total_charge"))
                db.session.add(event)
                db.session.commit()
                flash(f"Your request is sent to Venue!", "alert alert-primary")
                return redirect(url_for('main.home'))
        else:
            flash("You have already registered event on this day at this venue. Please try any other date or venue")
    return render_template('book_event.html', cate=cate, caterer=caterer, venue_get=venue_get, decorator=decorator,
                           form=form)



@book_event.route("/view_event", methods=['GET', 'POST'])
@login_required
@is_user
def view_event():
    """View event details"""
    event_detail = Event.query.filter_by(user_id=current_user.id).all()
    return render_template('view_events.html', event_detail=event_detail)
