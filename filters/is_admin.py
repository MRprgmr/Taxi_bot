from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message
from data.config import ADMINS


class IsAdmin(BoundFilter):
    async def check(self, message: Message):
        if str(message.from_user.id) in ADMINS:
            return True
        else:
            return False
