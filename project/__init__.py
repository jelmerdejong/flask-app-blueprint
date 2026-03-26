import os

from flask import Flask, render_template
from flask_login import current_user, login_required
from flask_wtf.csrf import CSRFError
from sqlalchemy import select

from project.extensions import bcrypt, csrf, db, login_manager, mail, migrate


def _get_config_object(config_object=None):
    return config_object or os.environ.get("APP_SETTINGS", "config.DevelopmentConfig")


def create_app(config_object=None, config_overrides=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(_get_config_object(config_object))

    if config_overrides:
        app.config.update(config_overrides)

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    mail.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)

    from project.models import Item
    from project.users.views import users_blueprint
    from project.items.views import items_blueprint

    app.register_blueprint(users_blueprint)
    app.register_blueprint(items_blueprint)

    register_routes(app, Item)
    register_error_handlers(app)

    return app


@login_manager.user_loader
def load_user(user_id):
    from project.models import User

    try:
        return db.session.get(User, int(user_id))
    except (TypeError, ValueError):
        return None


def register_routes(app, item_model):
    @app.route("/", methods=["GET", "POST"])
    @login_required
    def home():
        """Render homepage."""
        all_user_items = db.session.scalars(
            select(item_model).where(item_model.user_id == current_user.id).order_by(item_model.id)
        ).all()
        return render_template("home.html", items=all_user_items)


def register_error_handlers(app):
    @app.errorhandler(CSRFError)
    def handle_csrf_error(error):
        return render_template("400.html", error_message=error.description), 400

    @app.errorhandler(400)
    def bad_request(error):
        description = getattr(error, "description", "Bad request.")
        return render_template("400.html", error_message=description), 400

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("404.html"), 404

    @app.errorhandler(403)
    def page_forbidden(error):
        return render_template("403.html"), 403

    @app.errorhandler(410)
    def page_gone(error):
        return render_template("410.html"), 410


app = create_app()
