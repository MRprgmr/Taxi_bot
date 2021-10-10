from aiogram import Bot, Dispatcher, types
from aiogram.bot import api
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.bot.api import TelegramAPIServer

from data import config

api_server = TelegramAPIServer.from_base(config.SERVER)

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML, server=api_server)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)