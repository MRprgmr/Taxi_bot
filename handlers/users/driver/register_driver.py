import re

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, Message, ContentTypes, ReplyKeyboardRemove
from asgiref.sync import sync_to_async

from Bot.models import User, Car
from keyboards.default.main_menu import main_menu_driver
from keyboards.default.send_contact import request_contract
from keyboards.inline.callbackdatas import CarType_callback
from keyboards.inline.register_button import AcceptButton
from keyboards.inline.type_cars import get_cars
from keyboards.inline.type_users import TypesMarkup
from loader import dp
from states.register_state import RegisterDriver, RegisterUser


def make_name_button(name):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton(name))
    return markup


@dp.callback_query_handler(state=RegisterUser.select_type, text="type_driver")
async def register_driver(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)
    await state.update_data(user_type=call.data)
    await RegisterDriver.name.set()
    await call.message.answer(text="\n".join([
        "   ☑️  ⬜️  ⬜️  ⬜\n",
        "1. Ismingizni kiriting:",
    ]), reply_markup=make_name_button(call.message.chat.first_name))


@dp.message_handler(state=RegisterDriver.name, content_types=ContentTypes.TEXT)
async def get_name(message: Message, state: FSMContext):
    if len(message.text) >= 3 and message.text.isalpha():
        await state.update_data(name=message.text)
        answer_text = "\n".join([
            "   ✅  ☑️  ⬜️  ⬜\n",
            "2. Telefon raqamingizni kiritish uchun:\n\n<b>📞 Yuborish</b> tugmasini bosing yoki boshqa raqamni quyidagi ",
            "ko'rinishda yozing!\n\n👉 +998901234567",
        ])
        await message.answer(text=answer_text, reply_markup=request_contract)
        await RegisterDriver.phone_number.set()
    else:
        await message.answer(
            "☝️ Foydalnuvchi ismi kamida 3 ta harfdan iborat bo'lishi shart, iltimos ismingizni qayta kiriting:")


@dp.message_handler(state=RegisterDriver.phone_number, content_types=ContentTypes.TEXT | ContentTypes.CONTACT)
async def get_number(message: Message, state: FSMContext):
    if message.content_type == 'contact':
        phone_number = message.contact.phone_number
    else:
        phone_number = message.text
    if phone_number[0] != '+':
        phone_number = '+' + phone_number

    if re.match(r"\+998(?:33|93|94|97|90|91|98|99|95|88)\d\d\d\d\d\d\d", phone_number) is not None and len(phone_number) == 13:
        await state.update_data(phone_number=phone_number)
        msg = await message.answer("🔄", reply_markup=ReplyKeyboardRemove())
        await msg.delete()
        await message.answer(
            "   ✅  ✅  ☑️  ⬜️\n\n3. Yoshingizni kiriting:\n\n☝️ Yoshingiz 18 - 60 oralig'ida bo'lishi shart.")
        await RegisterDriver.age.set()
    else:
        await message.answer(
            "❌ Telefon nomeri xato kiritildi, iltimos qayta kiriting:\n\n☝️ Raqam <b>+998xxxxxxx</b> formatida "
            "bo'lishi kerak.")


@dp.message_handler(state=RegisterDriver.age, content_types=ContentTypes.TEXT)
async def get_age(message: Message, state: FSMContext):
    if message.text.isdigit() and 60 >= int(message.text) >= 18:
        await state.update_data(age=int(message.text))
        cars = await sync_to_async(get_cars)()
        await message.answer(text="   ✅  ✅  ✅  ☑️\n\n4. 🚕 Avtomobilingiz modelini tanlang:", reply_markup=cars)
        await RegisterDriver.car_model.set()
    else:
        await message.answer(
            "❌ Noto'g'ri yosh kiritildi, iltimos qayta kiriting:\n\n☝️ Yoshingiz 18 - 60 oralig'ida bo'lishi shart.")


@dp.callback_query_handler(CarType_callback.filter(), state=RegisterDriver.car_model)
async def select_car(call: CallbackQuery, state: FSMContext, callback_data: dict):
    await call.answer(cache_time=60)
    await state.update_data(car_model=callback_data)
    data = await state.get_data()
    answer_text = "\n".join([
        "   ✅  ✅  ✅  ✅\n",
        f"<b>Foydalanuvchi turi:</b>   Xaydovchi 🚖",
        f"<b>Ismi:</b>   {data['name']}",
        f"<b>Telefoni:</b>   {data['phone_number']}",
        f"<b>Yoshi:</b>   {data['age']}",
        f"<b>Avtomobil modeli:</b>   {data['car_model']['name']}\n",
        "Ma'lumotlarni tasdiqlaysizmi ❔",
    ])
    await call.message.edit_text(text=answer_text, reply_markup=AcceptButton)
    await RegisterDriver.confirmation.set()


@dp.callback_query_handler(state=RegisterDriver.confirmation)
async def confirm_user_information(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)
    if call.data == 'accept':
        data = await state.get_data()
        user = await sync_to_async(User.objects.get)(Telegram_id=call.message.chat.id)
        user.Name = data['name']
        user.Phone_number = data['phone_number']
        user.Age = data['age']
        user.Car = await sync_to_async(Car.objects.get)(id=data['car_model']['id'])
        user.Is_registered = True
        user.Is_Driver = True
        await sync_to_async(user.save)()
        await call.message.delete()
        await call.message.answer(text='\n'.join([
            "   ✅  ✅  ✅  ✅\n",
            "Tabriklaymiz siz muvaffaqiyatli ro‘yxatdan o‘tdingiz,",
            "endi botdan foydalanishingiz mumkin.\n",
            "🙋 Yordam uchun /help ni bosing."
        ]), reply_markup=main_menu_driver)
        await state.finish()
    elif call.data == 'refill':
        await call.message.edit_text(text="🤖: Botdan kim sifatida foydalanmoqchisiz?", reply_markup=TypesMarkup)
        await RegisterUser.select_type.set()
