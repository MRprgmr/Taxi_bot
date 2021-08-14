from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ContentTypes, ForceReply

from data.config import ADMINS
from filters.is_registered import IsRegistered
from handlers.users.most_uses import send_main_menu
from loader import dp
from states.common_states import Feedback


@dp.message_handler(IsRegistered(), text="💬 Fikr bildirish")
async def send_feedback(message: Message):
    await message.answer("Bot haqida fikringiz yoki taklifingiz bo'lsa izohda qoldiring: ", reply_markup=ForceReply())
    await Feedback.FeedbackState.set()


@dp.message_handler(content_types=ContentTypes.TEXT, state=Feedback.FeedbackState)
async def send(message: Message, state: FSMContext):
    await state.finish()
    feedback_text = "\n".join([
        f"💬 New feedback from {message.from_user.get_mention(as_html=True)}",
        f"<code>",
        message.text,
        "</code>",
    ])
    await message.answer("Izohlaringiz uchun raxmat, siz bilan tez orada aloqaga chiqishga xarakat qilamiz 😉.")
    await send_main_menu(message.from_user.id)
    for i in ADMINS:
        await dp.bot.send_message(i, feedback_text)
