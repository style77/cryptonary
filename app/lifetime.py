from flask import Flask

from app.cli import crypto_cli
from app.services.database import db
from app.views.urls import views
from app.utils import format_currency


def create_app():
    app = Flask(__name__)
    app.config.from_object("app.settings.Settings")

    for view in views:
        app.register_blueprint(view)

    db.init_app(app)

    app.template_filter("format_currency")(lambda value: format_currency(value))

    with app.app_context():
        # if app.config["DEBUG"]:
        #     db.drop_all()
        db.create_all()

    app.cli.add_command(crypto_cli)

    return app
