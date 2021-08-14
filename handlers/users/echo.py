from handlers.users.most_uses import send_main_menu
from aiogram.types.message import ContentTypes, Message
from loader import dp

@dp.message_handler(content_types=ContentTypes.ANY, state='*')
async def any_message(message: Message):
    await send_main_menu(message.from_user.id)
