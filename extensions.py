import requests
import json

from config import keys


class Converter:
    @staticmethod
    # Проверки ввода пользователя
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

        if amount <= 0:
            raise APIException(f'Введите количество больше нуля')
        # Если проблем нет, то делаем запрос к API сайта для получения курса валют
        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = (json.loads(r.content)[keys[base]]) * float(amount)
        return total_base


# Класс для вывода сообщений об ошибках ввода
class APIException(Exception):
    pass
