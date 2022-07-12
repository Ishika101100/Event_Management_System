from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length


class CatererAddCategoryForm(FlaskForm):
    """Decorator add category form"""
    food_type = StringField('Category Title', validators=[DataRequired(), Length(min=2, max=20)])
    food_charges = IntegerField('Charges', validators=[DataRequired()])
    submit = SubmitField('Submit')
