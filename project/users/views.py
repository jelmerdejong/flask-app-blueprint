# project/users/views.py

# IMPORTS
from datetime import timedelta

from flask import Blueprint, abort, current_app, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from itsdangerous import BadSignature, URLSafeTimedSerializer
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError

from .forms import RegisterForm, LoginForm, EmailForm, PasswordForm
from project.extensions import db
from project.mailers import send_email
from project.models import User
from project.time_utils import utc_now


# CONFIG
users_blueprint = Blueprint('users', __name__, template_folder='templates')


def send_confirmation_email(user_email):
    confirm_serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])

    confirm_url = url_for(
        'users.confirm_email',
        token=confirm_serializer.dumps(user_email, salt='email-confirmation-salt'),
        _external=True)

    html = render_template(
        'email_confirmation.html',
        confirm_url=confirm_url)

    send_email('Confirm Your Email Address', [user_email], html)


def send_password_reset_email(user_email):
    password_reset_serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])

    password_reset_url = url_for(
        'users.reset_with_token',
        token=password_reset_serializer.dumps(user_email, salt='password-reset-salt'),
        _external=True)

    html = render_template(
        'email_password_reset.html',
        password_reset_url=password_reset_url)

    send_email('Password Reset Requested', [user_email], html)


def get_user_by_email(email):
    return db.session.scalar(select(User).where(User.email == email))


# ROUTES
@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                new_user = User(
                    form.email.data,
                    form.password.data,
                    email_confirmation_sent_on=utc_now(),
                )
                new_user.authenticated = True
                db.session.add(new_user)
                db.session.commit()
                send_confirmation_email(new_user.email)
                message = "Success! Thanks for registering. Please check your email to confirm your email address."
                flash(message, 'success')
                return redirect(url_for('home'))
            except IntegrityError:
                db.session.rollback()
                message = "Error! Unable to process registration."
                flash(message, 'danger')
    return render_template('register.html', form=form)


@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            user = get_user_by_email(form.email.data)
            if user is not None and user.is_correct_password(form.password.data):
                if user.is_email_confirmed is not True:
                    send_confirmation_email(user.email)
                    user.email_confirmation_sent_on = utc_now()
                    user.authenticated = False
                    db.session.add(user)
                    db.session.commit()
                    message = "Email sent to confirm your email address. Please check your inbox!"
                    flash(message, 'success')
                    return redirect(url_for('users.login'))
                if user.is_email_confirmed is True:
                    user.authenticated = True
                    user.last_logged_in = user.current_logged_in
                    user.current_logged_in = utc_now()
                    db.session.add(user)
                    db.session.commit()
                    login_user(user)
                    message = "Welcome back! You are now successfully logged in."
                    flash(message, 'success')
                    return redirect(url_for('home'))
            else:
                message = "Error! Incorrect login credentials."
                flash(message, 'danger')
    return render_template('login.html', form=form)


@users_blueprint.route('/user_profile', methods=['GET', 'POST'])
@login_required
def user_profile():
    return render_template('user_profile.html')


@users_blueprint.route('/confirm/<token>')
def confirm_email(token):
    try:
        confirm_serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        email = confirm_serializer.loads(token, salt='email-confirmation-salt', max_age=3600)
    except BadSignature:
        message = "The confirmation link is invalid or has expired."
        flash(message, 'danger')
        return redirect(url_for('users.login'))

    user = get_user_by_email(email)

    if user.email_confirmed:
        message = "Account already confirmed. Please login."
        flash(message, 'info')
    else:
        user.email_confirmed = True
        user.email_confirmed_on = utc_now()
        db.session.add(user)
        db.session.commit()
        message = "Thank you for confirming your email address!"
        flash(message, 'success')

    return redirect(url_for('home'))


@users_blueprint.route('/reset', methods=["GET", "POST"])
def reset():
    form = EmailForm()
    if form.validate_on_submit():
        user = get_user_by_email(form.email.data)
        if user is None:
            message = "Invalid email address!"
            flash(message, 'danger')
            return render_template('password_reset_email.html', form=form)
        if user.email_confirmed:
            send_password_reset_email(user.email)
            message = "Please check your email for a password reset link."
            flash(message, 'success')
        else:
            message = "Your email address must be confirmed before attempting a password reset."
            flash(message, 'danger')
        return redirect(url_for('users.login'))

    return render_template('password_reset_email.html', form=form)


@users_blueprint.route('/reset/<token>', methods=["GET", "POST"])
def reset_with_token(token):
    try:
        password_reset_serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        email = password_reset_serializer.loads(token, salt='password-reset-salt', max_age=3600)
    except BadSignature:
        message = "The password reset link is invalid or has expired."
        flash(message, 'danger')
        return redirect(url_for('users.login'))

    form = PasswordForm()

    if form.validate_on_submit():
        user = get_user_by_email(email)
        if user is None:
            message = "Invalid email address!"
            flash(message, 'danger')
            return redirect(url_for('users.login'))

        user.password = form.password.data
        db.session.add(user)
        db.session.commit()
        message = "Your password has been updated!"
        flash(message, 'success')
        return redirect(url_for('users.login'))

    return render_template('reset_password_with_token.html', form=form, token=token)


@users_blueprint.route('/admin_view_users')
@login_required
def admin_view_users():
    if current_user.role != 'admin':
        abort(403)
    else:
        users = db.session.scalars(select(User).order_by(User.id)).all()
        return render_template('admin_view_users.html', users=users)


@users_blueprint.route('/admin_dashboard')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        abort(403)
    else:
        users = db.session.scalars(select(User).order_by(User.id)).all()
        kpi_mau = db.session.scalar(
            select(func.count(User.id)).where(User.last_logged_in > (utc_now() - timedelta(days=30)))
        ) or 0
        kpi_total_confirmed = db.session.scalar(
            select(func.count(User.id)).where(User.email_confirmed.is_(True))
        ) or 0
        kpi_mau_percentage = 0 if kpi_total_confirmed == 0 else (100 / kpi_total_confirmed) * kpi_mau
        return render_template('admin_dashboard.html', users=users, kpi_mau=kpi_mau, kpi_total_confirmed=kpi_total_confirmed, kpi_mau_percentage=kpi_mau_percentage)


@users_blueprint.route('/logout', methods=['POST'])
@login_required
def logout():
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    message = "Goodbye! You are now logged out."
    flash(message, 'info')
    return redirect(url_for('users.login'))


@users_blueprint.route('/password_change', methods=["GET", "POST"])
@login_required
def user_password_change():
    form = PasswordForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = current_user
            user.password = form.password.data
            db.session.add(user)
            db.session.commit()
            message = "Password has been updated!"
            flash(message, 'success')
            return redirect(url_for('users.user_profile'))

    return render_template('password_change.html', form=form)


@users_blueprint.route('/email_change', methods=["GET", "POST"])
@login_required
def user_email_change():
    form = EmailForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                user_check = get_user_by_email(form.email.data)
                if user_check is None:
                    user = current_user
                    user.email = form.email.data
                    user.email_confirmed = False
                    user.email_confirmed_on = None
                    user.email_confirmation_sent_on = utc_now()
                    db.session.add(user)
                    db.session.commit()
                    send_confirmation_email(user.email)
                    message = "Email changed! Please confirm your new email address (link sent to new email)."
                    flash(message, 'success')
                    return redirect(url_for('users.user_profile'))
                else:
                    message = "Sorry, that email already exists!"
                    flash(message, 'danger')
            except IntegrityError:
                db.session.rollback()
                message = "Sorry, that email already exists!"
                flash(message, 'danger')
    return render_template('email_change.html', form=form)
