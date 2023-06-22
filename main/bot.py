from datetime import datetime, timezone

from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardMarkup

from keyboard import get_sale_menu_keyboard, get_stock_menu_keyboard
from main import StockSalesReport, give_dates_ago
from config import token_tg, users

bot = Bot(token=token_tg)
dp = Dispatcher(bot)


@dp.message_handler(commands='start')
async def start(message: types.Message) -> None:
    if message.from_user.id in users:
        start_buttons = ['Остатки', "Продажи"]
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*start_buttons)
        await message.answer("Привет! Чем помочь?", reply_markup=keyboard)
    else:
        await message.answer("Извините, но у вас нет доступа к боту.")


@dp.message_handler(Text(equals='Остатки'))
async def stock_menu(message: types.Message) -> None:
    if message.from_user.id in users:
        stock_menu_keyboard_1 = get_stock_menu_keyboard()
        await message.answer("Какую выгрузку сделать?", reply_markup=stock_menu_keyboard_1)
    else:
        await message.answer("Извините, но у вас нет доступа к боту.")


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('stock_'))
async def inline_keyboard_stock_buttons(callback: types.CallbackQuery) -> None:
    sr = StockSalesReport()
    stock_dict = sr.get_goods_dict()
    cat_callbackdata = callback.data.split('_', 1)[1]

    if cat_callbackdata in [i for i in stock_dict.keys()] and cat_callbackdata != "Все остатки":
        cat_str = f"{cat_callbackdata} | {sum(good['stock'] for good in stock_dict[cat_callbackdata])} \n"
        for good in stock_dict[cat_callbackdata]:
            cat_str += f"  {good['name']} {good['price']} THB - {good['stock']}\n"
        await callback.message.answer(cat_str)

    elif callback.data == "stock_all_stock_button":
        for cat, values in stock_dict.items():
            cat_str = f"{cat} | {sum(good['stock'] for good in values)}\n"
            for good in values:
                cat_str += f"  {good['name']} {good['price']} THB - {good['stock']}\n"
            await callback.message.answer(cat_str)


@dp.message_handler(Text(equals='Продажи'))
async def sale_menu(message:types.Message) -> None:
    if message.from_user.id in users:
        sale_menu_keyboard = get_sale_menu_keyboard()
        await message.answer('Продажи за какой период выгрузить?', reply_markup=sale_menu_keyboard)
    else:
        await message.answer("Извините, но у вас нет доступа к боту.")


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('sales_'))
async def inline_keyboard_sales_buttons(callback:types.CallbackQuery) -> None:
    date_format = "%Y-%m-%d"

    if callback.data == 'sales_today':
        moment_from, moment_to = give_dates_ago(0)

        report = StockSalesReport(moment_from=moment_from, moment_to=moment_to)
        result = report.get_sales_turnover_outcome_report()

    elif callback.data == "sales_yesterday":
        moment_from, moment_to = give_dates_ago(1)

        report = StockSalesReport(moment_from=moment_from, moment_to=moment_to)
        result = report.get_sales_turnover_outcome_report()

    elif callback.data == 'sales_before_yesterday':
        moment_from, moment_to = give_dates_ago(2)

        report = StockSalesReport(moment_from=moment_from, moment_to=moment_to)
        result = report.get_sales_turnover_outcome_report()

    elif callback.data == 'sales_this_week':
        start_of_week_days_ago = datetime.now(timezone.utc).astimezone().weekday()
        moment_from, moment_to = give_dates_ago(start_of_week_days_ago, curent_period=True)

        report = StockSalesReport(moment_from=moment_from, moment_to=moment_to)
        result = report.get_sales_turnover_outcome_report()

    elif callback.data == 'sales_this_month':
        start_of_months_days_ago = int(datetime.now(timezone.utc).astimezone().strftime('%d')) - 1
        moment_from, moment_to = give_dates_ago(start_of_months_days_ago, curent_period=True)

        report = StockSalesReport(moment_from=moment_from, moment_to=moment_to)
        result = report.get_sales_turnover_outcome_report()

    elif callback.data == 'sales_month_before':
        time_now = datetime.now(timezone.utc).astimezone()
        moment_from, moment_to = give_dates_ago(months_ago=1)

        report = StockSalesReport(moment_from=moment_from, moment_to=moment_to)
        result = report.get_sales_turnover_outcome_report()

    await callback.message.answer(result)


if __name__ == '__main__':
    executor.start_polling(dispatcher=dp)
