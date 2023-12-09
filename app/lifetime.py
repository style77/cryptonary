from flask import Flask

from app.cli import crypto_cli
from app.services.database import db


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.settings.Settings')

    # app.register_blueprint(urls, url_prefix="/")

    db.init_app(app)

    with app.app_context():
        # if app.config["DEBUG"]:
        #     db.drop_all()
        db.create_all()

    app.cli.add_command(crypto_cli)

    return app
