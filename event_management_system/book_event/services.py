from flask import render_template, request, jsonify, flash, redirect, url_for
from flask_login import current_user

from event_management_system.book_event.constants import BOOK_EVENT_SUCCESSFULLY, SENT_REQUEST_TO_VENUE
from event_management_system.book_event.forms import UpdateForm, EventForm
from event_management_system.book_event.models import Event, EventCategory
from event_management_system.caterer.models import CatererGetFoodCategory
from event_management_system.decorator.models import DecoratorGetTypes
from event_management_system.venue.models import Venues, VenueGetCaterer, VenueGetDecorator


class BookEvent:
    def get_update_event(self, event_id):
        """
        User can update his/her booked event if today's date is not equal to today's date.
        :param event_id: int> get id of event which user wants to update
        :return:template of updating event
        """
        form = UpdateForm()
        event_obj = Event.get_event_query(event_id)

        if form.validate_on_submit():
            if current_user.id == event_obj.user_id:
                Event.update_event_data(event_id=event_id, title=form.title.data, no_of_guests=form.no_of_guests.data,
                                        date=form.date.data, start_time=form.start_time.data,
                                        end_time=form.end_time.data)

            return render_template('update_event.html', form=form)
        elif request.method == 'GET':
            form.title.data = event_obj.title
            form.no_of_guests.data = event_obj.no_of_guests
            form.date.data = event_obj.date
            form.start_time.data = event_obj.start_time
            form.end_time.data = event_obj.end_time
        return render_template('update_event.html', form=form)

    def get_delete_event(self, event_id):
        """
        User can delete his/her booked event if today's date is not equal to today's date.
        :param event_id: int> get id of event which user wants to delete
        :return:template of viewing all events
        """
        form = UpdateForm()
        Event.delete_event_data(event_id)
        return render_template('view_events.html', form=form)

    def getEventVenue(self):
        """
        user get list of venues according to selected event type
        :return: json data of venue id and venue name
        """
        if request.method == 'POST':
            form_data = request.get_json()
            event_type_id = form_data['event_type']
            venue_get = Venues.get_venue_for_event(event_type_id)
            venue_name = []
            for venue in venue_get:
                data = {'id': venue.id, 'name': venue.venue_name.username}
                venue_name.append(data)
        return jsonify({'venue_name': venue_name})

    def getCatererDetails(self):
        """
        user get list of food category, and it's charge of selected caterer
        :return: json data of caterer's food category and charge
        """
        if request.method == "POST":
            form_data = request.get_json()
            caterer_id = form_data['caterer_id']
            caterer_data = CatererGetFoodCategory.get_caterer_food_cate_for_event(caterer_id)
            caterer_details = []
            for caterer in caterer_data:
                data = {'id': caterer.caterer_id, 'charges': caterer.charges,
                        'food_category': caterer.caterer_get_foodcategory.food_type,
                        'food_type_id': caterer.food_category_id}
                caterer_details.append(data)
        return jsonify({'caterer_details': caterer_details})

    def get_decorator_details(self):
        """
        user get list of decoration category, and it's charge of selected decorator
        :return: json data of decorator's decoration category and charge
        """
        if request.method == "POST":
            form_data = request.get_json()
            decorator_id = form_data['decorator_id']
            decorator_data = DecoratorGetTypes.get_decor_types_for_event(decorator_id)
            decorator_details = []
            for decorator in decorator_data:
                data = {'id': decorator.decorator_id, 'charges': decorator.charges,
                        'decoration_type': decorator.decorator_get_decorationType.decoration_type,
                        'decoration_type_id': decorator.decoration_type_id}
                decorator_details.append(data)
        return jsonify({'decorator_details': decorator_details})

    def getVenueDetails(self):
        """
        user get list of decorators and caterers of selected venue
        :return: json data of venue , caterer and decorator details
        """
        if request.method == "POST":
            form_data = request.get_json()
            venue_id = form_data['venue_id']
            venue_data = Venues.get_venue_data_for_event(venue_id)
            venue_list = {'capacity': venue_data.capacity, 'charges': venue_data.charges}
            caterer = VenueGetCaterer.venue_get_caterer_for_event(venue_id)
            caterer_list = []
            for caterer_details in caterer:
                caterer_data = VenueGetCaterer.caterer_query_for_event(caterer_id=caterer_details.caterer_id)
                data = {'id': caterer_data.caterer_id, 'name': caterer_data.venue_get_caterer.user_get_caterer.username}
                caterer_list.append(data)

            decorator = VenueGetDecorator.venue_get_decorator_for_event(venue_id)
            decorator_list = []
            for decorator_details in decorator:
                decorator_data = VenueGetDecorator.decorator_query_for_event(
                    decorator_id=decorator_details.decorator_id)
                data = {'id': decorator_data.decorator_id,
                        'name': decorator_data.venue_get_decorators.user_get_decorator.username}
                decorator_list.append(data)
        return jsonify({'venue_data': venue_list, 'caterer_list': caterer_list, 'decorator_list': decorator_list})

    def get_book_event(self):
        """
        book users event and add booking details in database
        :return: book event template
        """
        cate = EventCategory.get_event_category()
        venue_get = Venues.book_event_get_venue_query()
        caterer = VenueGetCaterer.get_caterer_query_for_event()
        decorator = VenueGetDecorator.get_decorator_for_event()
        form = EventForm()
        category = request.form.get('event_location')

        if category == "1":
            event = Event.get_event(venue_id=request.form.get('venue_select'))
            if not event:
                if form.validate_on_submit():
                    Event.book_event_for_category_one(title=form.title.data,
                                                      category=request.form.get('event_location'),
                                                      date=request.form.get('date'),
                                                      venue_id=request.form.get('venue_select'),
                                                      decorator_id=request.form.get('decorator_select'),
                                                      caterer_id=request.form.get('caterer_select'),
                                                      start_time=request.form.get('start_time'),
                                                      end_time=request.form.get('end_time'),
                                                      no_of_guests=form.no_of_guests.data,
                                                      venue_charge=request.values.get("id_venue_charge"),
                                                      decorator_charge=request.values.get(
                                                          "id_decoration_charge"),
                                                      caterer_charge=request.values.get(
                                                          "id_caterer_charge"),
                                                      Total_charge=request.values.get("id_total_charge"))

                    flash(SENT_REQUEST_TO_VENUE, "alert alert-primary")
                    return redirect(url_for('users.home'))
            else:
                flash(BOOK_EVENT_SUCCESSFULLY, "danger")
        else:
            event = Event.get_event(venue_id=request.form.get('venue_select'))
            if not event:
                if form.validate_on_submit():
                    Event.book_event_for_category_two(title=form.title.data,
                                                      category=request.form.get('event_location'),
                                                      date=request.form.get('date'),
                                                      venue_id=request.form.get('venue_select'),
                                                      caterer_id=request.form.get('caterer_select'),
                                                      start_time=request.form.get('start_time'),
                                                      end_time=request.form.get('end_time'),
                                                      no_of_guests=form.no_of_guests.data,
                                                      venue_charge=request.values.get("id_venue_charge"),
                                                      caterer_charge=request.values.get(
                                                          "id_caterer_charge"),
                                                      Total_charge=request.values.get("id_total_charge"))
                    flash(SENT_REQUEST_TO_VENUE, "alert alert-primary")
                    return redirect(url_for('users.home'))
            else:
                flash(BOOK_EVENT_SUCCESSFULLY, "danger")
        return render_template('book_event.html', cate=cate, caterer=caterer, venue_get=venue_get, decorator=decorator,
                               form=form)

    def get_view_event(self):
        """
        view list of events of current user
        :return: view events template
        """
        event_detail = Event.get_current_event()
        return render_template('view_events.html', event_detail=event_detail)
