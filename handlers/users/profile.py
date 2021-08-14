from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from asgiref.sync import sync_to_async

from Bot.models import User, Car
from filters.is_registered import IsRegistered
from keyboards.inline.defaults import EditProfile
from keyboards.inline.type_users import TypesMarkup
from loader import dp
from aiogram.dispatcher.filters import Command

from states.register_state import RegisterUser


@dp.message_handler(Command('profile'), IsRegistered(), state='*')
async def show_profile(message: Message, state: FSMContext):
    await state.finish()
    user = await sync_to_async(User.objects.select_related('Car').get)(Telegram_id=message.from_user.id)
    if user.Is_Driver:
        response = "\n".join([
            f"    <b>👤 Profil ma'lumotlari</b>   \n",
            f"<b>Foydalanuvchi turi:</b>    🚖 Xaydovchi",
            f"<b>Ismi:</b>   {user.Name}",
            f"<b>Telefoni:</b>   {user.Phone_number}",
            f"<b>Yoshi:</b>   {user.Age}",
            f"<b>Avtomobil modeli:</b>   {user.Car.Name}\n"
        ])
    else:
        response = "\n".join([
            f"    <b>👤 Profil ma'lumotlari</b>   \n",
            f"<b>Foydalanuvchi turi:</b>    🤵 Yo'lovchi",
            f"<b>Ismi:</b>   {user.Name}",
            f"<b>Telefoni:</b>   {user.Phone_number}"
        ])
    await message.answer(response, reply_markup=EditProfile)


@dp.callback_query_handler(IsRegistered(), text="edit_profile")
async def edit_profile(call: CallbackQuery):
    await call.message.edit_text(text="🤖: Botdan kim sifatida foydalanmoqchisiz?", reply_markup=TypesMarkup)
    await RegisterUser.select_type.set()
