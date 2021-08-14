from aiogram.types.message import Message
from filters.is_registered import IsRegistered
from re import I
from loader import dp
from aiogram.utils import markdown

@dp.message_handler(IsRegistered(), text="👨‍💻 Bot Haqida")
async def about_message(message: Message):
    await message.answer(f"Botdan foydalanish haqida:⠀⠀⠀⠀⠀⠀\n\
            {markdown.hlink('⠀', 'https://telegra.ph/Toshkent-Vodiy-bot-07-28')}")
