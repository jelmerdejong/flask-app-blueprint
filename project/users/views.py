# project/users/views.py

# IMPORTS
from flask import render_template, Blueprint, request, redirect, url_for, flash, Markup
from sqlalchemy.exc import IntegrityError
from flask_login import login_user, current_user, login_required, logout_user
from datetime import datetime

from .forms import RegisterForm, LoginForm
from project import db
from project.models import User


# CONFIG
users_blueprint = Blueprint('users', __name__, template_folder='templates')


# ROUTES
@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                new_user = User(form.email.data, form.password.data)
                new_user.authenticated = True
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user)
                message = Markup(
                    "<strong>Success!</strong> Thanks for registering.")
                flash(message, 'success')
                return redirect(url_for('home'))
            except IntegrityError:
                db.session.rollback()
                message = Markup(
                    "<strong>Error!</strong> Unable to process registration.")
                flash(message, 'danger')
    return render_template('register.html', form=form)


@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user is not None and user.is_correct_password(form.password.data):
                user.authenticated = True
                user.last_logged_in = user.current_logged_in
                user.current_logged_in = datetime.now()
                db.session.add(user)
                db.session.commit()
                login_user(user)
                message = Markup(
                    "<strong>Welcome back!</strong> You are now successfully logged in.")
                flash(message, 'success')
                return redirect(url_for('home'))
            else:
                message = Markup(
                    "<strong>Error!</strong> Incorrect login credentials.")
                flash(message, 'danger')
    return render_template('login.html', form=form)


@users_blueprint.route('/user_profile', methods=['GET', 'POST'])
@login_required
def user_profile():
    return render_template('user_profile.html')


@users_blueprint.route('/logout')
@login_required
def logout():
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    message = Markup("<strong>Goodbye!</strong> You are now logged out.")
    flash(message, 'info')
    return redirect(url_for('users.login'))
