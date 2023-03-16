import json
import requests
# импрортируем словарь currency
from conf import currency
# обьявляем класс ошибки конвертации
class ConvException(Exception):
    pass
# обьявляем класс для обмена валют
class Exchange:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise ConvException(
                f'Нельзя переводить одинаковые валюты {base}.')
# попытка найти валюту в словаре и выброс ошибки
        try:
            quote_ticker = currency[quote]
        except KeyError:
            raise ConvException(f'Не могу обработать валюту {quote}')

        try:
            base_ticker = currency[base]
        except KeyError:
            raise ConvException(f'Не могу обработать валюту {base}')

        try:
            amount = int(amount)
        except ValueError:
            raise ConvException(f'Не смог обработать количество {amount}')
 # запрос к API
        r = requests.get(
            f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
 # расчет результата
        total_base = float(json.loads(r.content)[currency[base]]) * amount
        return (total_base)