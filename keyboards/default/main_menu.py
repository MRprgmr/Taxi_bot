from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

main_menu_user = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2,
                                     keyboard=[
                                         [
                                             KeyboardButton(
                                                 text="π Taxi qidirish"),
                                             KeyboardButton(
                                                 text="π Saqlangan e'lonlar")
                                         ],
                                         [
                                             KeyboardButton(
                                                 text="π¬ Fikr bildirish"),
                                             KeyboardButton(text="π¨βπ» Bot Haqida"),
                                         ],
                                     ])

main_menu_driver = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2,
                                       keyboard=[
                                           [
                                               KeyboardButton(
                                                   text="β Yangi eβlon"),
                                               KeyboardButton(
                                                   text="π¨ Mening eβlonlarim"),
                                           ],
                                           [
                                               KeyboardButton(
                                                   text="π¬ Fikr bildirish"),
                                               KeyboardButton(
                                                   text="π¨βπ» Bot Haqida"),
                                           ],
                                       ])
