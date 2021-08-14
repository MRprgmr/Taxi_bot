from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

main_menu_user = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2,
                                     keyboard=[
                                         [
                                             KeyboardButton(
                                                 text="🔍 Taxi qidirish"),
                                             KeyboardButton(
                                                 text="📑 Saqlangan e'lonlar")
                                         ],
                                         [
                                             KeyboardButton(
                                                 text="💬 Fikr bildirish"),
                                             KeyboardButton(text="👨‍💻 Bot Haqida"),
                                         ],
                                     ])

main_menu_driver = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2,
                                       keyboard=[
                                           [
                                               KeyboardButton(
                                                   text="➕ Yangi e’lon"),
                                               KeyboardButton(
                                                   text="📨 Mening e’lonlarim"),
                                           ],
                                           [
                                               KeyboardButton(
                                                   text="💬 Fikr bildirish"),
                                               KeyboardButton(
                                                   text="👨‍💻 Bot Haqida"),
                                           ],
                                       ])
