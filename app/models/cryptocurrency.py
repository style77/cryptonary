from app.services.database import db
from sqlalchemy import UniqueConstraint, Index


class CryptoCurrencyDetails(db.Model):
    __tablename__ = "cryptocurrencies_details"
    id = db.Column(db.Integer, primary_key=True)
    market_cap = db.Column(db.BigInteger())
    market_cap_rank = db.Column(db.Integer())
    circulating_supply = db.Column(db.BigInteger())
    max_supply = db.Column(db.BigInteger())

    currency_id = db.Column(
        db.String, db.ForeignKey("cryptocurrencies.id", ondelete="CASCADE"), unique=True
    )
    currency = db.relationship(
        "CryptoCurrency", back_populates="details", cascade="all, delete"
    )

    def __init__(
        self,
        market_cap: int,
        market_cap_rank: int,
        circulating_supply: int,
        max_supply: int,
        currency_id: str,
    ):
        self.market_cap = market_cap
        self.market_cap_rank = market_cap_rank
        self.circulating_supply = circulating_supply
        self.max_supply = max_supply
        self.currency_id = currency_id


class CryptoCurrency(db.Model):
    __tablename__ = "cryptocurrencies"
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    symbol = db.Column(db.String, nullable=False)
    image_url = db.Column(db.String, nullable=True)
    is_rising = db.Column(db.Boolean, default=False)

    details = db.relationship(
        "CryptoCurrencyDetails", back_populates="currency", cascade="all, delete"
    )
    historical_data = db.relationship(
        "CryptoCurrencyHistoricalPrice",
        back_populates="currency",
        cascade="all, delete",
    )
    forecasted_data = db.relationship(
        "CryptoCurrencyForecastedPrice",
        back_populates="currency",
        cascade="all, delete",
    )

    def __init__(self, id: str, name: str, symbol: str, image: str):
        self.id = id
        self.name = name
        self.symbol = symbol
        self.image_url = image

    def __repr__(self):
        return f"<CryptoCurrency {self.name} [{self.symbol}]>"


class HistoricalData:
    id = db.Column(db.Integer, primary_key=True)
    currency_id = db.Column(
        db.String, db.ForeignKey("cryptocurrencies.id", ondelete="CASCADE")
    )
    timestamp = db.Column(db.DateTime, nullable=False)  # MAKE THAT DATE WITHOUT HOUR
    price = db.Column(db.Numeric(scale=2), nullable=False)

    def __init__(self, currency_id: str, timestamp: int, price: float):
        self.currency_id = currency_id
        self.timestamp = timestamp
        self.price = price


class CryptoCurrencyHistoricalPrice(HistoricalData, db.Model):
    __tablename__ = "cryptocurrencies_historical_prices"

    currency = db.relationship(
        "CryptoCurrency", back_populates="historical_data", cascade="all, delete"
    )

    def __init__(self, currency_id: str, timestamp: int, price: float):
        super().__init__(currency_id, timestamp, price)


class CryptoCurrencyForecastedPrice(HistoricalData, db.Model):
    __tablename__ = "cryptocurrencies_forecasted_prices"

    currency = db.relationship(
        "CryptoCurrency", back_populates="forecasted_data", cascade="all, delete"
    )

    def __init__(self, currency_id: str, timestamp: int, price: float):
        super().__init__(currency_id, timestamp, price)