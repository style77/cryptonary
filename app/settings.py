import ast
import os
from typing import List


class Settings(object):
    HOST: str = "0.0.0.0"
    PORT: int = 5000
    DEBUG: bool = True
    PROXIES: List[str] = []
    COINGECKO_API_KEYS: str = ast.literal_eval(os.environ["COINGECKO_API_KEYS"])

    SQLALCHEMY_DATABASE_URI: str = (
        "postgresql://postgres:postgres@cryptonary-db:5432/cryptonary"
    )
    SQLALCHEMY_MAX_OVERFLOW: int = 120
    SQLALCHEMY_POOL_SIZE: int = 30
