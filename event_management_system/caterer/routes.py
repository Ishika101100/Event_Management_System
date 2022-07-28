from flask import Blueprint
from flask_login import login_required

from event_management_system.caterer.services import CatererClass
from event_management_system.caterer.utils import is_caterer

caterer = Blueprint('caterer', __name__, template_folder='templates/caterer')

caterer_obj = CatererClass()


@caterer.route("/caterer_check_event")
@login_required
@is_caterer
def check_event():
    """Caterer can check events where he has served food"""
    return caterer_obj.get_event()


@caterer.route("/caterer_venues")
@login_required
@is_caterer
def venues():
    """caterer can check and add venues where he is providing service"""
    return caterer_obj.get_venues()


@caterer.route("/venue_get_caterer_request/<int:caterer_id>/<int:venue_id>")
def caterer_send_request(venue_id, caterer_id):
    """caterer sends request to venue for business deal"""
    return caterer_obj.get_caterer_send_request(venue_id, caterer_id)


@caterer.route("/caterer_category", methods=['GET', 'POST'])
@login_required
@is_caterer
def category():
    """caterer can add food category and it's charges"""
    return caterer_obj.get_caterer_category()


@caterer.route("/view_food_category")
@login_required
@is_caterer
def view_food_category():
    """caterer can view list of categories"""
    return caterer_obj.get_view_food_category()


@caterer.route("/update_caterer_category/<caterer_id>/<food_category_id>", methods=['GET', 'POST'])
@login_required
def update_category(caterer_id, food_category_id):
    """caterer can update category and it's charges"""
    return caterer_obj.get_update_category_for_caterer(caterer_id, food_category_id)


@caterer.route("/delete_caterer_category/<caterer_id>/<food_category_id>", methods=['GET', 'POST'])
@login_required
def delete_category(caterer_id, food_category_id):
    """caterer can delete category"""
    return caterer_obj.get_delete_category_for_caterer(caterer_id, food_category_id)
