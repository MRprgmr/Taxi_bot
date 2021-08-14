from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

EditProfile = InlineKeyboardMarkup(row_width=1,
                                   inline_keyboard=[
                                       [
                                           InlineKeyboardButton(
                                               text="🖋 Tahrirlash",
                                               callback_data="edit_profile",
                                           )
                                       ]
                                   ])
