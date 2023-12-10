import ast
import os


class Settings(object):
    HOST: str = "0.0.0.0"
    PORT: int = 5000
    DEBUG: bool = True

    RESOLUTION: int = 7

    # Days to fetch historical data for
    HISTORICAL_DAYS: int = 1095

    # Days to forecast data for
    PERIODS: int = 90
    # "backtested" periods to show in the graph
    PREV_PERIODS: int = 30

    COINGECKO_API_KEYS: str = ast.literal_eval(os.environ["COINGECKO_API_KEYS"])

    SQLALCHEMY_DATABASE_URI: str = (
        "postgresql://postgres:postgres@cryptonary-db:5432/cryptonary"
    )
    SQLALCHEMY_MAX_OVERFLOW: int = 120
    SQLALCHEMY_POOL_SIZE: int = 30
