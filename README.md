# Cryptonary

## Description

...

## Installation

Cryptonary uses Docker to run the application. To install Docker, follow the instructions on the [Docker website](https://docs.docker.com/install/).
You also need to install [Docker Compose](https://docs.docker.com/compose/install/).

## Usage

Before running application you need to setup `.env` file. Copy `.env.example` file to `.env` and fill the `COINGECKO_API_KEYS` with your key(s), variable should look like a list.

To start the application and insert base currencies, run the following command:

```bash
docker-compose up --build
docker exec -it cryptonary-app python -m flask crypto fetch_top
```

This will run the application on port 8000. You can access it by going to [http://localhost:8000](http://localhost:8000).

Don't forget to setup cronjob on your server to run `fetch_historical` and `forecast` commands periodically.
There is already a cronjob file in the project root directory. You can add it to your crontab by running the following command:

```bash
crontab cryptonary.cron
```

## CLI Commands

```bash
docker-compose exec cryptonary-app python -m flask crypto fetch_top  # Fetch top 100 cryptocurrencies
docker-compose exec cryptonary-app python -m flask crypto fetch_historical # Fetch historical data for saved cryptocurrencies
docker-compose exec cryptonary-app python -m flask crypto forecast # Forecast data for saved cryptocurrencies
```
You can `ctrl+c` everytime while running any command above to run application a little faster. You can also add `--limit 10` flag to `fetch_top` command to fetch only 10 cryptocurrencies.

If you can wait for a while, you can just run `make all` to run all commands above. (It will take a while)

Then you can see forecasted data on [http://localhost:5000/chart/crypto_symbol](http://localhost:5000/chart/btc).

## Tests

No tests for now.