from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database import actualizar_puntos

def register_callback_handlers(dp: Dispatcher):
    @dp.message_handler(commands=['encuesta'])
    async def crear_encuesta(message: types.Message):
        teclado = InlineKeyboardMarkup()
        teclado.add(InlineKeyboardButton("🔥 +10 Puntos", callback_data="reaccion:10"))
        await message.reply("¿Te gustó el contenido?", reply_markup=teclado)

    @dp.callback_query_handler(lambda c: c.data.startswith('reaccion:'))
    async def manejar_reaccion(callback: types.CallbackQuery):
        puntos = int(callback.data.split(':')[1])
        actualizar_puntos(callback.from_user.id, puntos)
        await callback.answer(f"🎉 +{puntos} puntos!", show_alert=True)
