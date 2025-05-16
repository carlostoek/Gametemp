import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("👤 Mi Perfil", callback_data="profile"))
    await message.reply("¡Bienvenido! Usa los botones para navegar:", reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data == "profile")
async def show_profile(callback: types.CallbackQuery):
    await callback.answer("Perfil mostrado", show_alert=True)

if __name__ == "__main__":
    logger.info("Bot starting...")
    executor.start_polling(dp, skip_updates=True)
