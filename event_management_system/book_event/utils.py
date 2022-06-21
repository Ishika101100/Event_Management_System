from wtforms import ValidationError
from wtforms.fields import datetime


def no_of_guests_validation(self, field):
    if not field.data > 0:
        raise ValidationError("Age can't be negative")

def validate_date(self, field):
    if self.field.data < datetime.datetime.now().date():
        raise ValidationError('You can only book for day after today.')