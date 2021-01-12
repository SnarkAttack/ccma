import cryptowatch


kraken = cryptowatch.markets.get("kraken:btcusd")

print("Kraken BTCUSD Price: ", "${}".format(kraken.market.price.last))
print("Kraken BTCUSD Change:", "{:.2f}%".format(kraken.market.price.change))
print("Kraken BTCUSD Volume:", "${:.2f}".format(kraken.market.volume_quote))

print("---")
# Access your API allowance after each API call like this:
print("Cost of last API request:", kraken._allowance.cost)
print("Remaining allowance:", kraken._allowance.remaining)
print("Remaining allowance paid:", kraken._allowance.remaining_paid)
