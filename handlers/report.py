from aiogram import types
from aiogram.dispatcher import filters, FSMContext
from config import ADMIN_ID
from misc import dp, bot
from styles import keyboards
from aiogram.dispatcher.filters.state import State, StatesGroup
from handlers.requests import get_address_from_coords

class ReportInfo(StatesGroup):
    CATEGORY = State()
    TITLE = State()
    DISCRIPTION = State()
    LOCATION = State()
    PHOTO = State()
    FINISH = State()

INFO_MESSAGE = 'Бот находится в стадии тестирования. Мы будем рады, если в конце вы оставите обратную связь\n\n'
INFO_MESSAGE2 = 'Спасибо за использование бота! Сейчас он активно тестируется, поэтому будем рады обратной связи\n\n'

# Обработка начала подачи жалобы
@dp.message_handler(filters.Text(equals = 'Создать жалобу️️'))
@dp.message_handler(commands=['create_report'])
async def cmd_create_report(message: types.Message):
    await ReportInfo.CATEGORY.set()
    await message.answer(INFO_MESSAGE)
    await bot.send_message(ADMIN_ID, 'Внимание, кто-то начал создавать жалобу')
    print('[Начало подачи жалобы] Дата создания: ' + str(message.date))
    await message.answer('Выберите категорию:', reply_markup=keyboards.categories_button)

