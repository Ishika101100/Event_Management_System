from wtforms import ValidationError
from wtforms.fields import datetime


def no_of_guests_validation(self, field):
    """No of guests validation"""
    if not field.data > 0:
        raise ValidationError("No of guests can't be negative")


def validate_date(self, field):
    """Date validation of book event. User can only book events of dates after today's date"""
    if self.field.data < datetime.datetime.now().date():
        raise ValidationError('You can only book for day after today.')
