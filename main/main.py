from urllib.parse import urlencode

import requests

from config import token_ms


class StockReport:
    def __init__(self, filter_url="stockMode=nonEmpty", category_url=None):
        self.stock_url = 'https://online.moysklad.ru/api/remap/1.2/report/stock/all'  # расширенный отчет об остатках
        self.headers_stock = {
            "Authorization": f"Bearer {token_ms}",
            "Content-Type": "application/json",
            "charset": "UTF-8"
        }
        self.filter = filter_url
        self.category_url = category_url

    def get_goods_dict(self) -> dict:
        filter_url = urlencode({"filter": f"{self.filter}"})  # через точку с запятой добавляются фильтры
        stock_url_filter = f"{self.stock_url}?{filter_url}"
        try:
            stock_response = requests.get(url=stock_url_filter, headers=self.headers_stock)
        except Exception as ex:
            print(f'Проблема с подключением к API МойСклад: {ex}')

        goods = stock_response.json()['rows']
        result = dict()

        for good in goods:
            try:
                category = good['folder'].get('name')
                if category not in result:
                    result[category] = [{"name": good['name'], "stock": int(good['stock']),
                                         "price": int(good['salePrice'] / 100)}]
                else:
                    result[category].append({"name": good['name'], "stock": int(good['stock']),
                                             "price": int(good['salePrice'] / 100)})
            except Exception as ex:
                print(f"Для {good['name']} выгрузить не получилось! {ex}")

        return result
