from flask import render_template, redirect, url_for, request

from event_management_system.book_event.models import event_detail_for_caterer
from event_management_system.caterer.forms import CatererAddCategoryForm
from event_management_system.caterer.models import get_current_caterer, get_food_category, get_food_charges, \
    get_caterer_query, charge_query_for_caterer, food_category_query
from event_management_system.users.models import add_function, commit_function, delete_function
from event_management_system.venue.models import get_all_venues, venue_get_caterer_obj_for_caterer, \
    venue_get_caterer_query


def get_event():
    caterer = get_current_caterer()
    event_detail = event_detail_for_caterer(caterer_id=caterer.id)
    return render_template('caterer_check_events.html', event_detail=event_detail)

def get_venues():
    get_venues_for_caterer = get_all_venues()
    current_caterer = get_current_caterer()
    venue_get_caterer_obj_true =venue_get_caterer_obj_for_caterer(caterer_id=current_caterer.id,is_approved_caterer=True)
    venue_get_caterer_obj_false = venue_get_caterer_obj_for_caterer(caterer_id=current_caterer.id,is_approved_caterer=False)
    venue_get_caterer_obj_none = venue_get_caterer_obj_for_caterer(caterer_id=current_caterer.id,is_approved_caterer=None)
    venue_get_caterer_obj_true_list = [i[0] for i in venue_get_caterer_obj_true]
    venue_get_caterer_obj_false_list = [i[0] for i in venue_get_caterer_obj_false]
    venue_get_caterer_obj_none_list = [i[0] for i in venue_get_caterer_obj_none]
    return render_template('caterer_venues.html', get_venues_for_caterer=get_venues_for_caterer,
                           caterer=current_caterer.id,
                           venue_get_caterer_obj_true_list=venue_get_caterer_obj_true_list,
                           venue_get_caterer_obj_false_list=venue_get_caterer_obj_false_list,
                           venue_get_caterer_obj_none_list=venue_get_caterer_obj_none_list)

def get_caterer_send_request(venue_id,caterer_id):
    venue_query = venue_get_caterer_query(venue_id=venue_id, caterer_id=caterer_id)
    add_function(venue_query)
    commit_function()
    return redirect(url_for('users.home'))

def get_caterer_category():
    form = CatererAddCategoryForm()
    if form.validate_on_submit():
        caterer =get_current_caterer()
        food_category = get_food_category(food_type=form.food_type.data)
        add_function(food_category)
        commit_function()
        food_charges = get_food_charges(caterer_id=caterer.id, food_category_id=food_category.id,
                                               charges=form.food_charges.data)
        add_function(food_charges)
        commit_function()
        return redirect(url_for('users.home'))
    return render_template('caterer_category.html', form=form, title="Caterer_category")

def get_view_food_category():
    caterer = get_current_caterer()
    get_caterer = get_caterer_query(caterer_id=caterer.id)
    return render_template('view_caterer_category.html', get_caterer=get_caterer)

def get_update_category_for_caterer(caterer_id,food_category_id):
    form = CatererAddCategoryForm()
    charge = charge_query_for_caterer(caterer_id=caterer_id,food_category_id=food_category_id)
    category = food_category_query(food_category_id=food_category_id)
    if form.validate_on_submit():
        charge.charges = form.food_charges.data
        category.food_type = form.food_type.data
        commit_function()
        return render_template('caterer_category.html', form=form)
    elif request.method == 'GET':
        form.food_charges.data = charge.charges
        form.food_type.data = category.food_type
    return render_template('caterer_category.html', form=form, title="Decoration_category")

def get_delete_category_for_caterer(caterer_id,food_category_id):
    form = CatererAddCategoryForm()
    charge = charge_query_for_caterer(caterer_id=caterer_id,food_category_id=food_category_id)
    category = food_category_query(food_category_id=food_category_id)
    delete_function(charge)
    commit_function()
    delete_function(category)
    commit_function()
    return render_template('view_caterer_category.html', form=form)