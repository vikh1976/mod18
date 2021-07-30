import requests
import json

from config import keys


class Converter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise APIException(f'Введены одинаковые валюты для перевода - {quote}')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Неизвестная валюта - {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Неизвестная валюта - {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество - {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = (json.loads(r.content)[keys[base]]) * amount
        return total_base


class APIException(Exception):
    pass
