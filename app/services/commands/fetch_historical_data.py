import time
import math
from typing import List
import requests
from datetime import datetime
from app.models.cryptocurrency import CryptoCurrency, CryptoCurrencyHistoricalPrice
from app.services.database import db
from flask import current_app
from sqlalchemy.exc import IntegrityError


API_URL = "https://api.coingecko.com/api/v3/coins/{id}/market_chart"

# Since CoinGecko got 30/min api cooldown, the only way to fetch data without proxies is to do that in batch
PER_MINUTE = 30


def _get_protocol(ip: str):
    ip = ip.lower()
    match ip:
        case ip.startswith("https://"):
            return "https"
        case ip.startswith("http://"):
            return "http"
        case _:
            raise ValueError(f"Unexpected proxy protocol: {ip}")


def fetch_historical():
    # even though proxies list variable is meant to be constant
    # it needs to be under function, because current_app can be only used in
    # app context
    records: List[CryptoCurrency] = CryptoCurrency.query.all()

    PROXIES = current_app.config["PROXIES"]
    if PROXIES and math.ceil(len(PROXIES) / 30) < len(records):
        raise Exception(
            f"{len(PROXIES)} proxies is not enough to fetch {len(records)} records."
        )

    print(len(records))

    i = 0
    iteration = 0
    for record in records:
        if i >= PER_MINUTE and not PROXIES:
            time.sleep(61)  # Just in case
            i = 0
            iteration += 1

        proxy = None
        if PROXIES:
            proxy_address = PROXIES[iteration]
            protocol = _get_protocol(proxy_address)
            proxy = {protocol: proxy_address.replace(protocol, "")}

        r = requests.get(
            API_URL.format(id=record.id),
            params={
                "vs_currency": "usd",
                "days": "max",
                "x_cg_demo_api_key": current_app.config["COINGECKO_API_KEY"],
            },
            proxies=proxy,
        )

        data = r.json()

        # We could use transaction in here, but small piece of data is better than no data
        for row in data["prices"]:
            date = datetime.fromtimestamp(row[0] / 1000)
            print(f"INSERTING {record.symbol} {date}: {row[1]}")
            try:
                history = CryptoCurrencyHistoricalPrice(
                    currency_id=record.id,
                    timestamp=date,
                    price=row[1],
                )
                db.session.add(history)
            except Exception:
                break
            finally:
                db.session.commit()

        i += 1

        current_app.logger.info(
            f"Inserted {len(data)} for {record.name} ({record.symbol})"
        )
