from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database import registrar_usuario, obtener_usuario, top_10_usuarios

def register_user_handlers(dp: Dispatcher):
    @dp.message_handler(commands=['start'])
    async def cmd_start(message: types.Message):
        user_id = message.from_user.id
        username = message.from_user.username
        registrar_usuario(user_id, username)
        
        teclado = InlineKeyboardMarkup(row_width=2)
        teclado.add(
            InlineKeyboardButton("👤 Mi Perfil", callback_data="menu_perfil"),
            InlineKeyboardButton("🏆 Ranking", callback_data="menu_ranking")
        )
        await message.reply("🌟 **Bienvenido al Sistema VIP**", reply_markup=teclado)

    @dp.callback_query_handler(lambda c: c.data == "menu_perfil")
    async def mostrar_perfil(callback: types.CallbackQuery):
        usuario = obtener_usuario(callback.from_user.id)
        respuesta = f"👤 **Perfil**\nPuntos: {usuario[3]}\nNivel: {usuario[4]}"
        teclado = InlineKeyboardMarkup().add(InlineKeyboardButton("🔙 Volver", callback_data="menu_principal"))
        await callback.message.edit_text(respuesta, reply_markup=teclado)

    @dp.callback_query_handler(lambda c: c.data == "menu_ranking")
    async def mostrar_ranking(callback: types.CallbackQuery):
        top_usuarios = top_10_usuarios()
        respuesta = "🏆 **Ranking**\n" + "\n".join([f"{i+1}. {u[0]}: {u[1]} pts" for i, u in enumerate(top_usuarios)])
        teclado = InlineKeyboardMarkup().add(InlineKeyboardButton("🔙 Volver", callback_data="menu_principal"))
        await callback.message.edit_text(respuesta, reply_markup=teclado)
