
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import CommandStart
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Настройка Google Sheets API
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)
sheet = client.open_by_key("1KobwKat_W2KqCSveErU0tXPNavy-gwJAc0-gcTwZt38").worksheet("Курьер")

def get_cities():
    return [v.strip().lower() for v in sheet.col_values(1)[1:] if v.strip()]

# Получаем токен из переменной окружения
TOKEN = os.getenv("BOT_TOKEN")

# Настройка Telegram-бота
logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("👋 Привет! Напиши название города, и я скажу, есть ли туда курьерская доставка. Или напиши /города, чтобы посмотреть список.")

@dp.message(lambda msg: msg.text.lower() == "/города")
async def show_all(message: Message):
    cities = get_cities()
    await message.answer("📍 Города с доставкой:\n" + "\n".join(c.title() for c in cities))

@dp.message()
async def check_city(message: Message):
    user_input = message.text.strip().lower()
    cities = get_cities()
    if user_input in cities:
        await message.answer("✅ Да, доставка курьером есть в этот город!")
    else:
        await message.answer("❌ Пока туда доставки нет.")

if __name__ == "__main__":
    import asyncio
    asyncio.run(dp.start_polling(bot))
