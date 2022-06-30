from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user

from event_management_system import db
from event_management_system.models import Venues, VenueGetDecorator, Decorator

decorator = Blueprint('decorator', __name__)


@decorator.route("/decorator_check_event")
@login_required
def check_event():
    """Decorator can check events where he has decorated the venues"""
    if current_user.user_type == 3:
        return render_template('decorator_check_event.html')
    else:
        flash("Only decorator can access this page")
        return redirect(url_for('main.home'))


@decorator.route("/decorator_venues")
@login_required
def venues():
    """Decorator can check and add venues where he is providing service"""
    if current_user.user_type == 3:
        get_venues = Venues.query.all()
        current_decorator = Decorator.query.filter_by(user_id=current_user.id).first()
        venue_get_decorator_obj_true = VenueGetDecorator.query.filter_by(decorator_id=current_decorator.id).filter_by(
            is_approved_decorator=True).with_entities(VenueGetDecorator.venue_id,
                                                      VenueGetDecorator.is_approved_decorator).all()
        venue_get_decorator_obj_false = VenueGetDecorator.query.filter_by(decorator_id=current_decorator.id).filter_by(
            is_approved_decorator=False).with_entities(VenueGetDecorator.venue_id,
                                                       VenueGetDecorator.is_approved_decorator).all()
        venue_get_decorator_obj_none = VenueGetDecorator.query.filter_by(decorator_id=current_decorator.id).filter_by(
            is_approved_decorator=None).with_entities(VenueGetDecorator.venue_id,
                                                      VenueGetDecorator.is_approved_decorator).all()
        venue_get_decorator_obj_true_list = [i[0] for i in venue_get_decorator_obj_true]
        venue_get_decorator_obj_false_list = [i[0] for i in venue_get_decorator_obj_false]
        venue_get_decorator_obj_none_list = [i[0] for i in venue_get_decorator_obj_none]
        return render_template('decorator_venues.html', get_venues=get_venues, decorator=current_decorator.id,
                               venue_get_decorator_obj_true_list=venue_get_decorator_obj_true_list,
                               venue_get_decorator_obj_false_list=venue_get_decorator_obj_false_list,
                               venue_get_decorator_obj_none_list=venue_get_decorator_obj_none_list)
    else:
        flash("Only decorator can access this page")
        return redirect(url_for('main.home'))


@decorator.route("/venue_get_request/<int:decorator_id>/<int:venue_id>")
def decorator_send_request(venue_id, decorator_id):
    """Decorator sends request to venue for business deal"""
    a = VenueGetDecorator(venue_id=venue_id, decorator_id=decorator_id)
    db.session.add(a)
    db.session.commit()
    return redirect(url_for('main.home'))


@decorator.route("/decorator_category")
@login_required
def category():
    """Decorator can add category and it's charges"""
    if current_user.user_type == 3:
        return render_template('decorator_category.html')
    else:
        flash("Only decorator can access this page")
        return redirect(url_for('main.home'))
