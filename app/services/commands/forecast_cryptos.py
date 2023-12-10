import time
from typing import List

import pandas as pd
from flask import current_app
from prophet import Prophet

from app.models.cryptocurrency import (
    CryptoCurrency,
    CryptoCurrencyForecastedPrice,
    CryptoCurrencyHistoricalPrice,
)
from app.services.commands.common import setup_logger
from app.services.database import db

PERIODS = 90


def read_historical_data(record: CryptoCurrency):
    currency_id = record.id

    historical_data = CryptoCurrencyHistoricalPrice.query.filter_by(
        currency_id=currency_id
    ).all()

    data = [{"ds": entry.date, "y": entry.price} for entry in historical_data]

    df = pd.DataFrame(data, columns=["ds", "y"])
    df["ds"] = pd.to_datetime(df["ds"])
    df = df.sort_values("ds")

    return df


def forecast_data(df: pd.DataFrame):
    m = Prophet()
    m.fit(df)

    future = m.make_future_dataframe(periods=PERIODS, include_history=False)

    forecast = m.predict(future)

    return forecast


def forecast_cryptos():
    setup_logger(current_app)
    records: List[CryptoCurrency] = CryptoCurrency.query.all()
    global_start_time = time.time()
    for record in records:
        current_app.logger.info(
            f"Forecasting data for {record.name} ({record.symbol.upper()})"
        )

        df = read_historical_data(record)
        try:
            future = forecast_data(df)
        except Exception as e:
            current_app.logger.error(
                f"Something went wrong while forecasting data of {record.name} \
                ({record.symbol.upper()}): {e}"
            )
            continue

        currency_id = record.id

        forecasted_data = [
            {"date": date, "price": price}
            for date, price in zip(future["ds"], future["yhat"])
        ]

        predicted_rise = all(future["yhat"].diff().tail(3) > 0)

        if predicted_rise:
            record.is_rising = True
            current_app.logger.info(
                f"Setting {record.name} ({record.symbol.upper()}) as 'rising'."
            )
        else:
            record.is_rising = False

        local_start_time = time.time()
        for entry in forecasted_data:
            existing_entry = CryptoCurrencyForecastedPrice.query.filter_by(
                currency_id=currency_id, date=entry["date"]
            ).first()

            if existing_entry:
                existing_entry.price = entry["price"]
            else:
                new_entry = CryptoCurrencyForecastedPrice(
                    currency_id=currency_id, date=entry["date"], price=entry["price"]
                )
                db.session.add(new_entry)

        db.session.commit()
        current_app.logger.info(
            f"Inserted data for {record.name} ({record.symbol.upper()}) \
            in {round(time.time() - local_start_time, 2)}s"
        )

    current_app.logger.info(
        f"Forecasted all of data in {round(time.time() - global_start_time, 2)}s"
    )
