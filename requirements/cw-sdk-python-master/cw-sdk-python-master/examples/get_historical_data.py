# Example showing how to get the last 30 candles for the 1 minute  time frame
# for the KRAKEN:BTCUSD market.

import cryptowatch as cw

candles = cw.markets.get("kraken:btcusd", ohlc=True)

# This will return a list of 1 minute candles, each candle being a list with:
# [close_timestamp, open, high, low, close, volume_base, volume_quote].
# The oldest candle will be the first one in the list, the most recent will be the last one.
print(candles.of_1m[:-30])

# The last 500 candles for each time frames are returned.
# Possible time frames are:
#  1 minute candles:   candles.of_1m
#  3 minutes candles:  candles.of_3m
#  5 minutes candles:  candles.of_5m
# 15 minutes candles:  candles.of_15m
# 30 minutes candles:  candles.of_30m
#  1 hour candles:     candles.of_1h
#  2 hours candles     candles.of_2h
#  4 hours candles:    candles.of_4h
#  6 hours candles:    candles.of_6h
# 12 hours candles:    candles.of_12h
#  1 day candles:      candles.of_1d
#  3 days candles:     candles.of_3d
#  1 week candles starting on Thursday: candles.of_1w
#  1 week candles starting on Monday:   candles.of_1w_monday
