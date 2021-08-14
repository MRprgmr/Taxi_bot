from aiogram.dispatcher.filters.state import StatesGroup, State


class create_ads_states(StatesGroup):
    from_location_province = State()
    from_location_region = State()
    to_location_province = State()
    to_location_region = State()
    scheduled_date = State()
    has_mail = State()
    confirm_new_ads = State()
