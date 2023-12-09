import os
from typing import List


class Settings(object):
    HOST: str = "0.0.0.0"
    PORT: int = 5000
    DEBUG: bool = True
    PROXIES: List[str] = []
    COINGECKO_API_KEY: str = os.environ["COINGECKO_API_KEY"]

    SQLALCHEMY_DATABASE_URI: str = (
        "postgresql://postgres:postgres@cryptonary-db:5432/cryptonary"
    )
