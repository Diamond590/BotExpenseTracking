from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def keyboard_menu():
    kb = [
        [
            InlineKeyboardButton(text='Статистика', callback_data='statistic'),
            InlineKeyboardButton(text='Помощь', callback_data='help')
        ],
        [
            InlineKeyboardButton(text='Добавить расходы', callback_data='expense'),
            InlineKeyboardButton(text='История', callback_data='history')
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=kb)

def keyboard_category():
    kb = [
        [
            InlineKeyboardButton(text='Еда', callback_data='category_Food'),
            InlineKeyboardButton(text='Транспорт', callback_data='category_Transport')
        ],
        [
            InlineKeyboardButton(text='Развлечения', callback_data='category_Entertainment'),
            InlineKeyboardButton(text='Покупки', callback_data='category_Purchases')
        ],
        [
            InlineKeyboardButton(text='Другое', callback_data='category_Others'),
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=kb)

def keyboard_back_to_menu():
    kb = [
        [
            InlineKeyboardButton(text='Назад', callback_data='back_to_menu')
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=kb)