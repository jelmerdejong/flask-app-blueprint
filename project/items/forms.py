from flask_wtf import FlaskForm
from wtforms import TextField
from wtforms.validators import DataRequired, Length


class ItemsForm(FlaskForm):
    name = TextField('Name', validators=[DataRequired(),
                                         Length(min=1, max=254)])
    notes = TextField('Notes')


class EditItemsForm(FlaskForm):
    name = TextField('Name', validators=[DataRequired(),
                                         Length(min=1, max=254)])
    notes = TextField('Notes')
