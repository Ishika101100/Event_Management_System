from flask import Blueprint
from flask_login import login_required

from event_management_system.users.services import register_user, signin_user, log_user_out, user_account, \
    get_reset_request, get_reset_token, get_change_password, get_home, get_about

users = Blueprint('users', __name__, template_folder='templates', static_folder='static/users')


@users.route("/register", methods=['GET', 'POST'])
def register():
    return register_user()


@users.route("/login", methods=['GET', 'POST'])
def login():
    return signin_user()


@users.route("/logout")
def logout():
    return log_user_out()


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    return user_account()


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    return get_reset_request()


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    return get_reset_token(token)


@users.route("/change_password", methods=['GET', 'POST'])
@login_required
def change_password():
    return get_change_password()


@users.route("/")
@users.route("/home")
def home():
    """returns home page"""
    return get_home()


@users.route("/about")
def about():
    """returns about page"""
    return get_about()
