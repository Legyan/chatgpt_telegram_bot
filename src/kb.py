from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardMarkup)

menu = [
    [
        InlineKeyboardButton(
            text='📝 Генерировать текст', callback_data='generate_text'
        ),
        InlineKeyboardButton(
            text='🖼 Генерировать изображение', callback_data='generate_image'
        )
    ],
    [
        InlineKeyboardButton(
            text='💸 Потрачено токенов', callback_data='my_tokens'
        ),
        InlineKeyboardButton(
            text='🔎 Помощь', callback_data='help'
        )
    ]
]
menu = InlineKeyboardMarkup(
    inline_keyboard=menu
)
exit_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='Меню')]], resize_keyboard=True
)
iexit_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Меню', callback_data='menu')]
    ]
)
