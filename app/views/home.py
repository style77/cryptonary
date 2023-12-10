from flask import Blueprint, abort, render_template
from jinja2 import TemplateNotFound

home_page = Blueprint("home", __name__, template_folder="templates")


@home_page.route("/")
def home():
    try:
        render_template("pages/index.html")
    except TemplateNotFound:
        abort(404)
