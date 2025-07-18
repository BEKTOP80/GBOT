import asyncio
import nest_asyncio
import logging
import aiosqlite
import json

nest_asyncio.apply()

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram import F



#-------------------------------------------------------------------------------------------------------------------------------------------------------------

logging.basicConfig(level=logging.INFO)

API_TOKEN = '7565743468:AAGaIxF-FewIPTBMCSjukdYw2epjh7U3zlY'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

DB_NAME = 'quiz_bot.db'
DICT_DATA = 'data/quiz_data.json'
  
with open(DICT_DATA, 'r') as j:
    quiz_data = json.loads(j.read())

def generate_options_keyboard(answer_options, right_answer):
    builder = InlineKeyboardBuilder()

    for option in answer_options:
        builder.add(types.InlineKeyboardButton(
            text=option,
            callback_data="right_answer" if option == right_answer else "wrong_answer"))

    builder.adjust(1)
    return builder.as_markup()

async def create_table():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''CREATE TABLE IF NOT EXISTS quiz_state (user_id INTEGER PRIMARY KEY, question_index INTEGER)''')
        await db.execute('''CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, score INTEGER)''')
        await db.commit()

async def main():
    await create_table()
    await dp.start_polling(bot)

if __name__ == "__main__": 
    asyncio.run(main())