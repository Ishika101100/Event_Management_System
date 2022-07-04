from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user

from event_management_system import db
from event_management_system.caterer.forms import CatererAddCategoryForm
from event_management_system.models import Venues, Caterer, VenueGetCaterer, FoodCategory, CatererGetFoodCategory

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


@caterer.route("/caterer_category",methods=['GET', 'POST'])
@login_required
def category():
    """Caterer can add food category and it's charges"""
    if current_user.user_type == 4:
        if current_user.user_type == 4:
            form = CatererAddCategoryForm()
            if form.validate_on_submit():
                caterer = Caterer.query.filter_by(user_id=current_user.id).first()
                food_category = FoodCategory(food_type=form.food_type.data)
                db.session.add(food_category)
                db.session.commit()
                decor_charges = CatererGetFoodCategory(caterer_id=caterer.id, food_category_id=food_category.id,
                                                  charges=form.food_charges.data)
                db.session.add(decor_charges)
                db.session.commit()
                return redirect(url_for('main.home'))
            return render_template('caterer_category.html', form=form, title="Caterer_category")
        else:
            flash("Only caterer can access this page")
            return redirect(url_for('main.home'))
        return render_template('caterer_category.html')
    else:
        flash("Only caterer can access this page")
        return redirect(url_for('main.home'))

@caterer.route("/view_food_category")
@login_required
def view_food_category():
    """caterer can view list of categories"""
    if current_user.user_type == 4:
        caterer = Caterer.query.filter_by(user_id=current_user.id).first()
        get_caterer = CatererGetFoodCategory.query.filter_by(caterer_id=caterer.id).all()
        return render_template('view_caterer_category.html', get_caterer=get_caterer)
    else:
        flash("Only caterer can access this page")
        return redirect(url_for('main.home'))

@caterer.route("/update_caterer_category/<caterer_id>/<food_category_id>", methods=['GET', 'POST'])
@login_required
def update_category(caterer_id, food_category_id):
    """Decorator can update category and it's charges"""
    if current_user.user_type == 4:
        form = CatererAddCategoryForm()
        charge = CatererGetFoodCategory.query.filter_by(caterer_id=caterer_id,
                                                   food_category_id=food_category_id).first()
        category = FoodCategory.query.filter_by(id=food_category_id).first()
        if form.validate_on_submit():
            charge.charges = form.food_charges.data
            category.food_type = form.food_type.data
            db.session.commit()
            return render_template('caterer_category.html', form=form)
        elif request.method == 'GET':
            form.food_charges.data = charge.charges
            form.food_type.data = category.food_type
        return render_template('caterer_category.html', form=form, title="Decoration_category")
    else:
        flash("Only caterer can access this page")
        return redirect(url_for('main.home'))


@caterer.route("/delete_caterer_category/<caterer_id>/<food_category_id>", methods=['GET', 'POST'])
@login_required
def delete_category(caterer_id, food_category_id):
    if current_user.user_type == 4:
        """Decorator can delete category"""
        form = CatererAddCategoryForm()
        charge = CatererGetFoodCategory.query.filter_by(caterer_id=caterer_id,
                                                   food_category_id=food_category_id).first()
        category = FoodCategory.query.filter_by(id=food_category_id).first()
        db.session.delete(charge)
        db.session.commit()
        db.session.delete(category)
        db.session.commit()
        return render_template('view_caterer_category.html', form=form)
    else:
        flash("Only caterer can access this page")
        return redirect(url_for('main.home'))

