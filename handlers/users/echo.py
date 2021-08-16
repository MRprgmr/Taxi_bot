from aiogram.dispatcher import FSMContext
from aiogram.types.message import ContentTypes, Message

from handlers.users.most_uses import send_main_menu
from loader import dp


@dp.message_handler(content_types=ContentTypes.ANY, state='*')
async def any_message(message: Message, state: FSMContext):
    await state.finish()
    await send_main_menu(message.from_user.id)
