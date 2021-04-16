from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

button_report = KeyboardButton('Создать жалобу️️')
button_privacy = KeyboardButton('Политика конфидициальности')
button_about = KeyboardButton('О проекте')
button_feedback = KeyboardButton('Обратная связь')

button_cancel = KeyboardButton('Отмена')

button_anon = KeyboardButton('Анонимно')
button_non_anon = KeyboardButton('Подписать username')

button_back = KeyboardButton('Назад')

button_location = KeyboardButton('Поделиться текущей геолокацией', request_location=True)

# Возвращение в меню и назад
system_button = ReplyKeyboardMarkup(resize_keyboard=True)
system_button.add(button_back)
system_button.add(button_cancel)

# Возвращение в меню
system_button1 = ReplyKeyboardMarkup(resize_keyboard=True)
system_button1.add(button_cancel)

# Анонимность отправки анкеты
anonymous_button = ReplyKeyboardMarkup(resize_keyboard=True)
anonymous_button.row(button_anon, button_non_anon)
anonymous_button.add(button_cancel)

# Главное меню
menu_button = ReplyKeyboardMarkup(resize_keyboard=True)
menu_button.add(button_report)
menu_button.add(button_privacy)
menu_button.add(button_about)
menu_button.add(button_feedback)

# Кнопки для подачи информации
information_button = ReplyKeyboardMarkup(resize_keyboard=True)
information_button.add(button_location)
information_button.add(button_back)
information_button.add(button_cancel)

# Пропуск пункта
button_skip = KeyboardButton("Пропустить")
skip_button = ReplyKeyboardMarkup(resize_keyboard=True)
skip_button.add(button_skip)
skip_button.add(button_back)
skip_button.add(button_cancel)

# Кнопки с категориями
category_transport = KeyboardButton('Общественный транспорт')
category_improvement = KeyboardButton('Благоустройство')
category_health = KeyboardButton('Здравоохранение')
category_JKU = KeyboardButton('Жилично-коммунальные услуги')
category_rules = KeyboardButton('Правонарушения')
category_eco = KeyboardButton('Экология')
category_road = KeyboardButton('Дорожное движение и тротуары')
category_study = KeyboardButton('Образование')
category_else = KeyboardButton('Другое')

categories_button = ReplyKeyboardMarkup(resize_keyboard=True)
categories_button.add(category_transport)
categories_button.add(category_improvement)
categories_button.add(category_health)
categories_button.add(category_eco)
categories_button.add(category_road)
categories_button.add(category_JKU)
categories_button.add(category_study)
categories_button.add(category_rules)
categories_button.add(category_else)
categories_button.add(button_cancel)