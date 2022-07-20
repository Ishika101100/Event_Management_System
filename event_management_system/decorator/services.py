from flask import render_template, url_for, redirect, request

from event_management_system.book_event.models import get_event_details_for_decorator
from event_management_system.decorator.forms import AddCategoryForm
from event_management_system.decorator.models import get_current_decorator, \
    get_decor_category, decor_get_types, get_decor_charges, \
    get_decorator_type, get_decoration_category
from event_management_system.users.models import add_function, commit_function, delete_function
from event_management_system.venue.models import get_all_venues, get_venue_get_decorator_obj_for_decorator, \
    venue_get_decorator_query_for_decorator


def get_decorator_event():
    decorator = get_current_decorator()
    event_detail = get_event_details_for_decorator(decorator_id=decorator.id)
    return render_template('decorator_check_event.html', event_detail=event_detail)


def get_decorator_venues():
    get_venues = get_all_venues()
    current_decorator = get_current_decorator()
    venue_get_decorator_obj_true = venue_get_decorator_query_for_decorator(decorator_id=current_decorator.id,
                                                                           is_approved_decorator=True)
    venue_get_decorator_obj_false = venue_get_decorator_query_for_decorator(decorator_id=current_decorator.id,
                                                                            is_approved_decorator=False)
    venue_get_decorator_obj_none = venue_get_decorator_query_for_decorator(decorator_id=current_decorator.id,
                                                                           is_approved_decorator=None)
    venue_get_decorator_obj_true_list = [i[0] for i in venue_get_decorator_obj_true]
    venue_get_decorator_obj_false_list = [i[0] for i in venue_get_decorator_obj_false]
    venue_get_decorator_obj_none_list = [i[0] for i in venue_get_decorator_obj_none]
    return render_template('decorator_venues.html', get_venues=get_venues,
                           decorator=current_decorator.id,
                           venue_get_decorator_obj_true_list=venue_get_decorator_obj_true_list,
                           venue_get_decorator_obj_false_list=venue_get_decorator_obj_false_list,
                           venue_get_decorator_obj_none_list=venue_get_decorator_obj_none_list)


def get_decorator_send_request(venue_id, decorator_id):
    """Decorator sends request to venue for business deal"""
    venue_get_decorator_obj = get_venue_get_decorator_obj_for_decorator(venue_id, decorator_id)
    add_function(venue_get_decorator_obj)
    commit_function()
    return redirect(url_for('users.home'))


def get_category():
    form = AddCategoryForm()
    if form.validate_on_submit():
        decorator = get_current_decorator()
        decor_category = get_decor_category(decoration_type=form.decoration_type.data)
        add_function(decor_category)
        commit_function()
        decor_charges = decor_get_types(decorator_id=decorator.id, decoration_type_id=decor_category.id,
                                        charges=form.category_charges.data)
        add_function(decor_charges)
        commit_function()
        return redirect(url_for('users.home'))
    return render_template('decorator_category.html', form=form, title="Decoration_category")


def get_update_category(decorator_id, decorator_type_id):
    form = AddCategoryForm()
    charge = get_decor_charges(decorator_id=decorator_id, decoration_type_id=decorator_type_id)
    category = get_decoration_category(decorator_type_id=decorator_type_id)
    if form.validate_on_submit():
        charge.charges = form.category_charges.data
        category.decoration_type = form.decoration_type.data
        commit_function()
        return render_template('decorator_category.html', form=form)
    elif request.method == 'GET':
        form.category_charges.data = charge.charges
        form.decoration_type.data = category.decoration_type
    return render_template('decorator_category.html', form=form, title="Decoration_category")


def get_delete_category(decorator_id, decorator_type_id):
    form = AddCategoryForm()
    charge = get_decor_charges(decorator_id=decorator_id, decoration_type_id=decorator_type_id)
    category = get_decoration_category(decorator_type_id=decorator_type_id)
    delete_function(charge)
    commit_function()
    delete_function(category)
    commit_function()
    return render_template('view_decorator_category.html', form=form)


def get_decoration_type():
    decorator = get_current_decorator()
    get_decorator = get_decorator_type(decorator_id=decorator.id)
    return render_template('view_decorator_category.html', get_decorator=get_decorator)
