#!/bin/bash

echo "Fetching top cryptocurrencies"
python -m flask crypto fetch_top

echo "Fetching historical data for top 100 cryptocurrencies"
python -m flask crypto fetch_historical

echo "Fetching forecast values for top 100 cryptocurrencies"
python -m flask crypto forecast