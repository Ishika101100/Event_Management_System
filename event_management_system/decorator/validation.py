from wtforms import ValidationError

from event_management_system.decorator.constants import NEGATIVE_VALUE_MESSAGE


def number_input_validation(self, field):
    """age validation"""
    if not field.data > 0:
        raise ValidationError(NEGATIVE_VALUE_MESSAGE)
