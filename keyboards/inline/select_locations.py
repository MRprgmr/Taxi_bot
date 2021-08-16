from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callbackdatas import Province_callback, Region_callback


def select_province(provinces, direction):
    provinces_keyboard = InlineKeyboardMarkup(row_width=1)
    for item in provinces:
        provinces_keyboard.add(
            InlineKeyboardButton(
                text=item.Name,
                callback_data=Province_callback.new(
                    direction=direction, name=item.Name, id=item.id),
            ),
        )
    return provinces_keyboard


def select_region(regions, direction):
    regions_keyboard = InlineKeyboardMarkup(row_width=2)
    for i in range(0, len(regions) - 1, 2):
        regions_keyboard.add(
            InlineKeyboardButton(
                text=regions[i].Name,
                callback_data=Region_callback.new(
                    direction=direction, name=regions[i].Name, id=regions[i].id),
            ),
            InlineKeyboardButton(
                text=regions[i + 1].Name,
                callback_data=Region_callback.new(
                    direction=direction, name=regions[i + 1].Name, id=regions[i + 1].id),
            )
        )
    if len(regions) % 2:
        regions_keyboard.add(
            InlineKeyboardButton(
                text=regions.last().Name,
                callback_data=Region_callback.new(
                    direction=direction, name=regions.last(), id=regions.last().id),
            ),
        )
    return regions_keyboard
