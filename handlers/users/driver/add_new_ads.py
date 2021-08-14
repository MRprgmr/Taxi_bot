from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ContentTypes, ReplyKeyboardRemove, CallbackQuery
from asgiref.sync import sync_to_async
from aiogram.dispatcher.filters import Text
from Bot.models import Province, User, Ads, Region
from filters.driver_filters import StartCreateAds
from handlers.users.most_uses import send_main_menu
from keyboards.default.new_ads_buttons import cancel_button
from keyboards.inline.ads_create_buttons import confirm_new_ads, has_mail_button
from keyboards.inline.calendar import SimpleCalendar
from keyboards.inline.callbackdatas import Province_callback, Region_callback, calendar_callback
from keyboards.inline.select_locations import select_province, select_region
from loader import dp
from states.create_ads_states import create_ads_states


@dp.message_handler(StartCreateAds())
async def start_create_ads(message: Message):
    usr = await sync_to_async(User.objects.get)(Telegram_id=message.from_user.id)
    is_available = await sync_to_async(usr.ads.filter(status=True).count)() <= 0
    if is_available:
        await message.answer("📝 Yangi e'lon yaratish", reply_markup=cancel_button)

        provinces = await sync_to_async(Province.objects.order_by)('Name')
        provinces_markup = await sync_to_async(select_province)(provinces=provinces, direction='from')

        await message.answer("———— Qayerdan?\n\n↗️ Qaysi viloyatdan yo'lga chiqyapsiz?",
                             reply_markup=provinces_markup)

        await create_ads_states.from_location_province.set()
    else:
        await message.answer(
            "✖️ Kechirasiz xozirda sizda aktiv e'lon bor.\n E'lonni <b>🔉 Mening e’lonlarim</b> orqali ko'rishingiz "
            "mumkin.")


@dp.callback_query_handler(Province_callback.filter(direction='from'), state=create_ads_states.from_location_province)
async def select_current_province(call: CallbackQuery, state: FSMContext, callback_data: dict):
    await state.update_data(from_province=callback_data)

    province = await sync_to_async(Province.objects.get)(id=callback_data['id'])
    reg = await sync_to_async(province.regions.order_by)('Name')
    regions = await sync_to_async(select_region)(regions=reg, direction='from')

    await call.message.edit_text(
        f"———— Qayerdan?\n\n<b>Viloyat:</b>  {callback_data['name']}\n\n📌 Qaysi tumandan yo'lga chiqyapsiz?",
        reply_markup=regions)

    await create_ads_states.from_location_region.set()


@dp.callback_query_handler(Region_callback.filter(direction='from'), state=create_ads_states.from_location_region)
async def select_current_region(call: CallbackQuery, state: FSMContext, callback_data: dict):
    await state.update_data(from_region=callback_data)

    data = await state.get_data()
    if data['from_province']['name'] == "Toshkent":
        provinces = await sync_to_async(Province.objects.exclude)(Name="Toshkent")
    else:
        provinces = await sync_to_async(Province.objects.get)(Name="Toshkent")
        provinces = [provinces]

    provinces_markup = await sync_to_async(select_province)(provinces=provinces, direction='to')
    await call.message.edit_text(text="———— Qayerga?\n\n↙️ Qaysi viloyatga yo'lga chiqyapsiz?",
                                 reply_markup=provinces_markup)
    await create_ads_states.to_location_province.set()


@dp.callback_query_handler(Province_callback.filter(direction='to'), state=create_ads_states.to_location_province)
async def select_destination_province(call: CallbackQuery, state: FSMContext, callback_data: dict):
    await state.update_data(to_province=callback_data)

    province = await sync_to_async(Province.objects.get)(id=callback_data['id'])
    reg = await sync_to_async(province.regions.order_by)('Name')
    regions = await sync_to_async(select_region)(regions=reg, direction='to')

    await call.message.edit_text(f"———— Qayerga?\n\n<b>Viloyat:</b>  {callback_data['name']}\n\n📍 Qaysi tumanga "
                                 "yo'lga chiqyapsiz?",
                                 reply_markup=regions)

    await create_ads_states.to_location_region.set()


@dp.callback_query_handler(Region_callback.filter(direction='to'), state=create_ads_states.to_location_region)
async def select_current_region(call: CallbackQuery, state: FSMContext, callback_data: dict):
    await state.update_data(to_region=callback_data)
    await call.message.edit_text("📦 Pochta olasizmi?", reply_markup=has_mail_button)
    await create_ads_states.has_mail.set()


@dp.callback_query_handler(Text(startswith='mail'), state=create_ads_states.has_mail)
async def check_has_mail(call: CallbackQuery, state: FSMContext):
    if call.data == 'mail_true':
        await state.update_data(mail=True)
    else:
        await state.update_data(mail=False)
    await call.message.edit_text(
        "📅 Qaysi sanaga yo'lga chiqmoqchisiz?\n\n",
        reply_markup=await SimpleCalendar().start_calendar())
    await create_ads_states.scheduled_date.set()


@dp.callback_query_handler(calendar_callback.filter(), state=create_ads_states.scheduled_date)
async def get_date(call: CallbackQuery, state: FSMContext, callback_data: dict):
    selected, date = await SimpleCalendar().process_selection(call, callback_data)
    if selected:
        await state.update_data(scheduled_date=date)
        user_data = await sync_to_async(User.objects.select_related('Car').get)(Telegram_id=call.message.chat.id)
        data = await state.get_data()
        if data['mail']:
            mail = "Bor"
        else:
            mail = "Yo'q"
        answer = "\n".join([
            "<b>ℹ️ E'lon ma'lumotlari:</b>\n",
            f"<b>📌 Qayerdan:</b>  {data['from_province']['name']}, {data['from_region']['name']}\n",
            f"<b>📍Qayerga:</b>  {data['to_province']['name']}, {data['to_region']['name']}\n",
            f"<b>📦 Pochta:</b>   {mail}\n",
            f"<b>📅 Sana:</b>   {data['scheduled_date'].strftime('%A, %e-%B, %Y')}\n",
            f"<b>📞 Telefon:</b>  {user_data.Phone_number}\n",
            f"<b>🚕 Avtomobil:</b>  {user_data.Car.Name}"
        ])
        await call.message.edit_text(text=answer, reply_markup=confirm_new_ads)
        await create_ads_states.confirm_new_ads.set()
    else:
        await call.answer()


@dp.callback_query_handler(text="confirm_new_ads", state=create_ads_states.confirm_new_ads)
async def confirm_ads(call: CallbackQuery, state: FSMContext):
    await call.answer("✅ Eloningiz e'lonlar ro'yhatiga qo'shildi", show_alert=True)
    data = await state.get_data()
    await state.finish()
    driver = await sync_to_async(User.objects.get)(Telegram_id=call.message.chat.id)
    From = await sync_to_async(Region.objects.get)(id=data['from_region']['id'])
    To = await sync_to_async(Region.objects.get)(id=data['to_region']['id'])
    await sync_to_async(Ads.objects.create)(Driver=driver, From=From, To=To, scheduled_date=data['scheduled_date'], has_mail=data['mail'])
    await call.message.delete()
    await send_main_menu(call.message.chat.id)


@dp.message_handler(text='❌ Bekor qilish', content_types=ContentTypes.TEXT, state=create_ads_states)
async def cancel_ads(message: Message, state: FSMContext):
    await message.answer("E'lon bekor qilindi.", reply_markup=ReplyKeyboardRemove())
    await state.finish()
    await send_main_menu(message.from_user.id)
