from flask import url_for, render_template, flash, request
from flask_login import current_user, login_user, logout_user
from werkzeug.utils import redirect

from event_management_system import bcrypt
from event_management_system.caterer.models import save_caterer
from event_management_system.decorator.models import save_decorator
from event_management_system.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, \
    ResetPasswordForm, ChangePasswordForm
from event_management_system.users.models import get_user_type, get_venue_type, User, save_user, get_user_from_email, \
    commit_function
from event_management_system.users.utils import get_hashed_password, save_picture, send_reset_email
from event_management_system.venue.models import save_venue


def register_user():
    if current_user.is_authenticated:
        return redirect(url_for('users.home'))
    form = RegistrationForm()
    get_user_type_obj = get_user_type()
    get_venue_type_obj = get_venue_type()
    if form.validate_on_submit():
        hashed_password = get_hashed_password(form.password.data)
        user_obj = save_user(form, hashed_password)
        if user_obj.user_type == 2:
            save_venue(user_obj.id)
        elif user_obj.user_type == 3:
            save_decorator(user_obj.id)
        elif user_obj.user_type == 4:
            save_caterer(user_obj.id)
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('users.login'))

    return render_template('users/register.html', title='Register', form=form, get_user_type=get_user_type_obj,
                           get_venue_type=get_venue_type_obj)


def signin_user():
    """User can login by providing email address and password"""
    if current_user.is_authenticated:
        return redirect(url_for('users.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = get_user_from_email(form.email.data)
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('users.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('users/login.html', title='Login', form=form)


def log_user_out():
    """User can log out himself from the app"""
    logout_user()
    return redirect(url_for('users.home'))


def user_account():
    """user can update his/her account"""
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.mobile_number = form.mobile_number.data
        current_user.address = form.address.data
        commit_function()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.mobile_number.data = current_user.mobile_number
        form.address.data = current_user.address
    image_file = url_for('users.static', filename='profile_pics/' + current_user.image_file)
    return render_template('users/account.html', title='Account',
                           image_file=image_file, form=form)


def get_reset_request():
    """An email for reset password id sent to email address provided by the user"""
    if current_user.is_authenticated:
        return redirect(url_for('users.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = get_user_from_email(form.email.data)
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('users/reset_request.html', title='Reset Password', form=form)


def get_reset_token(token):
    """A token is sent in the email address provided by user for password reset."""
    if current_user.is_authenticated:
        return redirect(url_for('users.home'))
    user = User.verify_reset_token(token)
    if not user:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = get_hashed_password(form.password.data)
        user.password = hashed_password
        commit_function()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('users/reset_token.html', title='Reset Password', form=form)


def get_change_password():
    """User can change his/her password by providing old password, new password and confirm password"""
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if bcrypt.check_password_hash(current_user.password, form.old_password.data):
            hashed_password = get_hashed_password(form.password.data)
            current_user.password = hashed_password
            get_hashed_password
            log_user_out()
            flash("Password Changed Successfully! Please login again!", 'success')
            return redirect(url_for('users.login'))
        else:
            flash("Incorrect Old Password", 'danger')
    return render_template('users/change_password.html', title='Change Password', form=form)


def get_home():
    return render_template('users/home.html')


def get_about():
    return render_template('users/about.html', title='About')
