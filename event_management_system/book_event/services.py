from flask import render_template, request, jsonify, flash, redirect, url_for
from flask_login import current_user

from event_management_system.book_event.forms import UpdateForm, EventForm
from event_management_system.book_event.models import get_event_query, get_event_category, get_event, \
    book_event_for_category_one, book_event_for_category_two, get_current_event
from event_management_system.users.models import commit_function, delete_function, add_function
from event_management_system.venue.models import get_venue_for_event, get_venue_data_for_event, \
    venue_get_caterer_for_event, caterer_query_for_event, venue_get_decorator_for_event, decorator_query_for_event, \
    book_event_get_venue_query, get_caterer_query_for_event, get_decorator_for_event


def get_update_event(event_id):
    form = UpdateForm()
    event_obj = get_event_query(event_id)

    if form.validate_on_submit():
        if current_user.id == event_obj.user_id:
            event_obj.title = form.title.data
            event_obj.no_of_guests = form.no_of_guests.data
            event_obj.date = form.date.data
            event_obj.start_time = form.start_time.data
            event_obj.end_time = form.end_time.data
            commit_function()
        return render_template('update_event.html', form=form)
    elif request.method == 'GET':
        form.title.data = event_obj.title
        form.no_of_guests.data = event_obj.no_of_guests
        form.date.data = event_obj.date
        form.start_time.data = event_obj.start_time
        form.end_time.data = event_obj.end_time
    return render_template('update_event.html', form=form)


def get_delete_event(event_id):
    form = UpdateForm()
    event_obj = get_event_query(event_id)
    delete_function(event_obj)
    commit_function()
    return render_template('view_events.html', form=form)


def getEventVenue():
    if request.method == 'POST':
        form_data = request.get_json()
        event_type_id = form_data['event_type']

        venue_get = get_venue_for_event(event_type_id)
        venue_name = []
        for venue in venue_get:
            data = {'id': venue.id, 'name': venue.venue_name.username}
            venue_name.append(data)
    return jsonify({'venue_name': venue_name})


def getVenueDetails():
    if request.method == "POST":
        form_data = request.get_json()
        venue_id = form_data['venue_id']
        venue_data = get_venue_data_for_event(venue_id)
        venue_list = {'capacity': venue_data.capacity, 'charges': venue_data.charges}
        caterer = venue_get_caterer_for_event(venue_id)
        caterer_list = []
        for caterer_details in caterer:
            caterer_data = caterer_query_for_event(caterer_id=caterer_details.caterer_id)
            data = {'id': caterer_data.caterer_id, 'name': caterer_data.venue_get_caterer.user_get_caterer.username}
            caterer_list.append(data)

        decorator = venue_get_decorator_for_event(venue_id)
        decorator_list = []
        for decorator_details in decorator:
            decorator_data = decorator_query_for_event(decorator_id=decorator_details.decorator_id)
            data = {'id': decorator_data.decorator_id,
                    'name': decorator_data.venue_get_decorators.user_get_decorator.username}
            decorator_list.append(data)
    return jsonify({'venue_data': venue_list, 'caterer_list': caterer_list, 'decorator_list': decorator_list})


def get_book_event():
    cate = get_event_category()
    venue_get = book_event_get_venue_query()
    caterer = get_caterer_query_for_event()
    decorator = get_decorator_for_event()
    form = EventForm()
    category = request.form.get('event_location')

    if category == "1":
        event = get_event(venue_id=request.form.get('venue_select'))
        if not event:
            if form.validate_on_submit():
                event_obj = book_event_for_category_one(title=form.title.data,
                                                        category=request.form.get('event_location'),
                                                        date=request.form.get('date'),
                                                        venue_id=request.form.get('venue_select'),
                                                        decorator_id=request.form.get('decorator_select'),
                                                        caterer_id=request.form.get('caterer_select'),
                                                        start_time=request.form.get('start_time'),
                                                        end_time=request.form.get('end_time'),
                                                        no_of_guests=form.no_of_guests.data,
                                                        venue_charge=request.values.get("id_venue_charge"),
                                                        decorator_charge=request.values.get("id_decoration_charge"),
                                                        caterer_charge=request.values.get("id_caterer_charge"),
                                                        Total_charge=request.values.get("id_total_charge"))
                add_function(event_obj)
                commit_function()
                flash(f"Your request is sent to Venue!", "alert alert-primary")
                return redirect(url_for('users.home'))
        else:
            flash("You have already registered event on this day at this venue. Please try any other date or venue",
                  "danger")
    else:
        event = get_event(venue_id=request.form.get('venue_select'))
        if not event:
            if form.validate_on_submit():
                event_obj = book_event_for_category_two()
                add_function(event_obj)
                commit_function()
                flash(f"Your request is sent to Venue!", "alert alert-primary")
                return redirect(url_for('users.home'))
        else:
            flash("You have already registered event on this day at this venue. Please try any other date or venue")
    return render_template('book_event.html', cate=cate, caterer=caterer, venue_get=venue_get, decorator=decorator,
                           form=form)


def get_view_event():
    event_detail = get_current_event()
    return render_template('view_events.html', event_detail=event_detail)
