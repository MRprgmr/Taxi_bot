from aiogram import executor
from django.core.management.base import BaseCommand
from loader import dp
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


class Command(BaseCommand):
    help = 'Telegram-bot'

    def handle(self, *args, **options):
        pass


async def on_startup(dispatcher):
    await set_default_commands(dispatcher)

    await on_startup_notify(dispatcher)


executor.start_polling(dp, on_startup=on_startup)