from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import markdown

from keyboards.inline.callbackdatas import AdsView_callback, DeleteSavedAds


def get_ads(id, queryset):
    ads = queryset[id]

    AdsModel = InlineKeyboardMarkup(row_width=3)

    if ads.has_mail:
        mail = "Bor"
    else:
        mail = "Yo'q"

    text = "\n".join([
        f"<b>📌 Qayerdan:</b>  {ads.From.Province.Name}, {ads.From.Name}\n",
        f"<b>📍Qayerga:</b>  {ads.To.Province.Name}, {ads.To.Name}\n",
        f"<b>📦 Pochta:</b>   {mail}\n",
        f"<b>📅 Sana:</b>   {ads.scheduled_date.strftime('%A, %e-%B, %Y')}\n",
        f"<b>🚕 Avtomobil:</b>   {ads.Driver.Car.Name}\n",
        f"<b>🚖 Xaydovchi</b>   {markdown.hlink(ads.Driver.Name, f'tg://user?id={ads.Driver.Telegram_id}')},  <b>Yoshi:</b> {ads.Driver.Age}\n",
        f"<b>📞 Telefon:</b>   {ads.Driver.Phone_number}",
    ])
    if id == 0:
        previous_button = "null"
    else:
        previous_button = AdsView_callback.new(action='show', ads_id=id - 1)
    if id == queryset.count() - 1:
        next_button = "null"
    else:
        next_button = AdsView_callback.new(action='show', ads_id=id + 1)

    AdsModel.add(
        InlineKeyboardButton(text="<",
                             callback_data=previous_button,
                             ),
        InlineKeyboardButton(text=f"{id + 1}/{queryset.count()}",
                             callback_data="null",
                             ),
        InlineKeyboardButton(text=">",
                             callback_data=next_button,
                             )
    )

    AdsModel.add(InlineKeyboardButton(text="🗑 O'chirish",
                                      callback_data=DeleteSavedAds.new(ads_id=id)))

    result = {'text': text, 'markup': AdsModel}
    return result
