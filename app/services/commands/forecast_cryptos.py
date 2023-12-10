from typing import List
import pandas as pd
from prophet import Prophet
from app.services.database import db
from app.models.cryptocurrency import (
    CryptoCurrency,
    CryptoCurrencyHistoricalPrice,
    CryptoCurrencyForecastedPrice,
)


def read_historical_data(record: CryptoCurrency):
    currency_id = record.id

    historical_data = CryptoCurrencyHistoricalPrice.query.filter_by(
        currency_id=currency_id
    ).all()

    data = [{"ds": entry.date, "y": entry.price} for entry in historical_data]

    df = pd.DataFrame(data)
    return df


def forecast_data(df: pd.DataFrame, periods: int = 30):
    m = Prophet()
    m.fit(df)
    future = m.make_future_dataframe(periods=periods)
    return future


def forecast_cryptos(periods: int = 30):
    records: List[CryptoCurrency] = CryptoCurrency.query.all()
    for record in records:
        df = read_historical_data(record)
        future = forecast_data(df, periods)

        # Get the currency id for the forecasted data
        currency_id = record.id

        # Convert future DataFrame to a list of dictionaries
        forecasted_data = [
            {"date": date, "price": price}
            for date, price in zip(future["ds"], future["yhat"])
        ]

        # Check if the forecast indicates a rise in price
        predicted_rise = all(
            future["yhat"].diff().tail(3) > 0
        )  # Check the last 3 data points for rising trend

        # Update the is_rising field in CryptoCurrency based on the prediction
        if predicted_rise:
            record.is_rising = True
        else:
            record.is_rising = False

        # Iterate through the forecasted data and update/create rows in CryptoCurrencyForecastedPrice
        for entry in forecasted_data:
            # Check if the entry already exists in CryptoCurrencyForecastedPrice
            existing_entry = CryptoCurrencyForecastedPrice.query.filter_by(
                currency_id=currency_id, date=entry["date"]
            ).first()

            if existing_entry:
                # If entry exists, update its price
                existing_entry.price = entry["price"]
            else:
                # If entry does not exist, create a new row
                new_entry = CryptoCurrencyForecastedPrice(
                    currency_id=currency_id, date=entry["date"], price=entry["price"]
                )
                db.session.add(new_entry)

        # Commit changes to the database
        db.session.commit()
