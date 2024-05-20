from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length


class ItemsForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(),
                                         Length(min=1, max=254)])
    notes = StringField('Notes')


class EditItemsForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(),
                                         Length(min=1, max=254)])
    notes = StringField('Notes')