# Отмена заполнения и возвращение в главное меню
@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(filters.Text(equals='Отмена', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):

    await state.finish()
    await message.reply('Вернитесь, когда понадобится', reply_markup = keyboards.menu_button)
    print('[Создание жалобы отменено]')

# Назад
@dp.message_handler(state='*', commands='back')
@dp.message_handler(filters.Text(equals='Назад', ignore_case=True), state='*')
async def back_handler(message: types.Message, state: FSMContext):
    print('[Кнопка «Назад»]')
    await message.answer("Возвращаемся на предыдуший пункт. Можете прислать новые данные",reply_markup=keyboards.system_button)
    await ReportInfo.previous()

# Оработка категории
@dp.message_handler(state=ReportInfo.CATEGORY)
async def answer_categoty(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Категория'] = message.text

    print('[Выбрана категория] ' + message.text)
    await message.answer("Опишите проблему одним предложением",reply_markup=keyboards.system_button)
    await ReportInfo.next()

# Обработка названия
@dp.message_handler(state=ReportInfo.TITLE)
async def answer_title(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Название'] = message.text

    print('[Название] ' + message.text)
    await message.answer("Более детально опишите проблему")
    await ReportInfo.next()

# Обработка описания
@dp.message_handler(state=ReportInfo.DISCRIPTION)
async def answer_discription(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Описание'] = message.text

    print('[Описание] ' + message.text)
    await message.answer("Укажите адрес или название места о котором вы говорите\n\nМожете отправить ваше местоположение, если вы там находитесь, "
                         "прикрепить геопозицию или просто написать адрес", reply_markup=keyboards.information_button)
    await ReportInfo.next()

# Обрабатываем адрес геолокацией
@dp.message_handler(state=ReportInfo.LOCATION, content_types='location')
async def answer_location(message: types.Location, state: FSMContext):
    user_position = (message.location.longitude, message.location.latitude)
    user_coordination = f'{user_position[0]},{user_position[1]}'
    adress = get_address_from_coords(user_coordination)

    async with state.proxy() as data:
        data['Адрес'] = str(adress)

    print('[Адрес] ' + str(adress))
    await message.answer("Можете добавить фото/видео или пропустить этот пункт\n\nПожалуйста, отправьте только одно фото или видео", reply_markup=keyboards.skip_button)
    await ReportInfo.next()

# Обрабатываем адрес текстом
@dp.message_handler(state=ReportInfo.LOCATION, content_types='text')
async def answer_location_text(message: types.Message, state: FSMContext):

    async with state.proxy() as data:
        data['Адрес'] = str(message.text)

    print('[Название] ' + str(message.text))
    await message.answer("Можете добавить фото/видео или пропустить этот пункт\n\nПожалуйста, отправьте только одно фото или видео", reply_markup=keyboards.skip_button)
    await ReportInfo.next()

# Обрабатываем фото
@dp.message_handler(state=ReportInfo.PHOTO, content_types=types.ContentTypes.PHOTO)
async def answer_photo(message: types.InputMediaPhoto, state: FSMContext):
    print('[Отправлено фото]\n')
    photo_id = message.photo[-1].file_id

    async with state.proxy() as data:
        data['Медиа'] = f'photo: {str(photo_id)}'

    await message.answer("Последний вопрос\n\nУкажите, хотите ли вы сохранить анонимность? В таком случае Ваши"
                         "данные не будут сохранены, но не факт, что мы сможем убедиться в достоверности"
                         "оправленной Вами жалобы, а также не сможем с Вами дополнительно связаться при"
                         "необходимости большей информации.\n\nВажно! Мы возьмём только Ваш username и user id."
                         "Если у Вас закрыты другие данные в телеграм, доступ к ним мы не получим, можете не переживать"
                         , reply_markup=keyboards.anonymous_button)

    await ReportInfo.next()

# Обрабатываем видео
@dp.message_handler(state=ReportInfo.PHOTO, content_types=types.ContentTypes.VIDEO)
async def answer_photo(message: types.InputMediaVideo, state: FSMContext):
    print('[Отправлено видео]\n')
    video_id = message.video.file_id

    async with state.proxy() as data:
        data['Медиа'] = f'video: {str(video_id)}'

    await message.answer("Последний вопрос\n\nУкажите, хотите ли вы сохранить анонимность? В таком случае Ваши"
                         "данные не будут сохранены, но не факт, что мы сможем убедиться в достоверности"
                         "оправленной Вами жалобы, а также не сможем с Вами дополнительно связаться при"
                         "необходимости большей информации.\n\nВажно! Мы возьмём только Ваш username и user id."
                         "Если у Вас закрыты другие данные в телеграм, доступ к ним мы не получим, можете не переживать"
                         , reply_markup=keyboards.anonymous_button)

    await ReportInfo.next()

# Пропускаем отправку фото
@dp.message_handler(state=ReportInfo.PHOTO, commands='skip')
@dp.message_handler(filters.Text(equals = "Пропустить"), state=ReportInfo.PHOTO)
async def answer_skip(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data ['Медиа'] = 'Фото/видео не отправлено'

    print('[Фото/видео не отправлено]')
    await message.answer("Последний вопрос\n\nУкажите, хотите ли вы сохранить анонимность? В таком случае Ваши "
                         "данные не будут сохранены, но не факт, что мы сможем убедиться в достоверности "
                         "оправленной Вами жалобы, а также не сможем с Вами дополнительно связаться при "
                         "необходимости большей информации.\n\nВажно! Мы возьмём только Ваш username и user id. "
                         "Если у Вас закрыты другие данные в телеграм, доступ к ним мы не получим, можете не переживать"
                         , reply_markup=keyboards.anonymous_button)

    await ReportInfo.next()

# Отправляем результаты
@dp.message_handler(state=ReportInfo.FINISH)
async def answer_finish(message: types.Message, state: FSMContext):

    async with state.proxy() as data:
        data['Приватность'] = message.text

    report_message = f"Категория: {data['Категория']}\n<b>{data['Название']}</b>\n" \
                     f"{data['Описание']}\nМесто: {data['Адрес']}\n\n" \
                     f"Дата обращения: {message.date}"

    await message.answer('Спасибо за ваш ответ!\n' + report_message, reply_markup=keyboards.menu_button,
                         parse_mode=types.ParseMode.HTML)

    if data['Приватность'] == 'Анонимно':
        await bot.send_message(ADMIN_ID, f'Анонимный пользователь отправил жалобу:\n{report_message}', parse_mode=types.ParseMode.HTML)
    else:
        await bot.send_message(ADMIN_ID, f'Пользователь {message.from_user.username} с ID {message.from_user.id} '
                                         f'отправил жалобу:\n{report_message}', parse_mode=types.ParseMode.HTML)

    if data['Медиа'] != 'Фото/видео не отправлено':
        MEDIA = data['Медиа'].split()
        # Здесь используется user id исключительно для отправки фотографии.
        # В дальнейшем он нигде не используется и не сохраняется.
        if MEDIA[0] == 'photo:':
            await bot.send_photo(message.from_user.id, MEDIA[1])
            await bot.send_photo(ADMIN_ID, MEDIA[1])
        elif MEDIA[0] == 'video:':
            await bot.send_video(message.from_user.id, MEDIA[1])
            await bot.send_video(ADMIN_ID, MEDIA[1])


    print(data['Категория'] + ' | ' + data['Название'] + ' | ' + data['Описание'] + ' | '
          + data['Адрес'] + ' | ' + data['Медиа'])

    await message.answer(INFO_MESSAGE2)
    await state.finish()