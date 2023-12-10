import click
from flask.cli import AppGroup
from app.services.commands.fetch_top_cryptos import fetch_top_currencies
from app.services.commands.fetch_historical_data import fetch_historical_data
from app.services.commands.forecast_cryptos import forecast_cryptos

crypto_cli = AppGroup("crypto")


@crypto_cli.command("fetch_top")
@click.option("-l", "--limit", type=click.IntRange(min=1, max=250), default=100)
def fetch_cryptocurrencies(limit):
    """
    Scrape top cryptocurrencies from coingecko.
    """
    return fetch_top_currencies(limit)


@crypto_cli.command("fetch_historical")
def fetch_historical():
    """
    Scrape top cryptocurrencies from coingecko.
    """
    return fetch_historical_data()


@crypto_cli.command("forecast")
def forecast_data():
    """
    Forecast data from already fetched historical data.
    """
    return forecast_cryptos()
