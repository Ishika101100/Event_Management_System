from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user

from event_management_system import db
from event_management_system.models import VenueGetDecorator, Decorator, Venues, VenueGetCaterer, Caterer, Event
from event_management_system.venue.forms import VenueInfo

venue = Blueprint('venue', __name__)


@venue.route("/venue_check_event")
@login_required
def check_event():
    """check booked events"""
    if current_user.user_type == 2:
        venue = Venues.query.filter_by(user_id=current_user.id).first()
        event_detail = Event.query.filter_by(venue_id=venue.id).filter_by(is_approved_by_venue=None).all()
        return render_template('venue_check_event.html',event_detail=event_detail)
    else:
        flash("Only venue can access this page")
        return redirect(url_for('main.home'))

@venue.route("/venue_accepted_event")
@login_required
def venue_accepted_event():
    """Check accepted event"""
    if current_user.user_type == 2:
        venue = Venues.query.filter_by(user_id=current_user.id).first()
        event_detail = Event.query.filter_by(venue_id=venue.id).filter_by(is_approved_by_venue=True).all()
        return render_template('venue_check_accepted_events.html',event_detail=event_detail)
    else:
        flash("Only venue can access this page")
        return redirect(url_for('main.home'))


@venue.route("/venue_rejected_event")
@login_required
def venue_rejected_event():
    """Check rejected events"""
    if current_user.user_type == 2:
        venue = Venues.query.filter_by(user_id=current_user.id).first()
        # current_time = datetime.datetime.now()
        event_detail = Event.query.filter_by(venue_id=venue.id).filter_by(is_approved_by_venue=False).all()
        return render_template('venue_check_rejected_events.html',event_detail=event_detail)
    else:
        flash("Only venue can access this page")
        return redirect(url_for('main.home'))




@venue.route("/venue_accept_booking_request/<int:event_id>")
def venue_accept_booking_request():
    """Venue accepts booking request"""
    venue_obj = Venues.query.filter_by(user_id=current_user.id).first()
    event_obj = Event.query.filter_by(venue_id=venue_obj.id).first()
    event_obj.is_approved_by_venue = True
    db.session.commit()
    return redirect(url_for('main.home'))

@venue.route("/venue_reject_booking_request/<int:event_id>")
def venue_reject_booking_request():
    """Venue rejects booking request"""
    venue_obj = Venues.query.filter_by(user_id=current_user.id).first()
    event_obj = Event.query.filter_by(venue_id=venue_obj.id).first()
    event_obj.is_approved_by_venue = False
    db.session.commit()
    return redirect(url_for('main.home'))



@venue.route("/venue_info", methods=['GET', 'POST'])
@login_required
def venue_info():
    """venue charges and capacity can be updated"""
    if current_user.user_type == 2:
        form = VenueInfo()
        venue = Venues.query.filter_by(user_id=current_user.id).first()
        if form.validate_on_submit():
            if current_user.id == venue.user_id:
                venue.charges = form.venue_charge.data
                venue.capacity = form.venue_capactity.data
                db.session.commit()
            return render_template('venue_info.html', form=form)
        elif request.method == 'GET':
            venue = Venues.query.filter(venue.user_id == Venues.user_id).first()
            form.venue_charge.data = venue.charges
            form.venue_capactity.data = venue.capacity
        return render_template('venue_info.html', form=form)
    else:
        flash("Only venue can access this page")
        return redirect(url_for('main.home'))


@venue.route("/venue_decorators")
@login_required
def venue_decorator():
    """venue gets list of decorator requests for business deal"""
    if current_user.user_type == 2:
        venue = Venues.query.filter_by(user_id=current_user.id).first()
        if current_user.id == venue.user_id:
            venue_get_decorator_obj = VenueGetDecorator.query.join(Decorator,
                                                                   VenueGetDecorator.decorator_id == Decorator.id).add_columns(
                Decorator.user_id).filter(VenueGetDecorator.decorator_id == Decorator.id).filter(
                VenueGetDecorator.venue_id == Venues.id).filter(Venues.user_id == current_user.id).filter(
                VenueGetDecorator.is_approved_decorator == None).all()
            decorator_username = {}
            decorator_email = {}
            decorator_mobile_number = {}
            decorator_address = {}

            for i in venue_get_decorator_obj:
                decorator = Decorator.query.filter_by(user_id=i.user_id).first()
                decorator_username[decorator.id] = decorator.user.username
                decorator_email[decorator.id] = decorator.user.email
                decorator_mobile_number[decorator.id] = decorator.user.mobile_number
                decorator_address[decorator.id] = decorator.user.address
            return render_template('venue_decorators.html', decorator=decorator_username,
                                   decorator_mobile_number=decorator_mobile_number, decorator_email=decorator_email,
                                   decorator_address=decorator_address)
        else:
            return render_template('venue_decorators.html')
    else:
        flash("Only venue can access this page")
        return redirect(url_for('main.home'))


