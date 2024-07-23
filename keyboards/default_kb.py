from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Загрузить файл'),
            KeyboardButton(text='Добавить запрещёнку'),
        ],
        [
            KeyboardButton(text='Список запрещённых товаров')
        ]
    ],
    resize_keyboard=True, one_time_keyboard=True)

# Реализована клавиатура команды отмена
cancel_markup = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text='Отмена'),

    ],
],
    resize_keyboard=True, one_time_keyboard=True)
