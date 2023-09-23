import configparser
import json
import pytz
from datetime import datetime
from requests import Request, Session
from dateutil import parser


class Coin:
    def __init__(self, coin_symbol):
        self.coin_symbol = coin_symbol
        self.fiat_symbol = "CAD"
        self.api_key = '6038d704-f04f-4ec6-86f7-f36ca68c5166'  # Hardcoded for now

    def get_info(self):
        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
        parameters = {'slug': self.coin_symbol, 'convert': self.fiat_symbol}
        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': self.api_key
        }

        session = Session()
        session.headers.update(headers)
        response = session.get(url, params=parameters)
        info = json.loads(response.text)

        data = list(info['data'].values())[0]  # Assuming the first value is the desired data
        return data

    def get_price(self):
        data = self.get_info()
        price = data['quote'][self.fiat_symbol]['price']
        return f"The current price of {self.coin_symbol} in {self.fiat_symbol} is {price:,.2f}"

    def get_change(self):
        data = self.get_info()
        percent_change_24h = data['quote'][self.fiat_symbol]['percent_change_24h']
        direction = "up" if percent_change_24h >= 0 else "down"
        return f"{self.coin_symbol} has gone {direction} {abs(percent_change_24h):.2f}% in the last 24 hours"


if __name__ == "__main__":
    bitcoin = Coin('bitcoin')
    print(bitcoin.get_price())
    print(bitcoin.get_change())
