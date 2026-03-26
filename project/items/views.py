# project/items/views.py

# IMPORTS
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from project.extensions import db
from project.models import Item
from .forms import ItemForm


# CONFIG
items_blueprint = Blueprint('items', __name__, template_folder='templates')


# ROUTES
@items_blueprint.route('/all_items', methods=['GET', 'POST'])
@login_required
def all_items():
    """Render homepage"""
    all_user_items = db.session.scalars(
        select(Item).where(Item.user_id == current_user.id).order_by(Item.id)
    ).all()
    return render_template('all_items.html', items=all_user_items)


@items_blueprint.route('/add_item', methods=['GET', 'POST'])
@login_required
def add_item():
    form = ItemForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                new_item = Item(form.name.data, form.notes.data, current_user.id)
                db.session.add(new_item)
                db.session.commit()
                message = "Well done! Item added successfully!"
                flash(message, 'success')
                return redirect(url_for('home'))
            except SQLAlchemyError:
                db.session.rollback()
                message = "Oh snap! Unable to add item."
                flash(message, 'danger')
    return render_template('add_item.html', form=form)


@items_blueprint.route('/edit_item/<int:items_id>', methods=['GET', 'POST'])
@login_required
def edit_item(items_id):
    form = ItemForm(request.form)
    item = db.session.get(Item, items_id)

    if item is None:
        message = "Error! Item does not exist."
        flash(message, 'danger')
        return redirect(url_for('home'))

    if current_user.is_authenticated and item.user_id == current_user.id:
        if request.method == 'POST':
            if form.validate_on_submit():
                try:
                    item.name = form.name.data
                    item.notes = form.notes.data
                    db.session.commit()
                    message = "Item edited successfully!"
                    flash(message, 'success')
                    return redirect(url_for('home'))
                except SQLAlchemyError:
                    db.session.rollback()
                    message = "Error! Unable to edit item."
                    flash(message, 'danger')
        return render_template('edit_item.html', item=item, form=form)

    message = "Error! Incorrect permissions to access this item."
    flash(message, 'danger')
    return redirect(url_for('home'))


@items_blueprint.route('/delete_item/<int:items_id>', methods=['POST'])
@login_required
def delete_item(items_id):
    item = db.get_or_404(Item, items_id)

    if not item.user_id == current_user.id:
        message = "Error! Incorrect permissions to delete this item."
        flash(message, 'danger')
        return redirect(url_for('home'))

    try:
        db.session.delete(item)
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        flash('Unable to delete {}.'.format(item.name), 'danger')
        return redirect(url_for('items.all_items'))

    flash('{} was deleted.'.format(item.name), 'success')
    return redirect(url_for('items.all_items'))
