from wtforms import ValidationError


def number_input_validation(self,field):
    """age validation"""
    if not field.data > 0:
        raise ValidationError("Negative value is not possible")