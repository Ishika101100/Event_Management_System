import os
import secrets
from functools import wraps

from PIL import Image
from flask import url_for, current_app, flash, redirect
from flask_login import current_user
from flask_mail import Message

from event_management_system import mail, bcrypt


def save_picture(form_picture):
    """save picture validation"""
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'users/static/users/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


def get_hashed_password(password):
    return bcrypt.generate_password_hash(password).decode('utf-8')


def send_reset_email(user):
    """send reset password email validation"""
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)


def is_user(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        if current_user.user_type == 1:
            return f()
        flash("Only users can access this page", "warning")
        return redirect(url_for('main.home'))

    return wrapped
