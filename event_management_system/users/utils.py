import os
import re
import secrets

from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from wtforms import ValidationError

from event_management_system import mail


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)


def phone_number_validation(self, field):
    if field.data.isnumeric():
        regex = r'[7-9][0-9]{9}'
        if not (re.fullmatch(regex, field.data)):
            raise ValidationError("Invalid phone number")


def age_validation(self, field):
    if not field.data > 13:
        raise ValidationError("Age must be greater than 13")


def password_validation(self, field):
    regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,18}$'
    if not re.fullmatch(regex, field.data):
        raise ValidationError("Password should consist One Capital Letter,Special Character,One Number,Length 8-18")
