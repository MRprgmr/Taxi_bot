from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from Bot.models import Car
from keyboards.inline.callbackdatas import CarType_callback


def get_cars():
    CarModels = InlineKeyboardMarkup()
    data = Car.objects.order_by('Name')
    for car in data:
        CarModels.add(InlineKeyboardButton(
            text=car.Name,
            callback_data=CarType_callback.new(name=car.Name, id=car.id),
        ))
    return CarModels
