from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo, Email


class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),
                                             Email(),
                                             Length(min=6, max=254)])
    password = PasswordField('Password', validators=[DataRequired(),
                                                     Length(min=6, max=254)])
    confirm = PasswordField('Repeat Password',
                            validators=[DataRequired(),
                                        EqualTo('password')])


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),
                                             Email(),
                                             Length(min=6, max=40)])
    password = PasswordField('Password', validators=[DataRequired()])
