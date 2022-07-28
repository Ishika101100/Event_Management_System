import re

from flask_login import current_user
from wtforms import ValidationError

from event_management_system.users.constants import INVALID_USERNAME_MESSAGE, INVALID_EMAIL_MESSAGE, \
    EMAIL_NOT_AVAILABLE_MESSAGE, INVALID_MOBILE_NUMBER_MESSAGE, INCORRECT_MOBILE_NUMBER_FORMAT, AGE_VALIDATION, \
    INCORRECT_PASSWORD_FORMAT
from event_management_system.users.models import User


def validate_username(self, field):
    """Validates if provided username exists in the database or not."""
    user = User.validate_name(username=field.data)
    if user:
        raise ValidationError(INVALID_USERNAME_MESSAGE)


def validate_update_username(self, field):
    """Validates if provided username exists in the database or not."""
    if field.data != current_user.username:
        user = User.validate_name(username=field.data)
        if user:
            raise ValidationError(INVALID_USERNAME_MESSAGE)


def validate_email(self, field):
    """Validates if provided email exists in the database or not."""
    user = User.validate_email(email=field.data)
    if user:
        raise ValidationError(INVALID_EMAIL_MESSAGE)


def validate_email_exists(self, field):
    user = User.validate_email(email=field.data)
    if user is None:
        raise ValidationError(EMAIL_NOT_AVAILABLE_MESSAGE)


def validate_number(self, field):
    """Validates if provided mobile number exists in the database or not."""
    user = User.validate_number(mobile_number=field.data)
    if user:
        raise ValidationError(INVALID_MOBILE_NUMBER_MESSAGE)


def validate_update_number(self, field):
    if field.data != current_user.mobile_number:
        user = User.validate_number(mobile_number=field.data)
        if user:
            raise ValidationError(INVALID_MOBILE_NUMBER_MESSAGE)


def phone_number_validation(self, field):
    """phone number validation"""
    if field.data.isnumeric():
        regex = r'[7-9][0-9]{9}'
        if not (re.fullmatch(regex, field.data)):
            raise ValidationError(INCORRECT_MOBILE_NUMBER_FORMAT)


def age_validation(self, field):
    """age validation"""
    if not field.data > 13:
        raise ValidationError(AGE_VALIDATION)


def password_validation(self, field):
    """password validation"""
    regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,18}$'
    if not re.fullmatch(regex, field.data):
        raise ValidationError(INCORRECT_PASSWORD_FORMAT)
