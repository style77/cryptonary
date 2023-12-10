from flask import Blueprint, abort, render_template
from jinja2 import TemplateNotFound
from app.models.cryptocurrency import CryptoCurrency

home_page = Blueprint("home", __name__, template_folder="templates")


@home_page.route("/")
def home():
    rising_cryptocurrencies = CryptoCurrency.query.filter_by(is_rising=True).all()
    print(rising_cryptocurrencies[0].details[0])

    try:
        return render_template(
            "pages/index.html", rising_cryptocurrencies=rising_cryptocurrencies
        )
    except TemplateNotFound:
        abort(404)
