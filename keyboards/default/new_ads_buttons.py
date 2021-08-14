from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

cancel_button = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1,
                                    keyboard=[
                                        [
                                            KeyboardButton(
                                                text="❌ Bekor qilish"),
                                        ],
                                    ])
