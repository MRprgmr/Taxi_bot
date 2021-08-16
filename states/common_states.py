from aiogram.dispatcher.filters.state import StatesGroup, State


class Feedback(StatesGroup):
    FeedbackState = State()


class SavedAdsState(StatesGroup):
    ViewAds = State()
