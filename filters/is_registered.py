from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from asgiref.sync import sync_to_async

from Bot.models import User


class IsRegistered(BoundFilter):
    async def check(self, message: types.Message):
        user = await sync_to_async(User.objects.get)(Telegram_id=message.from_user.id)
        return user.Is_registered
