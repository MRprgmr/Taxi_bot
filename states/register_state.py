from aiogram.dispatcher.filters.state import StatesGroup, State


class RegisterUser(StatesGroup):
    start_registration = State()
    select_type = State()
    name = State()
    phone_number = State()
    confirmation = State()


class RegisterDriver(StatesGroup):
    name = State()
    phone_number = State()
    age = State()
    car_model = State()
    confirmation = State()
