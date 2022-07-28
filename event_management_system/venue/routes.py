from flask import Blueprint
from flask_login import login_required

from event_management_system.venue.services import VenueClass
from event_management_system.venue.utils import is_venue

venue = Blueprint('venue', __name__, template_folder='templates/venue')

venue_obj = VenueClass()


@venue.route("/venue_check_event")
@login_required
@is_venue
def check_event():
    """check booked events"""
    return venue_obj.get_checked_event(is_approved_by_venue_value=None)


@venue.route("/venue_accepted_event")
@login_required
@is_venue
def venue_accepted_event():
    """Check accepted event"""
    return venue_obj.get_checked_event(is_approved_by_venue_value=True)


@venue.route("/venue_rejected_event")
@login_required
def venue_rejected_event():
    """Check rejected events"""
    return venue_obj.get_checked_event(is_approved_by_venue_value=False)


@venue.route("/venue_accept_booking_request/<int:event_id>")
def venue_accept_booking_request(event_id):
    """Venue accepts booking request"""
    return venue_obj.get_venue_booking_request(event_id, check_venue_approval=True)


@venue.route("/venue_reject_booking_request/<int:event_id>")
def venue_reject_booking_request(event_id):
    """Venue rejects booking request"""
    return venue_obj.get_venue_booking_request(event_id, check_venue_approval=False)


@venue.route("/venue_info", methods=['GET', 'POST'])
@login_required
@is_venue
def venue_info():
    """venue charges and capacity can be updated"""
    return venue_obj.get_venue_info()


@venue.route("/venue_decorators")
@login_required
@is_venue
def venue_decorators():
    """venue gets list of decorator requests for business deal"""
    return venue_obj.get_venue_decorators_list(is_approved_decorator_by_venue=None)


@venue.route("/venue_accepted_decorators")
@login_required
@is_venue
def venue_accepted_decorators():
    """venue can get list of decorator whose request is accepted"""
    return venue_obj.get_venue_decorators_list(is_approved_decorator_by_venue=True)


@venue.route("/venue_rejected_decorators")
@login_required
@is_venue
def venue_rejected_decorators():
    """venue can get list of decorator whose request is rejected"""
    return venue_obj.get_venue_decorators_list(is_approved_decorator_by_venue=False)


@venue.route("/venue_accept_request/<int:decorator_id>")
def venue_accept_request(decorator_id):
    """venue accepts decorator's request"""
    return venue_obj.get_venue_request(decorator_id, is_approved_decorator=True)


@venue.route("/venue_reject_request/<int:decorator_id>")
def venue_reject_request(decorator_id):
    """venue rejects decorator's request"""
    return venue_obj.get_venue_request(decorator_id, is_approved_decorator=False)


@venue.route("/venue_catrers")
@login_required
@is_venue
def venue_catrers():
    """venue gets list of caterers who all had requested for business deal"""
    return venue_obj.get_venue_catrers_list(is_approved_caterer_by_venue=None)


@venue.route("/venue_accepted_catrers")
@login_required
@is_venue
def venue_accepted_catrers():
    """venue can get list of caterer whose request is accepted"""
    return venue_obj.get_venue_catrers_list(is_approved_caterer_by_venue=True)


@venue.route("/venue_rejected_catrers")
@login_required
@is_venue
def venue_rejected_catrers():
    """venue can get list of caterer whose request is rejected"""
    return venue_obj.get_venue_catrers_list(is_approved_caterer_by_venue=False)


@venue.route("/venue_accept_caterer_request/<int:caterer_id>")
def venue_accept_caterer_request(caterer_id):
    """venue accepts caterer's request"""
    return venue_obj.get_venue_caterer_request(caterer_id, is_approved_caterer=True)


@venue.route("/venue_reject_caterer_request/<int:caterer_id>")
def venue_reject_caterer_request(caterer_id):
    """venue rejects caterer's request"""
    return venue_obj.get_venue_caterer_request(caterer_id, is_approved_caterer=False)
