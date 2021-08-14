from aiogram.dispatcher.storage import FSMContext
from aiogram.dispatcher.filters.builtin import Command
from asgiref.sync import sync_to_async
from aiogram.types.message import Message
from aiogram.types.reply_keyboard import ReplyKeyboardRemove
from filters.is_admin import IsAdmin
from Bot.models import User, Ads
from aiogram.types import ContentTypes as ct
from loader import dp
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
import asyncio
from .most_uses import send_main_menu
from datetime import datetime


# show admin commands --------------------------------------------
@dp.message_handler(IsAdmin(), Command('commands'))
async def show_admin_commands(message: Message):
    answer = "\n".join([
        "Admin commands:\n",
        "/status — show current status of the bot,",
        "/broadcast — send broadcast to bot users.",
    ])
    await message.answer(answer)
# -----------------------------------------------------------------


# show bot statistics
def get_status_info():
    # users statistics
    users = User.objects.all()
    joined_count = users.count()
    unregistered_users = users.filter(Is_registered=False).count()
    unregistered_users_today = users.filter(
        Is_registered=False, Joined_date=datetime.now()).count()
    today_joined = users.filter(Joined_date=datetime.today()).count()
    drivers_count = users.filter(Is_registered=True, Is_Driver=True).count()
    users_count = users.filter(Is_registered=True, Is_Driver=False).count()
    drivers_count_today = users.filter(
        Is_registered=True, Is_Driver=True, Joined_date=datetime.today()).count()
    users_count_today = users.filter(
        Is_registered=True, Is_Driver=False, Joined_date=datetime.today()).count()

    # ads statistics
    ads = Ads.objects.all()
    total_ads = ads.count()
    active = ads.filter(status=True).count()
    today_added_ads = ads.filter(created_date=datetime.today()).count()

    result = "\n".join([
        "📊 Bot statistics:\n",
        f"<b>Total joined:</b>    {joined_count},   <code>+ {today_joined}</code>",
        f"<b>Unregistered joiners:</b>    {unregistered_users},   <code>+ {unregistered_users_today}</code>",
        f"<b>Registrated drivers:</b>    {drivers_count},   <code>+ {drivers_count_today}</code>",
        f"<b>Registrated users:</b>    {users_count},   <code>+ {users_count_today}</code>",
        f"<b>Total added ads:</b>    {total_ads},   <code>+ {today_added_ads}</code>",
        f"<b>Current active ads:</b>    {active}"
    ])
    return result

@dp.message_handler(IsAdmin(), Command('status'))
async def show_bot_status(message: Message):
    statistics = await sync_to_async(get_status_info)()
    await message.answer(statistics)
# -------------------------------------------------------------------


# broadcast ---------------------------------------------------------
cancel_button = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1,
                                    keyboard=[
                                        [
                                            KeyboardButton(
                                                text="❌ Cancel broadcast"),
                                        ],
                                    ])


class BroadCastState(StatesGroup):
    start = State()


def get_users():
    users = User.objects.all()
    result = []
    for usr in users:
        result.append(usr.Telegram_id)
    return result


@dp.message_handler(IsAdmin(), Command('broadcast'))
async def send_broadcast(message: Message):
    await message.answer("Send a message to be broadcast:", reply_markup=cancel_button)
    await BroadCastState.start.set()


@dp.message_handler(IsAdmin(), text="❌ Cancel broadcast", state=BroadCastState.start)
async def cancel(message: Message, state: FSMContext):
    await state.finish()
    await message.answer("Canceled.", reply_markup=ReplyKeyboardRemove())
    await send_main_menu(message.from_user.id)


@dp.message_handler(IsAdmin(), content_types=ct.TEXT | ct.AUDIO | ct.PHOTO | ct.VIDEO | ct.VIDEO_NOTE, state=BroadCastState.start)
async def send_broadcast_start(message: Message, state: FSMContext):
    await message.answer("Broadcast started...")
    users_ids = await sync_to_async(get_users)()
    count = 0
    try:
        for user_id in users_ids:
            try:
                await message.send_copy(user_id)
                count += 1
            except:
                pass
        await asyncio.sleep(.05)
    finally:
        await message.answer(f"Message sent to {count} users.")
    await send_main_menu(message.from_user.id)
    await state.finish()
# ------------------------------------------------------------------------
