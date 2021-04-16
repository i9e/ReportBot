from aiogram import types
from misc import dp, bot
from config import ADMIN_ID
from styles import keyboards

@dp.message_handler(content_types=types.ContentTypes.ANY)
async def all_other_messages(message):
    await bot.forward_message(chat_id=ADMIN_ID, from_chat_id=message.chat.id, message_id=message.message_id)
    await message.answer("Ошибка! Пожалуйста, воспользуйтесь меню для подачи жалобы.\n"
                         "Если Вам кажется, ошибок быть не должно, пожалуйста, напишите нам! "
                         "Например, через пункт «Обратная связь» в меню\n\n Возможно, Вам поможет команда /help",
                         reply_markup = keyboards.menu_button)