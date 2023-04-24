from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

from config import token_tg
from keyboard import get_stock_menu_keyboard

from main import StockReport

bot = Bot(token=token_tg)
dp = Dispatcher(bot)


@dp.message_handler(commands='start')
async def start(message: types.Message) -> None:
    start_buttons = ['Остатки', "Продажи"]
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    await message.answer("Привет! Чем помочь?", reply_markup=keyboard)


@dp.message_handler(Text(equals='Остатки'))
async def stock_menu(message: types.Message) -> None:
    # stock_menu_keyboard_1 = stock_menu_keyboard
    # await message.answer("Какую выгрузку сделать?", reply_markup=stock_menu_keyboard_1)

    stock_menu_keyboard_1 = get_stock_menu_keyboard()
    await message.answer("Какую выгрузку сделать?", reply_markup=stock_menu_keyboard_1)


@dp.callback_query_handler()
async def inline_keyboard_stock_buttons(callback: types.CallbackQuery):
    sr = StockReport()
    stock_dict = sr.get_goods_dict()

    if callback.data in [i for i in stock_dict.keys()] and callback.data != "Все остатки":
        cat_str = f"{callback.data}: всего {sum(good['stock'] for good in stock_dict[callback.data])} шт.\n"
        for good in stock_dict[callback.data]:
            cat_str += f"  {good['name']}: остаток {good['stock']} шт., цена {good['price']} руб.\n"
        await callback.message.answer(cat_str)

    if callback.data == "all_stock_button":
        for cat, values in stock_dict.items():
            cat_str = f"{cat}: всего {sum(good['stock'] for good in values)} шт.\n"
            for good in values:
                cat_str += f"  {good['name']}: остаток {good['stock']} шт., цена {good['price']} руб.\n"
            await callback.message.answer(cat_str)


@dp.message_handler(Text(equals='Все остатки'))
async def get_all_stock(message: types.Message) -> None:
    await message.answer("Please waiting...")

    sr = StockReport()
    data = sr.get_goods_dict()

    for cat, values in data.items():
        cat_str = f"{cat}: всего {sum(good['stock'] for good in values)} шт.\n"
        for good in values:
            cat_str += f"  {good['name']}: остаток {good['stock']} шт., цена {good['price']} руб.\n"

        await message.answer(cat_str)


if __name__ == '__main__':
    executor.start_polling(dispatcher=dp)
