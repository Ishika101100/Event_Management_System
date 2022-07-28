from flask import Blueprint
from flask_login import login_required

from event_management_system.users.services import UserClass

users = Blueprint('users', __name__, template_folder='templates', static_folder='static/users')

user_obj = UserClass()


@users.route("/register", methods=['GET', 'POST'])
def register():
    """
    user gets registration form for creating an account
    """
    return user_obj.register_user()


@users.route("/login", methods=['GET', 'POST'])
def login():
    """user is able to log in into the website"""
    return user_obj.signin_user()


@users.route("/logout")
def logout():
    """user can logout from the website"""
    return user_obj.log_user_out()


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    """user is able to see his account details"""
    return user_obj.user_account()


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    """user can reset password if he/she forgot his old password"""
    return user_obj.get_reset_request()


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    """a token is sent to user's email for resetting the password"""
    return user_obj.get_reset_token(token)


@users.route("/change_password", methods=['GET', 'POST'])
@login_required
def change_password():
    """user can change his/her password for logging into the website"""
    return user_obj.get_change_password()


@users.route("/")
@users.route("/home")
def home():
    """returns home page"""
    return user_obj.get_home()


@users.route("/about")
def about():
    """returns about page"""
    return user_obj.get_about()
