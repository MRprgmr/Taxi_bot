from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message
from aiogram.types.callback_query import CallbackQuery
from asgiref.sync import sync_to_async

from Bot.models import Ads, Province, Region, User
from filters.is_registered import IsRegistered
from handlers.users.most_uses import send_main_menu
from keyboards.default import ads_filters
from keyboards.default.ads_filters import ads_filters_buttons
from keyboards.inline.ads_view import get_ads
from keyboards.inline.calendar import SimpleCalendar
from keyboards.inline.callbackdatas import AddAdsToSaved, AdsView_callback, Province_callback, Region_callback, \
    calendar_callback
from keyboards.inline.saved_ads_view import get_ads as get_ads2
from keyboards.inline.select_locations import select_province, select_region
from loader import dp
from states.ads_view_filetrs_state import Ads_Filters
from states.common_states import SavedAdsState


def get_available_ads_count(queryset):
    result = {}
    for ads in queryset:
        result.setdefault(ads.scheduled_date, 0)
        result[ads.scheduled_date] += 1
    return result


def add_ads_to_saved(ads_id, queryset, user_tgid):
    user = User.objects.get(Telegram_id=user_tgid)
    ads = queryset['filtered_ads'][int(ads_id)]
    user.Saved_Ads.add(ads)


def check_location_availability(data):
    region_from = Region.objects.get(id=int(data['from_region']['id']))
    region_to = Region.objects.get(id=int(data['to_region']['id']))
    count = Ads.objects.filter(From=region_from, To=region_to, status=True).count()
    if count == 0:
        return False
    else:
        return True


@dp.message_handler(IsRegistered(), Text(equals=["🔍 Taxi qidirish"]), state='*')
async def show_posts(message: Message, state: FSMContext):
    await state.finish()
    await Ads_Filters.from_province.set()
    await message.answer("Elonlarni saralash uchun\nma'lumotlarni to'ldiring:", reply_markup=ads_filters_buttons)
    provinces = await sync_to_async(Province.objects.order_by)('Name')
    provinces_markup = await sync_to_async(select_province)(provinces=provinces, direction='from')
    await message.answer("———— Qayerdan?\n\n↗️ Qaysi viloyatdan yo'lga chiqyapsiz?",
                         reply_markup=provinces_markup)


@dp.callback_query_handler(Province_callback.filter(direction='from'), state=Ads_Filters.from_province)
async def select_current_province(call: CallbackQuery, state: FSMContext, callback_data: dict):
    await state.update_data(from_province=callback_data)

    province = await sync_to_async(Province.objects.get)(id=callback_data['id'])
    reg = await sync_to_async(province.regions.order_by)('Name')
    regions = await sync_to_async(select_region)(regions=reg, direction='from')

    await call.message.edit_text(
        f"———— Qayerdan?\n\n<b>Viloyat:</b>  {callback_data['name']}\n\n📌 Qaysi tumandan yo'lga chiqyapsiz?",
        reply_markup=regions)

    await Ads_Filters.from_region.set()


@dp.callback_query_handler(Region_callback.filter(direction='from'), state=Ads_Filters.from_region)
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
    await Ads_Filters.to_province.set()


@dp.callback_query_handler(Province_callback.filter(direction='to'), state=Ads_Filters.to_province)
async def select_destination_province(call: CallbackQuery, state: FSMContext, callback_data: dict):
    await state.update_data(to_province=callback_data)

    province = await sync_to_async(Province.objects.get)(id=callback_data['id'])
    reg = await sync_to_async(province.regions.order_by)('Name')
    regions = await sync_to_async(select_region)(regions=reg, direction='to')

    await call.message.edit_text(f"———— Qayerga?\n\n<b>Viloyat:</b>  {callback_data['name']}\n\n📍 Qaysi tumanga "
                                 "yo'lga chiqyapsiz?",
                                 reply_markup=regions)

    await Ads_Filters.to_region.set()


@dp.callback_query_handler(Region_callback.filter(direction='to'), state=Ads_Filters.to_region)
async def select_destination_region(call: CallbackQuery, state: FSMContext, callback_data: dict):
    await state.update_data(to_region=callback_data)
    data = await state.get_data()
    if (await sync_to_async(check_location_availability)(data)):
        await call.message.edit_text(
            "📅 Qaysi sanaga yo'lga chiqmoqchisiz?\n\n",
            reply_markup=await SimpleCalendar().start_calendar())
        await Ads_Filters.scheduled_date.set()
    else:
        await call.answer("Kechirasiz ushbu manzil bo'yicha hozircha e'lon yo'q, boshqa manzillardan urinib ko'ring",
                          show_alert=True)


