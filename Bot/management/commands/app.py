from aiogram import executor
from django.core.management.base import BaseCommand

import handlers
import filters
import middlewares
from loader import dp
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


class Command(BaseCommand):
    help = 'Telegram-bot'

    def handle(self, *args, **options):
        pass


async def on_startup(dispatcher):
    filters.setup(dp)
    middlewares.setup(dp)
    await set_default_commands(dispatcher)

    await on_startup_notify(dispatcher)


executor.start_polling(dp, on_startup=on_startup, skip_updates=True, fast=True)
