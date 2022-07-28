from flask import url_for, render_template, flash, request
from flask_login import current_user, login_user, logout_user
from werkzeug.utils import redirect

from event_management_system import bcrypt
from event_management_system.book_event.models import EventCategory
from event_management_system.caterer.models import Caterer
from event_management_system.decorator.models import Decorator
from event_management_system.users.constants import ACCOUNT_CREATE_MESSAGE, SUCCESSFUL_LOGIN, UPDATE_ACCOUNT_MESSAGE, \
    SEND_EMAIL_FOR_RESET_PASSWORD, EXPIRE_TOKEN_MESSAGE, UPDATE_PASSWORD_MESSAGE, PASSWORD_CHANGE_MESSAGE, \
    INCORRECT_OLD_PASSWORD_MESSAGE
from event_management_system.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, \
    ResetPasswordForm, ChangePasswordForm
from event_management_system.users.models import User, UserType
from event_management_system.users.utils import get_hashed_password, save_picture, send_reset_email
from event_management_system.venue.models import Venues


class UserClass:
    @staticmethod
    def register_user():
        """User can register by providing his/her details"""
        if current_user.is_authenticated:
            return redirect(url_for('users.home'))
        form = RegistrationForm()
        get_user_type_obj = UserType.get_user_type()
        get_venue_type_obj = EventCategory.get_event_category()
        if form.validate_on_submit():
            hashed_password = get_hashed_password(form.password.data)
            user_obj = User.save_user(form, hashed_password)
            if user_obj.user_type == 2:
                Venues.save_venue(user_obj.id)
            elif user_obj.user_type == 3:
                Decorator.save_decorator(user_obj.id)
            elif user_obj.user_type == 4:
                Caterer.save_caterer(user_obj.id)
            flash(ACCOUNT_CREATE_MESSAGE, 'success')
            return redirect(url_for('users.login'))

        return render_template('users/register.html', title='Register', form=form, get_user_type=get_user_type_obj,
                               get_venue_type=get_venue_type_obj)

    @staticmethod
    def signin_user():
        """User can login by providing email address and password"""
        if current_user.is_authenticated:
            return redirect(url_for('users.home'))
        form = LoginForm()
        if form.validate_on_submit():
            user = User.get_user_from_email(form.email.data)
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('users.home'))
            else:
                flash(SUCCESSFUL_LOGIN, 'danger')
        return render_template('users/login.html', title='Login', form=form)

    @staticmethod
    def log_user_out():
        """User can log out himself from the app"""
        logout_user()
        return redirect(url_for('users.home'))

    @staticmethod
    def user_account():
        """user can update his/her account"""
        form = UpdateAccountForm()
        if form.validate_on_submit():
            if form.picture.data:
                picture_file = save_picture(form.picture.data)
                User.update_image(picture_file)
            User.update_account_function(username=form.username.data, mobile_number=form.mobile_number.data,
                                         address=form.address.data)
            flash(UPDATE_ACCOUNT_MESSAGE, 'success')
            return redirect(url_for('users.account'))
        elif request.method == 'GET':
            form.username.data = current_user.username
            form.mobile_number.data = current_user.mobile_number
            form.address.data = current_user.address
        image_file = url_for('users.static', filename='profile_pics/' + current_user.image_file)
        return render_template('users/account.html', title='Account',
                               image_file=image_file, form=form)

    @staticmethod
    def get_reset_request():
        """An email for reset password id sent to email address provided by the user"""
        if current_user.is_authenticated:
            return redirect(url_for('users.home'))
        form = RequestResetForm()
        if form.validate_on_submit():
            user = User.get_user_from_email(form.email.data)
            send_reset_email(user)
            flash(SEND_EMAIL_FOR_RESET_PASSWORD, 'info')
            return redirect(url_for('users.login'))
        return render_template('users/reset_request.html', title='Reset Password', form=form)

    @staticmethod
    def get_reset_token(token):
        """A token is sent in the email address provided by user for password reset."""
        if current_user.is_authenticated:
            return redirect(url_for('users.home'))
        user = User.verify_reset_token(token)
        if not user:
            flash(EXPIRE_TOKEN_MESSAGE, 'warning')
            return redirect(url_for('users.reset_request'))
        form = ResetPasswordForm()
        if form.validate_on_submit():
            hashed_password = get_hashed_password(form.password.data)
            User.update_user_password(hashed_password)
            flash(UPDATE_PASSWORD_MESSAGE, 'success')
            return redirect(url_for('users.login'))
        return render_template('users/reset_token.html', title='Reset Password', form=form)

    def get_change_password(self):
        """User can change his/her password by providing old password, new password and confirm password"""
        form = ChangePasswordForm()
        if form.validate_on_submit():
            if bcrypt.check_password_hash(current_user.password, form.old_password.data):
                hashed_password = get_hashed_password(form.password.data)
                current_user.password = hashed_password
                get_hashed_password
                self.log_user_out()
                flash(PASSWORD_CHANGE_MESSAGE, 'success')
                return redirect(url_for('users.login'))
            else:
                flash(INCORRECT_OLD_PASSWORD_MESSAGE, 'danger')
        return render_template('users/change_password.html', title='Change Password', form=form)

    @staticmethod
    def get_home():
        """home page of website """
        return render_template('users/home.html')

    @staticmethod
    def get_about():
        """About page of website"""
        return render_template('users/about.html', title='About')
