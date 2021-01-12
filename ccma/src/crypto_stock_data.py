import os
import csv
from datetime import datetime

class LinkedListElement():

    def __init__(self, data):
        self._data = data
        self._previous = None
        self._next = None

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        self._data = data

    @property
    def previous(self):
        return self._previous

    @previous.setter
    def previous(self, p):
        self._previous = p
    
    @property
    def next(self):
        return self._next

    @next.setter
    def next(self, n):
        self._next = n 

    # This takes any node in the linked list sequence and builds the full list out of it
    def node_to_list(self):
        
        # Add self to list
        node = self
        full_list = [node]

        # Add all "next" nodes to list
        while node.next is not None:
            node = node.next
            full_list.append(node)

        # Reset to node
        node = self

        # Add all "previous" nodes
        while node.previous is not None:
            node = node.previous
            full_list.insert(0, node)

        return full_list
        

class CryptoStockDateDataLinkedListElement(LinkedListElement):

    def __init__(self, data):
        super().__init__(data)


    

class CryptoStockDateData():

    def __init__(self, epoch, opn, high, low, close, vwap, volume, trade_count, date, volume_from):
        self.epoch = int(epoch)
        self.open = float(opn)
        self.high = float(high)
        self.low = float(low)
        self.close = float(close)
        self.vwap = float(vwap)
        self.volume = float(volume)
        self.trade_count = int(trade_count)
        self.date = datetime.strptime(date, "%Y-%m-%d").date()
        self.volume_from = float(volume_from)

    def __repr__(self):
        return f"CryptoStockDateData dated {self.date}"

class CryptoStockData():

    def __init__(self, crypto_currency_code, file_path=None):
        self.crypto_currency_code = crypto_currency_code
        self.file_path = file_path
        self.date_data = None

    def store_file_path(self, file_path):
        self.file_path = file_path

    def load_currency_data(self, file_path=None):
        if file_path is not None:
            self.store_file_path(file_path)

        if self.file_path is None:
            raise ValueError(f"No path to .csv file specified for {self.crypto_currency_code}")

        with open(self.file_path, "r") as csvfile:
            csvreader = csv.reader(csvfile)

            # This skips the first row of the CSV file.
            next(csvreader)

            self.date_data = [CryptoStockDateData(*row) for row in csvreader]

    def generate_linked_list(self):

        prev = None
        curr = None
        first = None

        for i, csdd in enumerate(self.date_data):
            prev = curr
            curr = CryptoStockDateDataLinkedListElement(csdd)
            if first is None:
                first =  curr
            if prev is not None:
                prev.next = curr
            if curr is not None:
                curr.previous = prev

        return first



class CryptoValueCurrency():

    def __init__(self, fiat_currency_code):
        self.fiat_currency_code = fiat_currency_code
        self.crypto_currencies = {}

    def load_stock_data(self):
        fiat_currency_path = os.path.join('data', str(self.fiat_currency_code))
        for file_path in os.listdir(fiat_currency_path):
            crypto_currency_code = file_path.split('_')[1]
            csd = CryptoStockData(crypto_currency_code, os.path.join(fiat_currency_path, file_path))
            csd.load_currency_data()
            self.crypto_currencies[crypto_currency_code] = csd

    def generate_linked_lists(self):
        if self.crypto_currencies == {}:
            raise ValueError("No stock data has been loaded, call load_stock_data")

        crypto_linked_list_dicts = {}

        for crypto_code, csd in self.crypto_currencies.items():
            crypto_linked_list_dicts[crypto_code] = csd.generate_linked_list()
        
        print(crypto_linked_list_dicts)

        print(crypto_linked_list_dicts['XRP'].node_to_list())



if __name__ == "__main__":
    cvc_usd = CryptoValueCurrency("USD")
    cvc_usd.load_stock_data()
    cvc_usd.generate_linked_lists()
