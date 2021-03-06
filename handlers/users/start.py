from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.utils.markdown import hbold
from asgiref.sync import sync_to_async

from Bot.models import User
from handlers.users.most_uses import send_main_menu
from keyboards.inline.register_button import RegisterButton
from loader import dp
from states.register_state import RegisterUser


@dp.message_handler(CommandStart(), state='*')
async def bot_start(message: types.Message):
    await dp.current_state().finish()
    user, created = await sync_to_async(User.objects.update_or_create)(Telegram_id=message.from_user.id,
                                                                       defaults={
                                                                           'Username': message.from_user.username})
    is_registered = user.Is_registered
    if user.Name == '':
        user.Name = message.from_user.first_name
    await sync_to_async(user.save)()

    if not is_registered:
        answer_text = "\n".join([
            f"đ¤:  Assalomu alaykum, {hbold(message.from_user.full_name)}\n",
            f"Bu yerda siz {hbold('đ Vodiy va Toshkent')}",
            f"bo'ylab {hbold('đ Taxi')} xizmatidan foydalana olasiz.",
            f"đ Yordam uchun /help ni bosing.\n",
            f"âšī¸ Botdan foydalanish uchun ro'yxatdan o'tish kerak",
        ])
        await message.answer(text=answer_text, reply_markup=RegisterButton)

        await RegisterUser.start_registration.set()
    else:
        await send_main_menu(message.from_user.id)
