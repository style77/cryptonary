import time
import math
from typing import List
import requests
from datetime import datetime
from app.models.cryptocurrency import CryptoCurrency, CryptoCurrencyHistoricalPrice
from app.services.database import db
from flask import current_app
from requests.exceptions import RequestException
from app.services.commands.common import setup_logger


API_URL = "https://api.coingecko.com/api/v3/coins/{id}/market_chart"

# Since CoinGecko got 30/min api cooldown, the only way to fetch data without proxies is to do that in batch
PER_MINUTE = 30
INTERVAL = 61


def get_key(enough_keys: bool, i: int, keys: list):
    if enough_keys and i >= PER_MINUTE:
        return keys[i]  # WARNING: UNTESTED - LACK OF KEYS
    else:
        return keys[0]


def fetch_data(record_id, key):
    r = requests.get(
        API_URL.format(id=record_id),
        params={
            "vs_currency": "usd",
            "days": "max",
            "x_cg_demo_api_key": key,
        },
    )

    if r.status_code == 429:
        current_app.logger.warning(f"429 interuppted fetching data. Sleeping {INTERVAL} seconds.")
        time.sleep(INTERVAL)
        return fetch_data()

    if not r.ok:
        r.raise_for_status()

    return r.json()


def fetch_historical_data():
    setup_logger(current_app)

    # even though proxies list variable is meant to be constant
    # it needs to be under function, because current_app can be only used in
    # app context
    records: List[CryptoCurrency] = CryptoCurrency.query.all()

    keys = current_app.config["COINGECKO_API_KEYS"]
    enough_keys = True
    if keys and math.ceil(len(keys) / 30) < len(records):
        enough_keys = False
        current_app.logger.warning(
            f"{len(keys)} is not enough keys to fetch data without sleeping."
        )

    global_start_time = time.time()

    i = 0
    for record in records:
        local_start_time = time.time()

        key = get_key(enough_keys, i, keys)

        data = fetch_data(record.id, key)

        # We could use transaction in here, but small piece of data is better than no data
        for row in reversed(data["prices"]):
            date = datetime.fromtimestamp(row[0] / 1000)
            current_app.logger.debug(f"INSERTING {record.symbol} {date}: {row[1]}")

            existing_record = CryptoCurrencyHistoricalPrice.query.filter_by(
                currency_id=record.id, timestamp=date
            ).first()
            if existing_record:
                current_app.logger.debug(f"Skipping {record.symbol}")
                print("Skipping")
                break

            history = CryptoCurrencyHistoricalPrice(
                currency_id=record.id,
                timestamp=date,
                price=row[1],
            )
            db.session.add(history)

        current_app.logger.info(
            f"Inserted {len(data['prices'])} prices for {record.name} ({record.symbol.upper()}) since {date}"
        )
        current_app.logger.info(
            f"Inserted {record.symbol} in {round(time.time() - local_start_time, 2)}s"
        )

        db.session.commit()

    try:
        current_app.logger.info(
            f"Inserted all of cryptos in {round(time.time() - global_start_time, 2)}s"
        )
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Failed to commit changes to the database: {e}")