@dp.callback_query_handler(calendar_callback.filter(), state=Ads_Filters.scheduled_date)
async def get_date(call: CallbackQuery, state: FSMContext, callback_data: dict):
    selected, date = await SimpleCalendar().process_selection(call, callback_data)
    if selected:
        await state.update_data(scheduled_date=date)

        ads_filters = await state.get_data()
        from_region = await sync_to_async(Region.objects.get)(id=ads_filters['from_region']['id'])
        to_region = await sync_to_async(Region.objects.get)(id=ads_filters['to_region']['id'])

        filtered_ads = await sync_to_async(Ads.objects.filter)(
            From=from_region, To=to_region, scheduled_date=ads_filters['scheduled_date'], status=True)
        filtered_ads = await sync_to_async(filtered_ads.order_by)('id')
        await state.update_data(filtered_ads=filtered_ads)

        if (await sync_to_async(filtered_ads.count)()) == 0:
            available_ads = await sync_to_async(Ads.objects.filter)(From=from_region, To=to_region, status=True)
            available_ads = await sync_to_async(available_ads.order_by)('scheduled_date')
            available_ads = await sync_to_async(get_available_ads_count)(available_ads)
            if len(available_ads) == 0:
                await call.answer("Kechirasiz siz bergan manzillar bo'yicha hech qanday e'lon topilmadi.",
                                  show_alert=True)
            text = "Kechirasi ushbu sana uchun hech qanday e'lon topilmadi, lekin quyidagi sanalarda e'lonlar mavjud:\n\n"
            for k, val in available_ads.items():
                text += f"{k.strftime('%A, %e-%B')}  —  {val} ta\n"
            await call.answer(text, show_alert=True)
        else:
            answer = await sync_to_async(get_ads)(call.message.chat.id, 0, filtered_ads)
            await call.message.edit_text(text=answer['text'], reply_markup=answer['markup'])
            await Ads_Filters.view_ads.set()
    else:
        await call.answer()


@dp.callback_query_handler(AddAdsToSaved.filter(), state=Ads_Filters.view_ads)
async def add_ads_tosaved(call: CallbackQuery, state: FSMContext, callback_data: dict):
    data = await state.get_data()
    await sync_to_async(add_ads_to_saved)(callback_data['ads_id'], data, call.message.chat.id)
    answer = await sync_to_async(get_ads)(call.message.chat.id, int(callback_data['ads_id']), data['filtered_ads'])
    await call.message.edit_text(answer['text'], reply_markup=answer['markup'])
    await call.answer("E'lon saqlanganlar ro'yxatiga qo'shildi")


@dp.callback_query_handler(AdsView_callback.filter(action='show'), state=Ads_Filters.view_ads)
async def change_current_ads(call: CallbackQuery, state: FSMContext, callback_data: dict):
    data = await state.get_data()
    answer = await sync_to_async(get_ads)(call.message.chat.id, int(callback_data['ads_id']), data['filtered_ads'])
    await call.message.edit_text(answer['text'], reply_markup=answer['markup'])


@dp.callback_query_handler(text="saved_ads", state=Ads_Filters.view_ads)
async def go_to_saved(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.delete()
    await call.message.answer("Saqlangan e'lonlar:", reply_markup=ads_filters.ads_filters_buttons)
    user = await sync_to_async(User.objects.get)(Telegram_id=call.message.chat.id)
    user: User
    saved_ads = await sync_to_async(user.Saved_Ads.filter)(status=True)
    await state.update_data(saved_ads_queryset=saved_ads)
    if (await sync_to_async(saved_ads.count)()) == 0:
        await call.message.answer("Kechirasiz hozirda sizada xech qanday saqlangan e'lon yo'q")
    else:
        await SavedAdsState.ViewAds.set()
        answer = await sync_to_async(get_ads2)(0, saved_ads)
        await call.message.answer(text=answer['text'], reply_markup=answer['markup'])


@dp.callback_query_handler(text="null", state='*')
async def answer_null(call: CallbackQuery):
    await call.answer()


@dp.message_handler(text="↩️ Bosh menu", state=Ads_Filters)
async def go_back(message: Message, state: FSMContext):
    await state.finish()
    await send_main_menu(message.from_user.id)
