from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from main import StockReport


def get_stock_menu_keyboard():
    sr = StockReport()
    stock_dict = sr.get_goods_dict()
    stock_menu_keyboard = InlineKeyboardMarkup()
    stock_menu_keyboard.insert(InlineKeyboardButton(text="Все остатки", callback_data="all_stock_button"))
    for num, cat in enumerate(stock_dict.keys()):
        stock_menu_keyboard.insert(InlineKeyboardButton(text=cat, callback_data=cat))

    return stock_menu_keyboard

# stock_menu_keyboard = InlineKeyboardMarkup()
# stock_menu_keyboard.insert(InlineKeyboardButton(text=f"Все остатки", callback_data=f"all_stock_button"))
# stock_menu_keyboard.insert(InlineKeyboardButton(text="Телогрейки", callback_data="Телогрейки"))
# stock_menu_keyboard.insert(InlineKeyboardButton(text="Шубы", callback_data="Шубы"))
# stock_menu_keyboard.insert(InlineKeyboardButton(text="Жилетки", callback_data="Жилетки"))
