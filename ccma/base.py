# First import the libraries that we need to use
import pandas as pd
import requests
import json

def fetch_OHLC_data(symbol, timeframe):
    """This function will get Open/High/Low/Close, Volume and tradecount data for the pair passed and save to CSV"""
    pair_split = symbol.split('/')  # symbol must be in format XXX/XXX ie. BTC/USD
    symbol = pair_split[0] + pair_split[1]
    url = f'https://api.kraken.com/0/public/OHLC?pair={symbol}&interval={timeframe}'
    response = requests.get(url)
    if response.status_code == 200:  # check to make sure the response from server is good
        j = json.loads(response.text)
        result = j['result']
        keys = []
        for item in result:
            keys.append(item)
        if keys[0] != 'last':
            data = pd.DataFrame(result[keys[0]],
                                columns=['unix', 'open', 'high', 'low', 'close', 'vwap', 'volume', 'tradecount'])
        else:
            data = pd.DataFrame(result[keys[1]],
                                columns=['unix', 'open', 'high', 'low', 'close', 'vwap', 'volume', 'tradecount'])

        data['date'] = pd.to_datetime(data['unix'], unit='s')
        data['volume_from'] = data['volume'].astype(float) * data['close'].astype(float)

        # if we failed to get any data, print an error...otherwise write the file
        if data is None:
            print("Did not return any data from Kraken for this symbol")
        else:
            if timeframe == '1':
                tf = 'minute'
            elif timeframe == '60':
                tf = 'hour'
            elif timeframe == '1440':
                tf = 'day'
            else:
                tf = ''
            data.to_csv(f'data/{pair_split[1]}/Kraken_{pair_split[0]}_{pair_split[1]}_{tf}.csv', index=False)
    else:
        print("Did not receieve OK response from Kraken API")

def fetch_SPREAD_data(symbol):
    """This function will return the nearest bid/ask and calculate the spread for the symbol passed and save
        the results to a CSV file"""
    pair_split = symbol.split('/')  # symbol must be in format XXX/XXX ie. BTC/USD
    symbol = pair_split[0] + pair_split[1]
    url = f'https://api.kraken.com/0/public/Spread?pair={symbol}'
    response = requests.get(url)
    if response.status_code == 200:  # check to make sure the response from server is good
        j = json.loads(response.text)
        result = j['result']
        keys = []
        for item in result:
            keys.append(item)
        if keys[0] != 'last':
            data = pd.DataFrame(result[keys[0]], columns=['unix', 'bid', 'ask'])
        else:
            data = pd.DataFrame(result[keys[1]], columns=['unix', 'bid', 'ask'])

        data['date'] = pd.to_datetime(data['unix'], unit='s')
        data['spread'] = data['ask'].astype(float) - data['bid'].astype(float)

        # if we failed to get any data, print an error...otherwise write the file
        if data is None:
            print("Did not return any data from Kraken for this symbol")
        else:
            data.to_csv(f'data/Kraken_{symbol}_spreads.csv', index=False)
    else:
        print("Did not receieve OK response from Kraken API")

def fetch_PRINTS_data(symbol):
    """This function will return historical trade prints for the symbol passed and save the results to a CSV file"""
    pair_split = symbol.split('/')  # symbol must be in format XXX/XXX ie. BTC/USD
    symbol = pair_split[0] + pair_split[1]
    url = f'https://api.kraken.com/0/public/Trades?pair={symbol}'
    response = requests.get(url)
    if response.status_code == 200:  # check to make sure the response from server is good
        j = json.loads(response.text)

        result = j['result']
        keys = []
        for item in result:
            keys.append(item)
        if keys[0] != 'last':
            data = pd.DataFrame(result[keys[0]], columns=['price', 'volume', 'time', 'buysell', 'ordtype', 'misc'])
        else:
            data = pd.DataFrame(result[keys[1]], columns=['price', 'volume', 'time', 'buysell', 'ordtype', 'misc'])

        data['date'] = pd.to_datetime(data['time'], unit='s')
        data['buysell'] = data['buysell'].apply(lambda x: "buy" if x == 'b' else "sell")
        data['ordtype'] = data['ordtype'].apply(lambda x: "limit" if x == 'l' else "market")
        data['dollaramount'] = data['price'].astype(float) * data['volume'].astype(float)
        data.drop(columns=['misc'], inplace=True)  #drop misc column that is typically blank

        # if we failed to get any data, print an error...otherwise write the file
        if data is None:
            print("Did not return any data from Kraken for this symbol")
        else:
            data.to_csv(f'data/Kraken_{symbol}_tradeprints.csv', index=False)
    else:
        print("Did not receieve OK response from Kraken API")


def fetch_matching_asset_pairs(currency='USD'):
    url = f"https://api.kraken.com/0/public/AssetPairs"
    response = requests.get(url)
    if response.status_code == 200:
        j = json.loads(response.text)
        result = j['result']
        matching_price_pairs = [data['wsname'] for data in result.values() if data.get('wsname') and data['wsname'].split('/')[1] == currency]
        return matching_price_pairs

if __name__ == "__main__":
    # we set which pair we want to retrieve data for
    pair = "ETH/USD"
    all_pairs = fetch_matching_asset_pairs('USD')
    # full timeframe intervals found here: https://www.kraken.com/en-us/features/api#get-ohlc-data
    #fetch_OHLC_data(symbol=pair, timeframe='1') # fetches minute data
    # fetch_OHLC_data(symbol=pair, timeframe='60')  # fetches hourly data
    for pair in all_pairs:
        fetch_OHLC_data(symbol=pair, timeframe='1440')  # fetches daily data
        # fetch_SPREAD_data(symbol=pair) # gets bid/ask spread data
        # fetch_PRINTS_data(symbol=pair) # gets historical trade print data