@venue.route("/venue_accepted_decorators")
@login_required
def venue_accepted_decorators():
    """venue can get list of decorator whose request is accepted"""
    if current_user.user_type == 2:
        venue = Venues.query.filter_by(user_id=current_user.id).first()
        if current_user.id == venue.user_id:
            venue_get_decorator_obj = VenueGetDecorator.query.join(Decorator,
                                                                   VenueGetDecorator.decorator_id == Decorator.id).add_columns(
                Decorator.user_id).filter(VenueGetDecorator.decorator_id == Decorator.id).filter(
                VenueGetDecorator.venue_id == Venues.id).filter(Venues.user_id == current_user.id).filter(
                VenueGetDecorator.is_approved_decorator == True).all()

            decorator_username = {}
            decorator_email = {}
            decorator_mobile_number = {}
            decorator_address = {}

            for i in venue_get_decorator_obj:
                decorator = Decorator.query.filter_by(user_id=i.user_id).first()
                decorator_username[decorator.id] = decorator.user.username
                decorator_email[decorator.id] = decorator.user.email
                decorator_mobile_number[decorator.id] = decorator.user.mobile_number
                decorator_address[decorator.id] = decorator.user.address
            return render_template('venue_accepted_decorators.html', decorator=decorator_username,
                                   decorator_mobile_number=decorator_mobile_number, decorator_email=decorator_email,
                                   decorator_address=decorator_address)
        else:
            return render_template('venue_accepted_decorators.html')
    else:
        flash("Only venue can access this page")
        return redirect(url_for('main.home'))


@venue.route("/venue_rejected_decorators")
@login_required
def venue_rejected_decorators():
    """venue can get list of decorator whose request is rejected"""
    if current_user.user_type == 2:
        venue = Venues.query.filter_by(user_id=current_user.id).first()
        if current_user.id == venue.user_id:
            venue_get_decorator_obj = VenueGetDecorator.query.join(Decorator,
                                                                   VenueGetDecorator.decorator_id == Decorator.id).add_columns(
                Decorator.user_id).filter(VenueGetDecorator.decorator_id == Decorator.id).filter(
                VenueGetDecorator.venue_id == Venues.id).filter(Venues.user_id == current_user.id).filter(
                VenueGetDecorator.is_approved_decorator == False).all()

            decorator_username = {}
            decorator_email = {}
            decorator_mobile_number = {}
            decorator_address = {}

            for i in venue_get_decorator_obj:
                decorator = Decorator.query.filter_by(user_id=i.user_id).first()
                decorator_username[decorator.id] = decorator.user.username
                decorator_email[decorator.id] = decorator.user.email
                decorator_mobile_number[decorator.id] = decorator.user.mobile_number
                decorator_address[decorator.id] = decorator.user.address
            return render_template('venue_rejected_decorators.html', decorator=decorator_username,
                                   decorator_mobile_number=decorator_mobile_number, decorator_email=decorator_email,
                                   decorator_address=decorator_address)
        else:
            return render_template('venue_rejected_decorators.html')
    else:
        flash("Only venue can access this page")
        return redirect(url_for('main.home'))


@venue.route("/venue_accept_request/<int:decorator_id>")
def venue_accept_request(decorator_id):
    """venue accepts decorator's request"""
    venue_obj = Venues.query.filter_by(user_id=current_user.id).first()
    venue_get_decorator_obj = VenueGetDecorator.query.filter_by(venue_id=venue_obj.id,
                                                                decorator_id=decorator_id).first()
    venue_get_decorator_obj.is_approved_decorator = True
    db.session.commit()
    return redirect(url_for('main.home'))


@venue.route("/venue_reject_request/<int:decorator_id>")
def venue_reject_request(decorator_id):
    """venue rejects decorator's request"""
    venue_obj = Venues.query.filter_by(user_id=current_user.id).first()
    venue_get_decorator_obj = VenueGetDecorator.query.filter_by(venue_id=venue_obj.id,
                                                                decorator_id=decorator_id).first()
    venue_get_decorator_obj.is_approved_decorator = False
    db.session.commit()
    return redirect(url_for('main.home'))


@venue.route("/venue_catrers")
@login_required
def venue_catrers():
    """venue gets list of caterers who all had requested for business deal"""
    if current_user.user_type == 2:
        venue = Venues.query.filter_by(user_id=current_user.id).first()
        if current_user.id == venue.user_id:
            venue_get_caterer_obj = VenueGetCaterer.query.join(Caterer,
                                                               VenueGetCaterer.caterer_id == Caterer.id).add_columns(
                Caterer.user_id).filter(VenueGetCaterer.caterer_id == Caterer.id).filter(
                VenueGetCaterer.venue_id == Venues.id).filter(Venues.user_id == current_user.id).filter(
                VenueGetCaterer.is_approved_caterer == None).all()
            caterer_username = {}
            caterer_email = {}
            caterer_mobile_number = {}
            caterer_address = {}

            for i in venue_get_caterer_obj:
                caterer = Caterer.query.filter_by(user_id=i.user_id).first()
                caterer_username[caterer.id] = caterer.user.username
                caterer_email[caterer.id] = caterer.user.email
                caterer_mobile_number[caterer.id] = caterer.user.mobile_number
                caterer_address[caterer.id] = caterer.user.address
            return render_template('venue_catrers.html', caterer=caterer_username,
                                   caterer_mobile_number=caterer_mobile_number, caterer_email=caterer_email,
                                   caterer_address=caterer_address)
        else:
            return render_template('venue_catrers.html')
    else:
        flash("Only venue can access this page")
        return redirect(url_for('main.home'))


