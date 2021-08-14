from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

TypesMarkup = InlineKeyboardMarkup(row_width=2,
                                   inline_keyboard=[
                                       [
                                           InlineKeyboardButton(
                                               text="🤵 Yo'lovchi",
                                               callback_data="type_passenger",
                                           ),
                                           InlineKeyboardButton(
                                               text="🚖 Xaydovchi",
                                               callback_data="type_driver",
                                           ),
                                       ],
                                   ])
