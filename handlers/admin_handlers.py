from aiogram import types
from aiogram.dispatcher import Dispatcher, FSMContext
from database import actualizar_puntos

def register_admin_handlers(dp: Dispatcher, admin_id: int):
    @dp.message_handler(commands=['admin'])
    async def panel_admin(message: types.Message):
        if message.from_user.id != admin_id:
            return
        teclado = InlineKeyboardMarkup()
        teclado.add(InlineKeyboardButton("➕ Sumar Puntos", callback_data="sumar_puntos"))
        await message.reply("🔧 **Panel Admin**", reply_markup=teclado)

    @dp.callback_query_handler(lambda c: c.data == "sumar_puntos")
    async def pedir_datos_puntos(callback: types.CallbackQuery):
        await callback.message.edit_text("Envía: `ID_Usuario Puntos`", parse_mode="Markdown")
        await dp.current_state().set_state("esperando_puntos")

    @dp.message_handler(state="esperando_puntos")
    async def procesar_puntos(message: types.Message, state: FSMContext):
        try:
            user_id, puntos = map(int, message.text.split())
            actualizar_puntos(user_id, puntos)
            await message.reply(f"✅ +{puntos} puntos asignados!")
        except:
            await message.reply("❌ Formato incorrecto.")
        await state.finish()
