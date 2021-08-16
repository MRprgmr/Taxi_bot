from asgiref.sync import sync_to_async

from Bot.models import User
from keyboards.default.main_menu import main_menu_driver, main_menu_user
from loader import dp


async def send_main_menu(id):
    user = await sync_to_async(User.objects.get)(Telegram_id=id)
    if user.Is_registered:
        if user.Is_Driver:
            reply_markup = main_menu_driver
        else:
            reply_markup = main_menu_user
        await dp.bot.send_message(id, "Bosh menu:", reply_markup=reply_markup)
    else:
        await dp.bot.send_message(id, "Ro'yxatdan o'tish uchun /start ni bosing")
