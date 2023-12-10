# Cryptonary

## Description

...

## Installation

Cryptonary uses Docker to run the application. To install Docker, follow the instructions on the [Docker website](https://docs.docker.com/install/).
You also need to install [Docker Compose](https://docs.docker.com/compose/install/).

## Usage

Before running application you need to setup `.env` file. Copy `.env.example` file to `.env` and fill the `COINGECKO_API_KEYS` with your key(s), variable should look like a list.

To start the application, run the following command:

```bash
docker-compose up --build
```

This will run the application on port 5000. You can access it by going to [http://localhost:5000](http://localhost:5000).

However to make application usable you need to fetch data. To do so, run the following command:

```bash
docker-compose exec cryptonary-app python -m flask crypto fetch_top  # Fetch top 100 cryptocurrencies
docker-compose exec cryptonary-app python -m flask crypto fetch_historical # Fetch historical data for saved cryptocurrencies
docker-compose exec cryptonary-app python -m flask crypto forecast # Forecast data for saved cryptocurrencies
```
You can `ctrl+c` everytime while running any command above to run application a little faster. You can also add `--limit 10` flag to `fetch_top` command to fetch only 10 cryptocurrencies.

If you can wait for a while, you can just run `docker-compose exec cryptonary-app make all` to run all commands above. (It will take a while)

Then you can see forecasted data on [http://localhost:5000/chart/crypto_symbol](http://localhost:5000/chart/btc).

## Tests

No tests for now.