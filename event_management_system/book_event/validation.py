import datetime
from datetime import date

from wtforms import ValidationError

from event_management_system.book_event.constants import DATE_VALIDATION_ERROR_MESSAGE


def validate_date(self, field):
    """Date validation of book event. User can only book events of dates after today's date"""
    if field.data < date.today() + datetime.timedelta(days=1):
        raise ValidationError(DATE_VALIDATION_ERROR_MESSAGE)
