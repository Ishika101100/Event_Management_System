from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user

from event_management_system import db
from event_management_system.models import Venues, Caterer, VenueGetCaterer

caterer = Blueprint('caterer', __name__)


@caterer.route("/caterer_check_event")
@login_required
def check_event():
    """Caterer can check events where he has served food"""
    if current_user.user_type == 4:
        return render_template('caterer_check_events.html')
    else:
        flash("Only caterer can access this page")
        return redirect(url_for('main.home'))


@caterer.route("/caterer_venues")
@login_required
def venues():
    """Caterer can check and add venues where he is providing service"""
    if current_user.user_type == 4:
        get_venues_for_caterer = Venues.query.all()
        current_caterer = Caterer.query.filter_by(user_id=current_user.id).first()
        venue_get_caterer_obj_true = VenueGetCaterer.query.filter_by(caterer_id=current_caterer.id).filter_by(
            is_approved_caterer=True).with_entities(VenueGetCaterer.venue_id, VenueGetCaterer.is_approved_caterer).all()
        venue_get_caterer_obj_false = VenueGetCaterer.query.filter_by(caterer_id=current_caterer.id).filter_by(
            is_approved_caterer=False).with_entities(VenueGetCaterer.venue_id,
                                                     VenueGetCaterer.is_approved_caterer).all()
        venue_get_caterer_obj_none = VenueGetCaterer.query.filter_by(caterer_id=current_caterer.id).filter_by(
            is_approved_caterer=None).with_entities(VenueGetCaterer.venue_id, VenueGetCaterer.is_approved_caterer).all()
        venue_get_caterer_obj_true_list = [i[0] for i in venue_get_caterer_obj_true]
        venue_get_caterer_obj_false_list = [i[0] for i in venue_get_caterer_obj_false]
        venue_get_caterer_obj_none_list = [i[0] for i in venue_get_caterer_obj_none]
        return render_template('caterer_venues.html', get_venues_for_caterer=get_venues_for_caterer,
                               caterer=current_caterer.id,
                               venue_get_caterer_obj_true_list=venue_get_caterer_obj_true_list,
                               venue_get_caterer_obj_false_list=venue_get_caterer_obj_false_list,
                               venue_get_caterer_obj_none_list=venue_get_caterer_obj_none_list)

    else:
        flash("Only caterer can access this page")
        return redirect(url_for('main.home'))


@caterer.route("/venue_get_caterer_request/<int:caterer_id>/<int:venue_id>")
def caterer_send_request(venue_id, caterer_id):
    """Caterer sends request to venue for business deal"""
    venue_query = VenueGetCaterer(venue_id=venue_id, caterer_id=caterer_id)
    db.session.add(venue_query)
    db.session.commit()
    return redirect(url_for('main.home'))


@caterer.route("/caterer_category")
@login_required
def category():
    """Caterer can add food category and it's charges"""
    if current_user.user_type == 4:
        return render_template('caterer_category.html')
    else:
        flash("Only caterer can access this page")
        return redirect(url_for('main.home'))
