from aiogram import types
from aiogram.dispatcher import filters, FSMContext
from config import ADMIN_ID
from misc import dp, bot
from styles import keyboards
from aiogram.dispatcher.filters.state import State, StatesGroup

class FeedbackInfo(StatesGroup):
    INFORMATION = State()
    FINISH = State()

# Обработка начала подачи жалобы
@dp.message_handler(filters.Text(equals = 'Обратная связь'))
@dp.message_handler(commands=['feedback'])
async def cmd_create_report(message: types.Message):
    await FeedbackInfo.INFORMATION.set()
    await message.answer('Опишите свой опыт использования бота в одном сообщении', reply_markup=keyboards.system_button1)

# Отмена заполнения и возвращение в главное меню
@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(filters.Text(equals='Отмена', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):

    await state.finish()
    await message.reply('Возвращаемся в главное меню', reply_markup = keyboards.menu_button)

# Оработка категории
@dp.message_handler(state=FeedbackInfo.INFORMATION)
async def answer_categoty(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Описание'] = message.text

    await message.answer("Хотите ли Вы подписаться под сообщением? Это поможет связаться с Вами при необходимости\n\n"
                         "Если Вы хотите изменить сообщение, нажмите отмена и начните заново",reply_markup=keyboards.anonymous_button)

    await FeedbackInfo.next()

# Отправляем результаты
@dp.message_handler(state=FeedbackInfo.FINISH)
async def answer_finish(message: types.Message, state: FSMContext):

    async with state.proxy() as data:
        data['Приватность'] = message.text

    await message.answer('Спасибо за ваш ответ!', reply_markup=keyboards.menu_button,
                         parse_mode=types.ParseMode.HTML)

    if data['Приватность'] == 'Анонимно':
        await bot.send_message(ADMIN_ID, f'Анонимный пользователь оставил обратную связь:\n{str(data["Описание"])}', parse_mode=types.ParseMode.HTML)
    else:
        await bot.send_message(ADMIN_ID, f'Пользователь {message.from_user.username} с ID {message.from_user.id} '
                                         f'оставил обратную:\n{str(data["Описание"])}', parse_mode=types.ParseMode.HTML)

    await state.finish()