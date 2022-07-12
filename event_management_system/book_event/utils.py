import datetime
from datetime import date
from wtforms import ValidationError


def validate_date(self, field):
    """Date validation of book event. User can only book events of dates after today's date"""
    if field.data < date.today()+datetime.timedelta(days=1):
        raise ValidationError('You can only book for day after today.')