@venue.route("/venue_accepted_catrers")
@login_required
def venue_accepted_catrers():
    """venue can get list of caterer whose request is accepted"""
    if current_user.user_type == 2:
        venue = Venues.query.filter_by(user_id=current_user.id).first()
        if current_user.id == venue.user_id:
            venue_get_caterer_obj = VenueGetCaterer.query.join(Caterer,
                                                               VenueGetCaterer.caterer_id == Caterer.id).add_columns(
                Caterer.user_id).filter(VenueGetCaterer.caterer_id == Caterer.id).filter(
                VenueGetCaterer.venue_id == Venues.id).filter(Venues.user_id == current_user.id).filter(
                VenueGetCaterer.is_approved_caterer == True).all()
            caterer_username = {}
            caterer_email = {}
            caterer_mobile_number = {}
            caterer_address = {}

            for i in venue_get_caterer_obj:
                caterer = Caterer.query.filter_by(user_id=i.user_id).first()
                caterer_username[caterer.id] = caterer.user.username
                caterer_email[caterer.id] = caterer.user.email
                caterer_mobile_number[caterer.id] = caterer.user.mobile_number
                caterer_address[caterer.id] = caterer.user.address
            return render_template('venue_accepted_caterers.html', caterer=caterer_username,
                                   caterer_mobile_number=caterer_mobile_number, caterer_email=caterer_email,
                                   caterer_address=caterer_address)
        else:
            return render_template('venue_accepted_caterers.html')
    else:
        flash("Only venue can access this page")
        return redirect(url_for('main.home'))


@venue.route("/venue_rejected_catrers")
@login_required
def venue_rejected_catrers():
    """venue can get list of caterer whose request is rejected"""
    if current_user.user_type == 2:
        venue = Venues.query.filter_by(user_id=current_user.id).first()
        if current_user.id == venue.user_id:
            venue_get_caterer_obj = VenueGetCaterer.query.join(Caterer,
                                                               VenueGetCaterer.caterer_id == Caterer.id).add_columns(
                Caterer.user_id).filter(VenueGetCaterer.caterer_id == Caterer.id).filter(
                VenueGetCaterer.venue_id == Venues.id).filter(Venues.user_id == current_user.id).filter(
                VenueGetCaterer.is_approved_caterer == False).all()
            caterer_username = {}
            caterer_email = {}
            caterer_mobile_number = {}
            caterer_address = {}

            for i in venue_get_caterer_obj:
                caterer = Caterer.query.filter_by(user_id=i.user_id).first()
                caterer_username[caterer.id] = caterer.user.username
                caterer_email[caterer.id] = caterer.user.email
                caterer_mobile_number[caterer.id] = caterer.user.mobile_number
                caterer_address[caterer.id] = caterer.user.address
            return render_template('venue_rejected_caterers.html', caterer=caterer_username,
                                   caterer_mobile_number=caterer_mobile_number, caterer_email=caterer_email,
                                   caterer_address=caterer_address)
        else:
            return render_template('venue_rejected_caterers.html')
    else:
        flash("Only venue can access this page")
        return redirect(url_for('main.home'))


@venue.route("/venue_accept_caterer_request/<int:caterer_id>")
def venue_accept_caterer_request(caterer_id):
    """venue accepts caterer's request"""
    venue_obj = Venues.query.filter_by(user_id=current_user.id).first()
    venue_get_caterer_obj = VenueGetCaterer.query.filter_by(venue_id=venue_obj.id,
                                                            caterer_id=caterer_id).first()
    venue_get_caterer_obj.is_approved_caterer = True
    db.session.commit()
    return redirect(url_for('main.home'))


@venue.route("/venue_reject_caterer_request/<int:caterer_id>")
def venue_reject_caterer_request(caterer_id):
    """venue rejects caterer's request"""
    venue_obj = Venues.query.filter_by(user_id=current_user.id).first()
    venue_get_caterer_obj = VenueGetCaterer.query.filter_by(venue_id=venue_obj.id,
                                                            caterer_id=caterer_id).first()
    venue_get_caterer_obj.is_approved_caterer = False
    db.session.commit()
    return redirect(url_for('main.home'))
