import requests
import json

class CoinInfo:
    def __init__(self, symbol: str):
        self.symbol = symbol
        self.base_url = "https://api.gemini.com"

    def get_price(self):
        url = f"{self.base_url}/v1/symbols/details/{self.symbol}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data.get('price')
        else:
            return "Failed to retrieve price."

    def get_high_low_diff(self):
        url = f"{self.base_url}/v2/ticker/{self.symbol}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            high = float(data.get('high', 0))
            low = float(data.get('low', 0))
            last = float(data.get('last', 0))

            diff_to_high = high - last
            diff_to_low = last - low

            biggest_diff = "high" if diff_to_high > diff_to_low else "low"
            diff_value = diff_to_high if biggest_diff == "high" else diff_to_low

            return biggest_diff, diff_value
        else:
            return "Failed to retrieve high/low."
