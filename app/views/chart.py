from flask import Blueprint, abort, render_template
from jinja2 import TemplateNotFound
from sqlalchemy import asc, or_

from app.models.cryptocurrency import (
    CryptoCurrency,
    CryptoCurrencyForecastedPrice,
    CryptoCurrencyHistoricalPrice,
)
from app.services.database import db

chart_page = Blueprint("chart", __name__, template_folder="templates")


def get_crypto_by_symbol_or_name(query_term):
    result = (
        db.session.query(CryptoCurrency)
        .filter(
            or_(
                CryptoCurrency.symbol.ilike(f"%{query_term}%"),
                CryptoCurrency.name.ilike(f"%{query_term}%"),
            )
        )
        .first()
    )
    return result


def fetch_data(crypto: CryptoCurrency):
    historical_data = (
        CryptoCurrencyHistoricalPrice.query.filter_by(currency_id=crypto.id)
        .order_by(asc(CryptoCurrencyHistoricalPrice.date))
        .all()
    )

    last_date = None
    if historical_data:
        last_date = historical_data[-1].date
        historical_data = [row.as_dict() for row in historical_data]

    print(last_date)

    forecasted_data = []
    if last_date:
        forecasted_data = (
            CryptoCurrencyForecastedPrice.query.filter(
                CryptoCurrencyForecastedPrice.currency_id == crypto.id,
            )
            .order_by(CryptoCurrencyForecastedPrice.date)
            .all()
        )
        forecasted_data = [row.as_dict() for row in forecasted_data]

    return historical_data, forecasted_data


@chart_page.route("/chart/<crypto>")
def chart(crypto: str):
    crypto = get_crypto_by_symbol_or_name(crypto)
    if not crypto:
        abort(404)

    historical_data, forecasted_data = fetch_data(crypto)
    print(historical_data, forecasted_data)

    try:
        return render_template(
            "pages/chart.html",
            cryptocurrency=crypto,
            historical_data=historical_data,
            forecasted_data=forecasted_data,
        )
    except TemplateNotFound:
        print(12)
        abort(404)
