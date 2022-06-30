from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required

from event_management_system import db, bcrypt
from event_management_system.models import User, UserType, EventCategory, Venues, Decorator, Caterer
from event_management_system.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, \
    ResetPasswordForm, ChangePasswordForm
from event_management_system.users.utils import send_reset_email, save_picture

users = Blueprint('users', __name__)


@users.route("/register", methods=['GET', 'POST'])
def register():
    """User needs to register by providing his/her user type"""
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = RegistrationForm()
    get_user_type = UserType.query.all()
    get_venue_type = EventCategory.query.all()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, user_type=form.user_type.data, email=form.email.data,
                    password=hashed_password,
                    mobile_number=form.mobile_number.data, address=form.address.data)
        db.session.add(user)
        db.session.commit()
        if user.user_type == 2:
            venue = Venues(venue_type=request.form.get('event_category'), capacity=request.form.get('event_capacity'),
                           charges=request.form.get('event_charges'), user_id=user.id)
            db.session.add(venue)
            db.session.commit()
        elif user.user_type == 3:
            decorator = Decorator(user_id=user.id)
            db.session.add(decorator)
            db.session.commit()
        elif user.user_type == 4:
            caterer = Caterer(user_id=user.id)
            db.session.add(caterer)
            db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form, get_user_type=get_user_type,
                           get_venue_type=get_venue_type)


@users.route("/login", methods=['GET', 'POST'])
def login():
    """User can login by providing email address and password"""
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@users.route("/logout")
def logout():
    """User can log out himself from the app"""
    logout_user()
    return redirect(url_for('main.home'))


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    """user can update his/her account"""
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.mobile_number.data = current_user.mobile_number
        form.address.data = current_user.address
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    """An email for reset password id sent to email address provided by the user"""
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    """A token is sent in the email address provided by user for password reset."""
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if not user:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)


@users.route("/change_password", methods=['GET', 'POST'])
@login_required
def change_password():
    """User can change his/her password by providing old password, new password and confirm password"""
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if bcrypt.check_password_hash(current_user.password, form.old_password.data):
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            current_user.password = hashed_password
            db.session.commit()
            logout()
            flash("Password Changed Successfully! Please login again!", 'success')
            return redirect(url_for('users.login'))
        else:
            flash("Incorrect Old Password", 'danger')
    return render_template('change_password.html', title='Change Password', form=form)
