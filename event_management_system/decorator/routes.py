from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user

from event_management_system import db
from event_management_system.decorator.forms import AddCategoryForm
from event_management_system.models import Venues, VenueGetDecorator, Decorator, DecoratorType, DecoratorGetTypes, Event

decorator = Blueprint('decorator', __name__)


@decorator.route("/decorator_check_event")
@login_required
def check_decorator_event():
    """Decorator can check events where he has decorated the venues"""
    if current_user.user_type == 3:
        decorator = Decorator.query.filter_by(user_id=current_user.id).first()
        event_detail = Event.query.filter_by(decorator_id=decorator.id).all()
        return render_template('decorator_check_event.html',event_detail=event_detail)
    else:
        flash("Only decorator can access this page")
        return redirect(url_for('main.home'))


@decorator.route("/decorator_venues")
@login_required
def decorator_venues():
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
        return render_template('decorator_venues.html', get_venues=get_venues,
                               decorator=current_decorator.id,
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


@decorator.route("/decorator_category", methods=['GET', 'POST'])
@login_required
def category():
    """Decorator can add category and it's charges"""
    if current_user.user_type == 3:
        form = AddCategoryForm()
        if form.validate_on_submit():
            decorator = Decorator.query.filter_by(user_id=current_user.id).first()
            decor_category = DecoratorType(decoration_type=form.decoration_type.data)
            db.session.add(decor_category)
            db.session.commit()
            decor_charges = DecoratorGetTypes(decorator_id=decorator.id, decoration_type_id=decor_category.id,
                                              charges=form.category_charges.data)
            db.session.add(decor_charges)
            db.session.commit()
            return redirect(url_for('main.home'))
        return render_template('decorator_category.html', form=form, title="Decoration_category")
    else:
        flash("Only decorator can access this page")
        return redirect(url_for('main.home'))


@decorator.route("/update_category/<decorator_id>/<decorator_type_id>", methods=['GET', 'POST'])
@login_required
def update_category(decorator_id, decorator_type_id):
    """Decorator can update category and it's charges"""
    if current_user.user_type == 3:
        form = AddCategoryForm()
        charge = DecoratorGetTypes.query.filter_by(decorator_id=decorator_id,
                                                   decoration_type_id=decorator_type_id).first()
        category = DecoratorType.query.filter_by(id=decorator_type_id).first()
        if form.validate_on_submit():
            charge.charges = form.category_charges.data
            category.decoration_type = form.decoration_type.data
            db.session.commit()
            return render_template('decorator_category.html', form=form)
        elif request.method == 'GET':
            form.category_charges.data = charge.charges
            form.decoration_type.data = category.decoration_type
        return render_template('decorator_category.html', form=form, title="Decoration_category")
    else:
        flash("Only decorator can access this page")
        return redirect(url_for('main.home'))


@decorator.route("/delete_category/<decorator_id>/<decorator_type_id>", methods=['GET', 'POST'])
@login_required
def delete_category(decorator_id, decorator_type_id):
    """Decorator can delete category"""
    if current_user.user_type == 3:
        form = AddCategoryForm()
        charge = DecoratorGetTypes.query.filter_by(decorator_id=decorator_id,
                                                   decoration_type_id=decorator_type_id).first()
        category = DecoratorType.query.filter_by(id=decorator_type_id).first()
        db.session.delete(charge)
        db.session.commit()
        db.session.delete(category)
        db.session.commit()
        return render_template('view_decorator_category.html', form=form)
    else:
        flash("Only decorator can access this page")
        return redirect(url_for('main.home'))


@decorator.route("/view_decoration_category")
@login_required
def view_decoration_type():
    """decorator can view list of categories"""
    if current_user.user_type == 3:
        decorator = Decorator.query.filter_by(user_id=current_user.id).first()
        get_decorator = DecoratorGetTypes.query.filter_by(decorator_id=decorator.id).all()
        return render_template('view_decorator_category.html', get_decorator=get_decorator)
    else:
        flash("Only decorator can access this page")
        return redirect(url_for('main.home'))
