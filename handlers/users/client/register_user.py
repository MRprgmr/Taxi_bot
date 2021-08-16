import re

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, Message, ContentTypes, \
    ReplyKeyboardRemove
from asgiref.sync import sync_to_async

from Bot.models import User
from keyboards.default.main_menu import main_menu_user
from keyboards.default.send_contact import request_contract
from keyboards.inline.register_button import AcceptButton
from keyboards.inline.type_users import TypesMarkup
from loader import dp
from states.register_state import RegisterUser


def make_name_button(name):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton(name))
    return markup


@dp.callback_query_handler(state=RegisterUser.start_registration)
async def select_type(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)
    if call.data == "register":
        await call.message.edit_text(text="🤖: Botdan kim sifatida foydalanmoqchisiz?", reply_markup=TypesMarkup)
        await RegisterUser.select_type.set()


@dp.callback_query_handler(state=RegisterUser.select_type, text="type_passenger")
async def register_user(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)
    await state.update_data(user_type=call.data)
    await RegisterUser.name.set()
    await call.message.answer(text="\n".join([
        "   ☑️  ⬜️  ️\n",
        "1. Ismingizni kiriting:",
    ]), reply_markup=make_name_button(call.message.chat.first_name))


@dp.message_handler(state=RegisterUser.name, content_types=ContentTypes.TEXT)
async def get_name(message: Message, state: FSMContext):
    if len(message.text) >= 3 and message.text.isalpha():
        await state.update_data(name=message.text)
        answer_text = "\n".join([
            "   ✅  ☑️\n",
            "2. Telefon raqamingizni <b>+998XXXXXXXXX</b> formatida jo'nating\nyoki <b>📲 Raqamni jo'natish</b> "
            "tugmasini bosing:",
        ])
        await message.answer(text=answer_text, reply_markup=request_contract)
        await RegisterUser.phone_number.set()
    else:
        await message.answer(
            "☝️ Foydalnuvchi ismi kamida 3 ta harfdan iborat bo'lishi shart, iltimos ismingizni qayta kiriting:")


@dp.message_handler(state=RegisterUser.phone_number, content_types=ContentTypes.TEXT | ContentTypes.CONTACT)
async def get_number(message: Message, state: FSMContext):
    if message.content_type == 'contact':
        phone_number = message.contact.phone_number
    else:
        phone_number = message.text
    if phone_number[0] != '+':
        phone_number = '+' + phone_number

    if re.match(r"\+998(?:33|93|94|97|90|91|98|99|95|88)\d\d\d\d\d\d\d", phone_number) is not None:
        await state.update_data(phone_number=phone_number)
        data = await state.get_data()
        answer_text = "\n".join([
            "   ✅  ✅  \n",
            f"<b>Foydalanuvchi turi:</b>   Yo'lovchi 🤵",
            f"<b>Ism:</b>   {data['name']}",
            f"<b>Telefon:</b>   {data['phone_number']}\n",
            "Ma'lumotlarni tasdiqlaysizmi ❔",
        ])
        msg = await message.answer("🔄", reply_markup=ReplyKeyboardRemove())
        await msg.delete()
        await dp.bot.send_message(chat_id=message.chat.id, text=answer_text, reply_markup=AcceptButton)
        await RegisterUser.confirmation.set()
    else:
        await message.answer(
            "❌ Telefon nomeri xato kiritildi, iltimos qayta kiriting:\n\n☝️ Raqam <b>+998xxxxxxx</b> formatida "
            "bo'lishi kerak.")


@dp.callback_query_handler(state=RegisterUser.confirmation)
async def confirm_user_information(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)
    if call.data == 'accept':
        data = await state.get_data()
        user = await sync_to_async(User.objects.get)(Telegram_id=call.message.chat.id)
        user.Name = data['name']
        user.Phone_number = data['phone_number']
        user.Is_registered = True
        user.Is_Driver = False
        user.Age = None
        user_ads = await sync_to_async(user.Saved_Ads)()
        for ads in await sync_to_async(user_ads.all)():
            ads.status = False
            await sync_to_async(ads.save)()
        await sync_to_async(user.save)()
        await call.message.delete()
        await call.message.answer(text='\n'.join([
            "    ✅ ✅ ✅  \n",
            "Tabriklaymiz siz muvaffaqiyatli ro‘yxatdan o‘tdingiz,",
            "endi botdan foydalanishingiz mumkin.\n",
            "🙋 Yordam uchun /help ni bosing."
        ]), reply_markup=main_menu_user)
        await state.finish()
    elif call.data == 'refill':
        await call.message.edit_text(text="🤖: Botdan kim sifatida foydalanmoqchisiz?", reply_markup=TypesMarkup)
        await RegisterUser.select_type.set()
