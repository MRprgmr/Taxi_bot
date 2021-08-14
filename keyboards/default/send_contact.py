from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

request_contract = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📲 Raqamni jo'natish", request_contact=True),
        ],
    ],
    resize_keyboard=True,
)
