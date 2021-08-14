from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

confirm_new_ads = InlineKeyboardMarkup(row_width=1,
                                       inline_keyboard=[
                                           [
                                               InlineKeyboardButton(
                                                   text="✅ Tasdiqlash",
                                                   callback_data="confirm_new_ads",
                                               )
                                           ]
                                       ])

delete_ads_button = InlineKeyboardMarkup(row_width=1,
                                         inline_keyboard=[
                                             [
                                                 InlineKeyboardButton(
                                                     text="🗑 O'chirish",
                                                     callback_data="delete_ads",
                                                 )
                                             ]
                                         ])

has_mail_button = InlineKeyboardMarkup(row_width=1,
                                       inline_keyboard=[
                                           [
                                               InlineKeyboardButton(
                                                   text="✅ Ha",
                                                   callback_data="mail_true",
                                               ),
                                               InlineKeyboardButton(
                                                   text="❌ Yo'q",
                                                   callback_data='mail_false',
                                               ),
                                           ],
                                       ])
