from datetime import datetime
from celery import shared_task
from Bot.models import User, Ads
from loader import bot
import asyncio

loop = asyncio.get_event_loop()

async def remind_driver(id):
    await bot.send_message(chat_id=id, text=f"Sizning e'loningiz rejalangan muddatdan qolib ketgani uchun o'chirildi.")
    await asyncio.sleep(.05)

@shared_task
def clear_expired_ads():
    expireds = Ads.objects.filter(scheduled_date__lt=datetime.today(), status=True)
    loop.run_until_complete(bot.send_message(973021229, f"All expired ads were deleted, count:  {expireds.count()}"))
    for ads in expireds:
        ads.status = False
        ads.save()
        loop.run_until_complete(remind_driver(ads.Driver.Telegram_id))