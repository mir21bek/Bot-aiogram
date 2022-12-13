"""
This is a echo bot.
It echoes any incoming text messages.
"""

import logging
import requests
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

API_TOKEN = '5960515236:AAFjwZtNAvCPA7ayod_ApWXKm14hUnX33Vo'
#
# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


page = 0


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    print(message.text)
    url1 = 'https://rickandmortyapi.com/api/character/'
    global page
    if message.text == 'next':
        rer = requests.get(url=url1).json()
        page += 1
        url1 += f'?page={page}'
    elif message.text == 'prev':
        rer = requests.get(url=url1).json()
        page -= 1
        url1 += f'?page={page}'
    data = requests.get(url1).json()
    characters = data['results']
    greet_kb = InlineKeyboardMarkup(row_width=2)
    for i in characters:
        button_hi = InlineKeyboardButton(f'{i["name"]}', callback_data=f'{i["url"]}')
        greet_kb.add(button_hi)
    button_next = InlineKeyboardButton(f'Вперед', callback_data='next')
    button_prev = InlineKeyboardButton(f'Назад', callback_data='prev')
    greet_kb.add(button_next, button_prev)

    await message.reply("Привет\nЯ вики по рик морти\nНажми на кнопку", reply_markup=greet_kb)


@dp.callback_query_handler()
async def call_data(call: types.CallbackQuery):
    if call.data == 'next':
        call.message.text = 'next'
        await send_welcome(message=call.message)
    elif call.data == 'prev':
        call.message.text = 'prev'
        await send_welcome(message=call.message)
    else:
        print(call.data)
        user = requests.get(call.data).json()
        print(call.from_user.first_name)
        await bot.send_photo(chat_id=call.from_user.id, photo=user["image"], caption=f'Имя - {user["name"]}\nСтатус - {user["status"]}\nПол - {user["gender"]}\nРаса - {user["species"]}')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
