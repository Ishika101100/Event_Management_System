from flask import Blueprint
from flask_login import login_required

from event_management_system.decorator.services import DecoratorClass
from event_management_system.decorator.utils import is_decorator

decorator = Blueprint('decorator', __name__, template_folder='templates/decorator')

decorator_obj = DecoratorClass()


@decorator.route("/decorator_check_event")
@login_required
@is_decorator
def check_decorator_event():
    """Decorator can check events where he has decorated the venues"""
    return decorator_obj.get_decorator_event()


@decorator.route("/decorator_venues")
@login_required
@is_decorator
def decorator_venues():
    """Decorator can check and add venues where he is providing service"""
    return decorator_obj.get_decorator_venues()


@decorator.route("/venue_get_request/<int:decorator_id>/<int:venue_id>")
def decorator_send_request(venue_id, decorator_id):
    """Decorator sends request to venue for business deal"""
    return decorator_obj.get_decorator_send_request(venue_id, decorator_id)


@decorator.route("/decorator_category", methods=['GET', 'POST'])
@login_required
@is_decorator
def category():
    """Decorator can add category and it's charges"""
    return decorator_obj.get_category()


@decorator.route("/update_category/<decorator_id>/<decorator_type_id>", methods=['GET', 'POST'])
@login_required
def update_category(decorator_id, decorator_type_id):
    """Decorator can update category and it's charges"""
    return decorator_obj.get_update_category(decorator_id, decorator_type_id)


@decorator.route("/delete_category/<decorator_id>/<decorator_type_id>", methods=['GET', 'POST'])
@login_required
def delete_category(decorator_id, decorator_type_id):
    """Decorator can delete category"""
    return decorator_obj.get_delete_category(decorator_id, decorator_type_id)


@decorator.route("/view_decoration_category")
@login_required
@is_decorator
def view_decoration_type():
    """decorator can view list of categories"""
    return decorator_obj.get_decoration_type()
