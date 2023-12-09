import click
from flask.cli import AppGroup
from app.services.commands.fetch_top_cryptos import fetch_top_currencies
from app.services.commands.fetch_historical_data import fetch_historical

crypto_cli = AppGroup("crypto")


@crypto_cli.command("fetch_top")
@click.option("-l", "--limit", type=click.IntRange(min=1, max=250), default=100)
def fetch_cryptocurrencies(limit):
    """
    Scrape top cryptocurrencies from coingecko.
    """
    return fetch_top_currencies(limit)


@crypto_cli.command("fetch_historical")
def fetch_historical_data():
    """
    Scrape top cryptocurrencies from coingecko.
    """
    return fetch_historical()
