from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

RegisterButton = InlineKeyboardMarkup(row_width=1,
                                      inline_keyboard=[
                                          [
                                              InlineKeyboardButton(
                                                  text="Ro'yxatdan o'tish 📝",
                                                  callback_data="register",
                                              )
                                          ]
                                      ])

AcceptButton = InlineKeyboardMarkup(row_width=2,
                                    inline_keyboard=[
                                        [
                                            InlineKeyboardButton(
                                                text="✅ Tasdiqlash",
                                                callback_data="accept",
                                            )
                                        ],
                                        [
                                            InlineKeyboardButton(
                                                text="🔄 Qayta to'ldirish",
                                                callback_data="refill",
                                            )
                                        ]
                                    ])
