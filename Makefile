.PHONY: help fetchtop fetchhistorical forecastvalues

help:
	@echo "`make help`"
	@echo "`make fetchtop`"
	@echo "`make fetchhistorical`"
	@echo "`make forecastvalues`"

fetchtop:
	@echo "Fetching top cryptocurrencies"
	python -m flask crypto fetch_top

fetchhistorical:
	@echo "Fetching historical data for top 100 cryptocurrencies"
	python -m flask crypto fetch_historical

all:
	@echo "Fetching top cryptocurrencies"
	python -m flask crypto fetch_top
	@echo "Fetching historical data for top 100 cryptocurrencies"
	python -m flask crypto fetch_historical
	# @echo "Fetching forecast values for top 100 cryptocurrencies"
	# python -m flask crypto fetch_forecast