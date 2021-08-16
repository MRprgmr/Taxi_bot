import calendar
from datetime import datetime, timedelta

from aiogram.types import CallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callbackdatas import calendar_callback


def check_date(year, month, day):
    if (datetime.today() - timedelta(days=1)) <= datetime(year, month, day) <= (datetime.today() + timedelta(days=6)):
        return True
    else:
        return False


class SimpleCalendar:

    async def start_calendar(
            self,
            year: int = datetime.now().year,
            month: int = datetime.now().month
    ) -> InlineKeyboardMarkup:
        inline_kb = InlineKeyboardMarkup(row_width=7)
        ignore_callback = calendar_callback.new("IGNORE", year, month, 0)
        inline_kb.row()
        inline_kb.insert(InlineKeyboardButton(
            f'{calendar.month_name[month]} {str(year)}',
            callback_data=ignore_callback
        ))
        inline_kb.row()
        for day in ["Du", "Se", "Chor", "Pay", "Jum", "Shan", "Yak"]:
            inline_kb.insert(InlineKeyboardButton(
                day, callback_data=ignore_callback))
        month_calendar = calendar.monthcalendar(year, month)
        for week in month_calendar:
            inline_kb.row()
            for day in week:
                if day == 0:
                    inline_kb.insert(InlineKeyboardButton(
                        " ", callback_data=ignore_callback))
                    continue
                if check_date(year, month, day):
                    if datetime.today().date() == datetime(year=year, month=month, day=day).date():
                        inline_kb.insert(InlineKeyboardButton(
                            str(f"[ {day} ]"), callback_data=calendar_callback.new("DAY", year, month, day)
                        ))
                    else:
                        inline_kb.insert(InlineKeyboardButton(
                            str(day), callback_data=calendar_callback.new("DAY", year, month, day)
                        ))
                else:
                    inline_kb.insert(InlineKeyboardButton(
                        " ", callback_data=ignore_callback))
        inline_kb.row()
        inline_kb.insert(InlineKeyboardButton(
            "<", callback_data=calendar_callback.new("PREV-MONTH", year, month, day)
        ))
        inline_kb.insert(InlineKeyboardButton(
            " ", callback_data=ignore_callback))
        inline_kb.insert(InlineKeyboardButton(
            ">", callback_data=calendar_callback.new("NEXT-MONTH", year, month, day)
        ))

        return inline_kb

    async def process_selection(self, query: CallbackQuery, data: dict) -> tuple:
        return_data = (False, None)
        temp_date = datetime(int(data['year']), int(data['month']), 1)
        if data['act'] == "IGNORE":
            await query.answer(cache_time=60)
        if data['act'] == "DAY":
            return_data = True, datetime(
                int(data['year']), int(data['month']), int(data['day']))
        if data['act'] == "PREV-MONTH":
            prev_date = temp_date - timedelta(days=1)
            await query.message.edit_reply_markup(await self.start_calendar(int(prev_date.year), int(prev_date.month)))
        if data['act'] == "NEXT-MONTH":
            next_date = temp_date + timedelta(days=31)
            await query.message.edit_reply_markup(await self.start_calendar(int(next_date.year), int(next_date.month)))
        return return_data
