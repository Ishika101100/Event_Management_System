from flask import render_template, redirect, url_for, request
from flask_login import current_user

from event_management_system.book_event.models import Event
from event_management_system.caterer.models import Caterer
from event_management_system.decorator.models import Decorator
from event_management_system.venue.forms import VenueInfo
from event_management_system.venue.models import Venues, VenueGetDecorator, VenueGetCaterer


class VenueClass:
    def get_checked_event(self, is_approved_by_venue_value):
        """
        user can get event details which he/she has booked
        :param is_approved_by_venue_value:from event's status
        :return:venue_check_event,venue_check_accepted_events or venue_check_accepted_events template according to venue's approval status
        """
        venue = Venues.get_current_venue()
        event_detail = Event.get_event_detail_for_venue(venue_id=venue.id,
                                                        is_approved_by_venue=is_approved_by_venue_value)
        if is_approved_by_venue_value == None:
            return render_template('venue_check_event.html', event_detail=event_detail)
        elif is_approved_by_venue_value == True:
            return render_template('venue_check_accepted_events.html', event_detail=event_detail)
        else:
            return render_template('venue_check_accepted_events.html', event_detail=event_detail)

    def get_venue_booking_request(self, event_id, check_venue_approval):
        """
        update event's status according to venue
        :param event_id:from selected event
        :param check_venue_approval:from event's status
        :return:redirect to home page of the website
        """
        Event.update_booking_request(event_id=event_id, check_venue_approval=check_venue_approval)
        return redirect(url_for('users.home'))

    def get_venue_info(self):
        """
        venue can change its rate and capacity
        :return: venue_info template
        """
        form = VenueInfo()
        venue = Venues.get_current_venue()
        if form.validate_on_submit():
            if current_user.id == venue.user_id:
                Venues.update_venue_info(venue_charge=form.venue_charge.data, venue_capacity=form.venue_capactity.data)
            return render_template('venue_info.html', form=form)
        elif request.method == 'GET':
            venue = Venues.get_venue(venue_user_id=venue.user_id)
            form.venue_charge.data = venue.charges
            form.venue_capactity.data = venue.capacity
        return render_template('venue_info.html', form=form)

    def get_venue_decorators_list(self, is_approved_decorator_by_venue):
        """venue gets list of decorator requests for business deal"""
        venue = Venues.get_current_venue()
        if current_user.id == venue.user_id:
            venue_get_decorator_obj = VenueGetDecorator.get_venue_get_decorator_obj(
                is_approved_decorator_by_venue=is_approved_decorator_by_venue)
            decorator_username = {}
            decorator_email = {}
            decorator_mobile_number = {}
            decorator_address = {}
            for i in venue_get_decorator_obj:
                decorator = Decorator.get_decorator_for_venue(user_id=i.user_id)
                decorator_username[decorator.id] = decorator.user.username
                decorator_email[decorator.id] = decorator.user.email
                decorator_mobile_number[decorator.id] = decorator.user.mobile_number
                decorator_address[decorator.id] = decorator.user.address
            if is_approved_decorator_by_venue == None:
                return render_template('venue_decorators.html', venue_get_decorator_obj=venue_get_decorator_obj,
                                       decorator=decorator_username,
                                       decorator_mobile_number=decorator_mobile_number, decorator_email=decorator_email,
                                       decorator_address=decorator_address)
            elif is_approved_decorator_by_venue == True:
                return render_template('venue_accepted_decorators.html',
                                       venue_get_decorator_obj=venue_get_decorator_obj,
                                       decorator=decorator_username,
                                       decorator_mobile_number=decorator_mobile_number, decorator_email=decorator_email,
                                       decorator_address=decorator_address)
            else:
                return render_template('venue_rejected_decorators.html',
                                       venue_get_decorator_obj=venue_get_decorator_obj,
                                       decorator=decorator_username,
                                       decorator_mobile_number=decorator_mobile_number, decorator_email=decorator_email,
                                       decorator_address=decorator_address)
        else:
            return render_template('venue_decorators.html')

    def get_venue_request(self, decorator_id, is_approved_decorator):
        """venue accepts decorator's request"""
        venue_obj = Venues.get_current_venue()
        VenueGetDecorator.get_approval_from_venue(venue_obj_id=venue_obj.id, decorator_id=decorator_id,
                                                  is_approved_decorator=is_approved_decorator)
        return redirect(url_for('users.home'))

    def get_venue_catrers_list(self, is_approved_caterer_by_venue):
        """
        venue get list of caterer according to its approval status from venue
        :param is_approved_caterer_by_venue: from venue's approval status
        :return: venue_catrers,venue_accepted_caterers or venue_rejected_caterers template according to approval status
        """
        venue = Venues.get_current_venue()
        if current_user.id == venue.user_id:
            venue_get_caterer_obj = VenueGetCaterer.get_venue_get_caterer_obj(is_approved_caterer_by_venue)
            caterer_username = {}
            caterer_email = {}
            caterer_mobile_number = {}
            caterer_address = {}

            for i in venue_get_caterer_obj:
                caterer = Caterer.get_caterer_for_venue(user_id=i.user_id)
                caterer_username[caterer.id] = caterer.user.username
                caterer_email[caterer.id] = caterer.user.email
                caterer_mobile_number[caterer.id] = caterer.user.mobile_number
                caterer_address[caterer.id] = caterer.user.address
            if is_approved_caterer_by_venue == None:
                return render_template('venue_catrers.html', caterer=caterer_username,
                                       caterer_mobile_number=caterer_mobile_number, caterer_email=caterer_email,
                                       caterer_address=caterer_address)
            elif is_approved_caterer_by_venue == True:
                return render_template('venue_accepted_caterers.html', caterer=caterer_username,
                                       caterer_mobile_number=caterer_mobile_number, caterer_email=caterer_email,
                                       caterer_address=caterer_address)
            else:
                return render_template('venue_rejected_caterers.html', caterer=caterer_username,
                                       caterer_mobile_number=caterer_mobile_number, caterer_email=caterer_email,
                                       caterer_address=caterer_address)
        else:
            return render_template('venue_catrers.html')

    def get_venue_caterer_request(self, caterer_id, is_approved_caterer):
        """
        venue changes approval status of caterer
        :param caterer_id: from VenueGetCaterer's caterer_id
        :param is_approved_caterer:from venue's approval status
        :return:redirect to home page of the website
        """
        venue_obj = Venues.get_current_venue()
        VenueGetCaterer.caterer_get_approval_from_venue(venue_obj_id=venue_obj.id, caterer_id=caterer_id,
                                                        is_approved_caterer=is_approved_caterer)
        return redirect(url_for('users.home'))
