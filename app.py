"""Flask App Blueprint"""
from flask import Flask, render_template, flash, redirect, request, url_for, Markup
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func, and_
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_login import login_user, current_user, login_required, logout_user
import os, datetime
from datetime import datetime

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

from models import Items, User
from forms import ItemsForm, RegisterForm, LoginForm, EditItemsForm

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == int(user_id)).first()

@app.route('/', methods=['GET', 'POST'])
@login_required
def home():
    """Render homepage"""

    all_user_items = Items.query.filter_by(user_id=current_user.id)
    return render_template('home.html', items=all_user_items)


@app.route('/all_items', methods=['GET', 'POST'])
@login_required
def all_items():
    """Render homepage"""
    all_user_items = Items.query.filter_by(user_id=current_user.id)
    return render_template('all_items.html', items=all_user_items)


@app.route('/add_item', methods=['GET', 'POST'])
@login_required
def add_item():
    form = ItemsForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                new_item = Items(form.name.data, form.notes.data, current_user.id)
                db.session.add(new_item)
                db.session.commit()
                message = Markup("<strong>Well done!</strong> Item added successfully!")
                flash(message, 'success')
                return redirect(url_for('home'))
            except:
                db.session.rollback()
                message = Markup("<strong>Oh snap!</strong>! Unable to add item.")
                flash(message, 'danger')
    return render_template('add_item.html', form=form)


@app.route('/edit_item/<items_id>', methods=['GET', 'POST'])
@login_required
def edit_item(items_id):
    form = EditItemsForm(request.form)
    item_with_user = db.session.query(Items, User).join(User).filter(Items.id == items_id).first()
    if item_with_user is not None:
        if current_user.is_authenticated and item_with_user.Items.user_id == current_user.id:
            if request.method == 'POST':
                if form.validate_on_submit():
                    try:
                        item = Items.query.get(items_id)
                        item.name = form.name.data
                        item.notes = form.notes.data
                        db.session.commit()
                        message = Markup("Item edited successfully!")
                        flash(message, 'success')
                        return redirect(url_for('home'))
                    except:
                        db.session.rollback()
                        message = Markup("<strong>Error!</strong> Unable to edit item.")
                        flash(message, 'danger')
            return render_template('edit_item.html', item=item_with_user, form=form)
        else:
            message = Markup("<strong>Error!</strong> Incorrect permissions to access this item.")
            flash(message, 'danger')
    else:
        message = Markup("<strong>Error!</strong> Item does not exist.")
        flash(message, 'danger')
    return redirect(url_for('home'))


@app.route('/register', methods=['GET', 'POST'])
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
                message = Markup("<strong>Success!</strong> Thanks for registering.")
                flash(message, 'success')
                return redirect(url_for('home'))
            except IntegrityError:
                db.session.rollback()
                message = Markup("<strong>Error!</strong> Unable to process registration.")
                flash(message, 'danger')
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
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
                message = Markup("<strong>Welcome back!</strong> You are now successfully logged in.")
                flash(message, 'success')
                return redirect(url_for('home'))
            else:
                message = Markup("<strong>Error!</strong> Incorrect login credentials.")
                flash(message, 'danger')
    return render_template('login.html', form=form)


@app.route('/user_profile', methods=['GET', 'POST'])
@login_required
def user_profile():
    return render_template('user_profile.html')


@app.route('/logout')
@login_required
def logout():
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    message = Markup("<strong>Goodbye!</strong> You are now logged out.")
    flash(message, 'info')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run()
