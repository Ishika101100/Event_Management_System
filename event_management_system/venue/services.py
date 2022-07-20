from flask import render_template, redirect, url_for, request
from flask_login import current_user

from event_management_system.book_event.models import get_event_detail_for_venue, get_event_obj_for_venue
from event_management_system.caterer.models import get_caterer_for_venue
from event_management_system.decorator.models import get_decorator_for_venue
from event_management_system.users.models import commit_function
from event_management_system.venue.forms import VenueInfo
from event_management_system.venue.models import get_current_venue, get_venue, \
    get_venue_get_decorator_obj, get_venue_get_decorator_query, get_venue_get_caterer_obj, \
    get_venue_caterer_query


def get_checked_event(is_approved_by_venue_value):
    venue = get_current_venue()
    event_detail = get_event_detail_for_venue(venue_id=venue.id, is_approved_by_venue=is_approved_by_venue_value)
    if is_approved_by_venue_value == None:
        return render_template('venue_check_event.html', event_detail=event_detail)
    elif is_approved_by_venue_value == True:
        return render_template('venue_check_accepted_events.html', event_detail=event_detail)
    else:
        return render_template('venue_check_rejected_events.html', event_detail=event_detail)


def get_venue_booking_request(event_id, check_venue_approval):
    event_obj = get_event_obj_for_venue(event_id)
    event_obj.is_approved_by_venue = check_venue_approval
    commit_function()
    return redirect(url_for('users.home'))


def get_venue_info():
    form = VenueInfo()
    venue = get_current_venue()
    if form.validate_on_submit():
        if current_user.id == venue.user_id:
            venue.charges = form.venue_charge.data
            venue.capacity = form.venue_capactity.data
            commit_function()
        return render_template('venue_info.html', form=form)
    elif request.method == 'GET':
        venue = get_venue(venue_user_id=venue.user_id)
        form.venue_charge.data = venue.charges
        form.venue_capactity.data = venue.capacity
    return render_template('venue_info.html', form=form)


def get_venue_decorators_list(is_approved_decorator_by_venue):
    """venue gets list of decorator requests for business deal"""
    venue = get_current_venue()
    if current_user.id == venue.user_id:
        venue_get_decorator_obj = get_venue_get_decorator_obj(
            is_approved_decorator_by_venue=is_approved_decorator_by_venue)
        decorator_username = {}
        decorator_email = {}
        decorator_mobile_number = {}
        decorator_address = {}
        for i in venue_get_decorator_obj:
            decorator = get_decorator_for_venue(user_id=i.user_id)
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
            return render_template('venue_accepted_decorators.html', venue_get_decorator_obj=venue_get_decorator_obj,
                                   decorator=decorator_username,
                                   decorator_mobile_number=decorator_mobile_number, decorator_email=decorator_email,
                                   decorator_address=decorator_address)
        else:
            return render_template('venue_rejected_decorators.html', venue_get_decorator_obj=venue_get_decorator_obj,
                                   decorator=decorator_username,
                                   decorator_mobile_number=decorator_mobile_number, decorator_email=decorator_email,
                                   decorator_address=decorator_address)
    else:
        return render_template('venue_decorators.html')


def get_venue_request(decorator_id, is_approved_decorator):
    """venue accepts decorator's request"""
    venue_obj = get_current_venue()
    venue_get_decorator_obj = get_venue_get_decorator_query(venue_obj.id, decorator_id)
    venue_get_decorator_obj.is_approved_decorator = is_approved_decorator
    commit_function()
    return redirect(url_for('users.home'))


def get_venue_catrers_list(is_approved_caterer_by_venue):
    venue = get_current_venue()
    if current_user.id == venue.user_id:
        venue_get_caterer_obj = get_venue_get_caterer_obj(is_approved_caterer_by_venue)
        caterer_username = {}
        caterer_email = {}
        caterer_mobile_number = {}
        caterer_address = {}

        for i in venue_get_caterer_obj:
            caterer = get_caterer_for_venue(user_id=i.user_id)
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


def get_venue_caterer_request(caterer_id, is_approved_caterer):
    venue_obj = get_current_venue()
    venue_get_caterer_obj = get_venue_caterer_query(venue_obj.id, caterer_id)
    venue_get_caterer_obj.is_approved_caterer = is_approved_caterer
    commit_function()
    return redirect(url_for('users.home'))
