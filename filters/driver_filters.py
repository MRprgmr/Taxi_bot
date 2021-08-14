from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message
from asgiref.sync import sync_to_async

from Bot.models import User


class StartCreateAds(BoundFilter):
    async def check(self, message: Message):
        user = await sync_to_async(User.objects.get)(Telegram_id=message.from_user.id)
        if message.content_type == 'text' and message.text == "➕ Yangi e’lon" and user.Is_Driver:

            return True
        else:
            return False


class MyAds(BoundFilter):
    async def check(self, message: Message):
        user = await sync_to_async(User.objects.get)(Telegram_id=message.from_user.id)
        if message.content_type == 'text' and message.text == "📨 Mening e’lonlarim" and user.Is_Driver:

            return True
        else:
            return False
