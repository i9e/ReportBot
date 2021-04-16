from aiogram import types
from misc import dp
from styles import keyboards
from aiogram.dispatcher import filters

from config import PRIVACY, COMMAND_LIST, ABOUT_MESSAGE, HELP_MESSAGE

# Главное меню
@dp.message_handler(filters.Text(equals = "Отмена"))
@dp.message_handler(commands=['start'])
async def cmd_start(message = types.Message):
    await message.answer('Здравствуйте! Для подачи жалобы нажмите кнопку в меню\n\nПеред началом работы '
                         'рекомендуем ознакомиться с /help, /privacy, /about', reply_markup = keyboards.menu_button)

# Помощь: Выводит словарь COMMAND_LIST
@dp.message_handler(commands=['help'])
async def cmd_start(message = types.Message):
    command_list_message = ''
    for command_name in COMMAND_LIST:
        command_list_message += command_name + ' — ' + COMMAND_LIST[command_name] + '\n'
    await message.answer(HELP_MESSAGE + '\n\n' + command_list_message, reply_markup=keyboards.menu_button)

# Политика конфидициальности
@dp.message_handler(filters.Text(equals = "Политика конфидициальности"))
@dp.message_handler(commands=['privacy'])
async def cmd_privacy(message = types.Message):
    await message.answer(PRIVACY, parse_mode=types.ParseMode.HTML, reply_markup=keyboards.menu_button)

# О проекте
@dp.message_handler(filters.Text(equals = "О проекте"))
@dp.message_handler(commands=['about'])
async def cmd_about(message = types.Message):
    await message.answer(ABOUT_MESSAGE, parse_mode=types.ParseMode.HTML, reply_markup=keyboards.menu_button)