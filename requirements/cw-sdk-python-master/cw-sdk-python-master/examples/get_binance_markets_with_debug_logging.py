import cryptowatch
import logging


logging.basicConfig()
# Get the cryptowatch logger and set it to DEBUG
logging.getLogger("cryptowatch").setLevel(logging.DEBUG)


binance = cryptowatch.markets.list("binance")

for market in binance.markets:
    print(market.pair)

print("TOTAL {} markets".format(len(binance.markets)))
