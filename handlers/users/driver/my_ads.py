from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from asgiref.sync import sync_to_async

from Bot.models import User, Ads
from filters.driver_filters import MyAds
from keyboards.inline.ads_create_buttons import delete_ads_button
from loader import dp


@dp.message_handler(MyAds(), state='*')
async def show_my_ads(message: Message, state: FSMContext):
    usr = await sync_to_async(User.objects.get)(Telegram_id=message.from_user.id)
    try:
        ads = await sync_to_async(
            usr.ads.select_related('Driver', 'Driver__Car', 'From__Province', "From", 'To__Province',
                                   "To").get)(status=True)
        if ads.has_mail:
            mail = "Bor"
        else:
            mail = "Yo'q"
        
        answer = "\n".join([
            "<b>ℹ️ E'lon ma'lumotlari:</b>\n",
            f"<b>📌 Qayerdan:</b>  {ads.From.Province.Name}, {ads.From.Name}\n",
            f"<b>📍Qayerga:</b>  {ads.To.Province.Name}, {ads.To.Name}\n",
            f"<b>📦 Pochta:</b>   {mail}\n",
            f"<b>📅 Sana:</b>   {ads.scheduled_date.strftime('%A, %e-%B, %Y')}\n",
            f"<b>📞 Telefon:</b>  {ads.Driver.Phone_number}\n",
            f"<b>🚕 Avtomobil:</b>  {ads.Driver.Car.Name}",
        ])
        await message.answer(answer, reply_markup=delete_ads_button)
    except Ads.DoesNotExist:
        await message.answer("Hozirda mavjud e'lonlaringiz yo'q")


@dp.callback_query_handler(text="delete_ads")
async def delete_ads(call: CallbackQuery):
    usr = await sync_to_async(User.objects.get)(Telegram_id=call.message.chat.id)
    try:
        ads = await sync_to_async(usr.ads.get)(status=True)
        ads.status = False
        await sync_to_async(ads.save)()
        await call.message.edit_text("✅ E'lon o'chirildi", reply_markup=None)
    except Ads.DoesNotExist:
        await call.message.edit_text("⚠️ Xatolik")
