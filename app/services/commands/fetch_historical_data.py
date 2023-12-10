from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import math
from typing import List
import requests
from datetime import datetime
from app.models.cryptocurrency import CryptoCurrency, CryptoCurrencyHistoricalPrice
from app.services.database import db
from flask import current_app
from app.services.commands.common import setup_logger

API_URL = "https://api.coingecko.com/api/v3/coins/{id}/market_chart"

# Since CoinGecko got 30/min api cooldown, the only way to fetch data without proxies is to do that in batch
PER_MINUTE = 30
INTERVAL = 61


def get_key(enough_keys: bool, i: int, keys: list):
    if enough_keys and i >= PER_MINUTE:
        key_idx = i // PER_MINUTE
        if key_idx >= len(keys):
            key_idx = len(keys)
        return keys[key_idx]  # WARNING: UNTESTED - LACK OF KEYS
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
        return fetch_data(record_id, key)

    if not r.ok:
        r.raise_for_status()

    return r.json()


def fetch_historical_data():
    setup_logger(current_app)

    records: List[CryptoCurrency] = CryptoCurrency.query.all()
    keys = current_app.config["COINGECKO_API_KEYS"]
    enough_keys = True

    if keys and math.ceil(len(keys) / 30) < len(records):
        enough_keys = False
        current_app.logger.warning(
            f"{len(keys)} keys are not enough to fetch data without sleeping."
        )

    global_start_time = time.time()

    def process_record(app_context, record):
        app_context.push()
        local_start_time = time.time()
        i = 0
        skipped = False

        key = get_key(enough_keys, i, keys)
        data = fetch_data(record.id, key)

        try:
            with db.session.begin():
                for row in reversed(data["prices"]):
                    date = datetime.fromtimestamp(row[0] / 1000).date()
                    current_app.logger.debug(f"Inserting {record.symbol.upper()} {date}: {row[1]}")

                    existing_record = CryptoCurrencyHistoricalPrice.query.filter_by(
                        currency_id=record.id, date=date
                    ).first()

                    if existing_record:
                        current_app.logger.warning(f"Skipping {record.symbol.upper()}, record for {date} already exists")
                        skipped = True
                        break

                    history = CryptoCurrencyHistoricalPrice(
                        currency_id=record.id,
                        date=date,
                        price=row[1],
                    )
                    db.session.add(history)
                    i += 1

                first_date = datetime.fromtimestamp(data["prices"][0][0] / 1000).date()
                last_date = datetime.fromtimestamp(data["prices"][-1][0] / 1000).date()
                if not skipped:
                    current_app.logger.info(
                        f"Inserted {i} prices for {record.name} ({record.symbol.upper()}) from {first_date} to {last_date}"
                    )
                    current_app.logger.info(
                        f"Inserted {record.symbol} in {round(time.time() - local_start_time, 2)}s"
                    )
        finally:
            db.session.commit()
            db.session.close()

    with ThreadPoolExecutor(max_workers=5) as executor:  # Adjust max_workers as needed
        future_to_record = {executor.submit(process_record, current_app.app_context(), record): record for record in records}

        for future in as_completed(future_to_record):
            _ = future_to_record[future]
            try:
                future.result()
            except Exception as e:
                current_app.logger.error(f"Record processing failed: {e}")

    current_app.logger.info(
        f"Inserted all of cryptos in {round(time.time() - global_start_time, 2)}s"
    )
