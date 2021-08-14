from aiogram.utils.callback_data import CallbackData

CarType_callback = CallbackData('CarType', 'name', 'id')
Province_callback = CallbackData('Province', 'direction', 'name', 'id')
Region_callback = CallbackData('Region', 'direction', 'name', 'id')
calendar_callback = CallbackData('simple_calendar', 'act', 'year', 'month', 'day')
AdsView_callback = CallbackData('AdsView', 'action', 'ads_id')
AddAdsToSaved = CallbackData('AddToSaved', 'ads_id')
DeleteSavedAds = CallbackData('Delete', 'ads_id')