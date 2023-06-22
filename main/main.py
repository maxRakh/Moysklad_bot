from calendar import monthrange
from urllib.parse import urlencode
from datetime import timedelta, datetime, timezone

import requests

from config import token_ms


class StockSalesReport:
    def __init__(self, filter_url="stockMode=nonEmpty", moment_from=None, moment_to=None):
        self.headers = {
            "Authorization": f"Bearer {token_ms}",
            "Content-Type": "application/json",
            "charset": "UTF-8"
        }
        self.stock_url_without_filter = 'https://online.moysklad.ru/api/remap/1.2/report/stock/all'  # расширенный отчет об остатках
        self.filter = filter_url

        self.sales_url_without_dates = 'https://online.moysklad.ru/api/remap/1.2/report/sales/plotseries'  # показатели продаж
        self.turnover_url_without_dates = 'https://online.moysklad.ru/api/remap/1.2/report/turnover/all'  # обороты
        self.moment_from = moment_from  # формат 2023-04-24 00:00:00
        self.moment_to = moment_to

    def get_goods_dict(self) -> dict:
        filter_url = urlencode({"filter": f"{self.filter}"})
        stock_url = f"{self.stock_url_without_filter}?{filter_url}"
        try:
            stock_response = requests.get(url=stock_url, headers=self.headers)
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

        except Exception as ex:
            print(f'Проблема с подключением к API МойСклад: {ex}')

    def get_sales(self) -> str:
        date_url_filter = f'momentFrom={self.moment_from}&momentTo={self.moment_to}&interval=day'
        sales_url = f"{self.sales_url_without_dates}?{date_url_filter}"
        try:
            sales_response = requests.get(url=sales_url, headers=self.headers)
            sales = sales_response.json()
            sales_sum = sum(i.get('sum') for i in sales.get('series')) / 100
            sales_quantity = sum(i.get('quantity') for i in sales.get('series'))

            if sales_sum != 0 and sales_quantity != 0:
                return f"За период c {self.moment_from} по {self.moment_to}\nчеков: {sales_quantity} шт., " \
                       f"на сумму {sales_sum} руб."
            else:
                return f"За период c {self.moment_from} по {self.moment_to} продаж не было"

        except Exception as ex:
            print(f'Проблема с подключением к API МойСклад: {ex}')

    def get_turnover_outcome(self) -> dict:
        turnover_filter = f'momentFrom={self.moment_from}&momentTo={self.moment_to}'
        turnover_url = f"{self.turnover_url_without_dates}?{turnover_filter}"
        try:
            response = requests.get(url=turnover_url, headers=self.headers)
            turnover = response.json()['rows']
            result = dict()
            for good in turnover:
                try:
                    if int(good['outcome']['quantity']) > 0:
                        category = good['assortment']['productFolder']['name'].split('/')[1]
                        if category not in result:
                            result[category] = [{"name": good['assortment']['name'], "outcome": int(good['outcome']['quantity'])}]
                        else:
                            result[category].append({"name": good['assortment']['name'], "outcome": int(good['outcome']['quantity'])})

                except Exception as ex:
                    print(f"Для {good['assortment']['name']} выгрузить не получилось! {ex}")

            return result
        except Exception as ex:
            print(f'Проблема с подключением к API МойСклад: {ex}')

    def get_sales_turnover_outcome_report(self) -> str:
        sales = self.get_sales()
        turnover_outcome = self.get_turnover_outcome()
        result = f"{sales}\n"

        for key, value in turnover_outcome.items():
            result += f"\n{key}:\n"
            for good in value:
                result += f"{good['name']} - {good['outcome']} \n"
        return result


def give_dates_ago(day_ago=None, curent_period=False, months_ago=0) -> tuple[str, str]:
    date_format = "%Y-%m-%d"
    delta = timedelta(hours=3)
    time_now = datetime.now(timezone.utc) + delta

    if day_ago >= 0:
        time_day = (time_now - timedelta(days=day_ago)).strftime(date_format)
        moment_from = f"{time_day} 00:00:00"

    if day_ago == 0 or curent_period:
        moment_to = time_now.strftime("%Y-%m-%d %H:%M:%S")
    elif months_ago:
        cur_y = int(time_now.strftime('%Y'))
        cur_m = int(time_now.strftime('%m'))
        if cur_m - months_ago <= 0:
            month_before = time_now.replace(year=cur_y - 1, month=12)
            days_in_month = monthrange(cur_y - 1, cur_m - months_ago)[1]
            moment_from = f"{month_before.strftime(date_format)} 00:00:00"
            moment_to = f"{month_before.replace(day=days_in_month).strftime(date_format)} 23:59:59"
        else:
            month_before = time_now.replace(month=cur_m - 1)
            days_in_month = monthrange(cur_y, cur_m)[1]
            moment_from = f"{month_before.strftime(date_format)} 00:00:00"
            moment_to = f"{month_before.replace(day=days_in_month).strftime(date_format)} 23:59:59"

    elif day_ago > 0:
        moment_to = f"{time_day} 23:59:59"

    return moment_from, moment_to


if __name__ == '__main__':
    report = StockSalesReport(moment_from='2023-04-25 00:00:01', moment_to='2023-04-25 20:25:45')
    print(report.get_sales_turnover_outcome_report())
