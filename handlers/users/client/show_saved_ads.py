from handlers.users.most_uses import send_main_menu
from aiogram.types.callback_query import CallbackQuery
from keyboards.inline.callbackdatas import AdsView_callback, DeleteSavedAds
from keyboards.inline.saved_ads_view import get_ads
from keyboards.default import ads_filters
from aiogram.dispatcher.storage import FSMContext
from states.common_states import SavedAdsState
from Bot.models import User
from aiogram.types.message import Message
from asgiref.sync import sync_to_async
from filters.is_registered import IsRegistered
from loader import dp


def delete_saved(user, ads_id, query):
    ads = query['saved_ads_queryset'][int(ads_id)]
    user.Saved_Ads.remove(ads)


@dp.message_handler(IsRegistered(), text="📑 Saqlangan e'lonlar")
async def show_saved_ads(message: Message, state: FSMContext):
    await message.answer("Saqlangan e'lonlar:", reply_markup=ads_filters.ads_filters_buttons)
    user = await sync_to_async(User.objects.get)(Telegram_id=message.from_user.id)
    user: User
    saved_ads = await sync_to_async(user.Saved_Ads.filter)(status=True)
    await state.update_data(saved_ads_queryset=saved_ads)
    if (await sync_to_async(saved_ads.count)()) == 0:
        await message.answer("Kechirasiz hozirda sizada xech qanday saqlangan e'lon yo'q")
    else:
        await SavedAdsState.ViewAds.set()
        answer = await sync_to_async(get_ads)(0, saved_ads)
        await message.answer(text=answer['text'], reply_markup=answer['markup'])


@dp.callback_query_handler(AdsView_callback.filter(action='show'), state=SavedAdsState.ViewAds)
async def change_current_ads(call: CallbackQuery, state: FSMContext, callback_data: dict):
    data = await state.get_data()
    answer = await sync_to_async(get_ads)(int(callback_data['ads_id']), data['saved_ads_queryset'])
    await call.message.edit_text(answer['text'], reply_markup=answer['markup'])


@dp.callback_query_handler(DeleteSavedAds.filter(), state=SavedAdsState.ViewAds)
async def delete_saved_ads(call: CallbackQuery, state: FSMContext, callback_data: dict):
    data = await state.get_data()
    user = await sync_to_async(User.objects.get)(Telegram_id=call.message.chat.id)
    user: User
    await sync_to_async(delete_saved)(user, callback_data['ads_id'], data)
    await call.answer("E'lon saqlangnalar ro'yxatidan o'chirildi")
    saved_ads = await sync_to_async(user.Saved_Ads.filter)(status=True)
    await state.update_data(saved_ads_queryset=saved_ads)
    if (await sync_to_async(saved_ads.count)()) == 0:
        await call.message.edit_text("Saqlangan e'lonlar qolmadi")
    else:
        await SavedAdsState.ViewAds.set()
        answer = await sync_to_async(get_ads)(0, saved_ads)
        await call.message.edit_text(text=answer['text'], reply_markup=answer['markup'])


@dp.message_handler(text="↩️ Bosh menu")
async def return_home(message: Message, state: FSMContext):
    await state.finish()
    await send_main_menu(message.from_user.id)
