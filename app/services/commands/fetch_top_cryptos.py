import requests

from app.models.cryptocurrency import CryptoCurrency, CryptoCurrencyDetails
from app.services.database import transaction
from flask import current_app

API_URL = "https://api.coingecko.com/api/v3/coins/markets"


def fetch_top_currencies(limit):
    r = requests.get(API_URL, params={
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": limit,
        "page": "1",
        "sparkline": "false",
        "locale": "en",
        "x_cg_demo_api_key": current_app.config["COINGECKO_API_KEY"]
    })
    data = r.json()

    for crypto in data:
        with transaction() as session:
            currency = CryptoCurrency(
                id=crypto["id"],
                name=crypto["name"],
                symbol=crypto["symbol"],
                image=crypto.get("image")
            )
            session.add(currency)

            details = CryptoCurrencyDetails(
                market_cap=crypto["market_cap"],
                market_cap_rank=crypto["market_cap_rank"],
                circulating_supply=crypto["circulating_supply"],
                max_supply=crypto["max_supply"],
                currency_id=currency.id
            )

            session.add(details)

    current_app.logger.info(f"Inserted {len(data)} in to database.")
