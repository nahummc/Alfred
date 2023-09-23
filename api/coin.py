import json
import os

from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects


class CoinInfo:
    BASE_URL = 'https://sandbox-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    HEADERS = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': os.getenv('CMC_PRO_API_KEY', 'your_default_api_key'),
        # Read API key from environment variable
    }

    def __init__(self, symbol='BTC'):
        self.symbol = symbol

    def fetch_data(self):
        parameters = {
            'start': '1',
            'limit': '5000',
            'convert': 'USD'
        }
        session = Session()
        session.headers.update(self.HEADERS)

        try:
            response = session.get(self.BASE_URL, params=parameters)
            if response.status_code == 200:
                data = json.loads(response.text)
                for entry in data['data']:
                    if entry['symbol'] == self.symbol:
                        return entry['quote']['USD']['price']
                return f"Symbol {self.symbol} not found."
            else:
                return f"Failed to get data: {response.status_code}"
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            return f"An error occurred: {str(e)}"

    def get_price(self):
        return self.fetch_data()


# Example usage
coin_info = CoinInfo()  # Defaults to 'BTC'
print(coin_info.get_price())

coin_info = CoinInfo('ETH')  # Ethereum
print(coin_info.get_price())
