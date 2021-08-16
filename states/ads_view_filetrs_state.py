from aiogram.dispatcher.filters.state import StatesGroup, State


class Ads_Filters(StatesGroup):
    from_province = State()
    from_region = State()
    to_province = State()
    to_region = State()
    scheduled_date = State()
    view_ads = State()
