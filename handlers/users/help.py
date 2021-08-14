from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp
from aiogram.utils import markdown

from loader import dp


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    await message.answer(f"Botdan foydalanish haqida:⠀⠀⠀⠀⠀⠀\n\
            {markdown.hlink('⠀', 'https://telegra.ph/Toshkent-Vodiy-bot-07-28')}")
