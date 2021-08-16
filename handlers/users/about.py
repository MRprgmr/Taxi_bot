from aiogram.types.message import Message
from aiogram.utils import markdown

from filters.is_registered import IsRegistered
from loader import dp


@dp.message_handler(IsRegistered(), text="👨‍💻 Bot Haqida")
async def about_message(message: Message):
    await message.answer(f"Botdan foydalanish haqida:⠀⠀⠀⠀⠀⠀\n\
            {markdown.hlink('⠀', 'https://telegra.ph/Toshkent-Vodiy-bot-07-28')}")
