from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from main import StockSalesReport


def get_stock_menu_keyboard():
    sr = StockSalesReport()
    stock_dict = sr.get_goods_dict()
    stock_menu_keyboard = InlineKeyboardMarkup()
    stock_menu_keyboard.insert(InlineKeyboardButton(text="Все остатки", callback_data="stock_all_stock_button"))
    for num, cat in enumerate(stock_dict.keys()):
        stock_menu_keyboard.insert(InlineKeyboardButton(text=cat, callback_data=f"stock_{cat}"))

    return stock_menu_keyboard


def get_sale_menu_keyboard():
    sale_menu_keyboard = InlineKeyboardMarkup(row_width=2)
    sale_menu_keyboard.insert(InlineKeyboardButton(text="Сегодня", callback_data="sales_today"))
    sale_menu_keyboard.insert(InlineKeyboardButton(text="Вчера", callback_data="sales_yesterday"))
    sale_menu_keyboard.insert(InlineKeyboardButton(text="Позавчера", callback_data="sales_before_yesterday"))
    sale_menu_keyboard.insert(InlineKeyboardButton(text="За эту неделю", callback_data="sales_this_week"))
    sale_menu_keyboard.insert(InlineKeyboardButton(text="За этот месяц", callback_data="sales_this_month"))
    sale_menu_keyboard.insert(InlineKeyboardButton(text="За прошлый месяц", callback_data="sales_month_before"))

    return sale_menu_keyboard
