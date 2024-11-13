from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Solve'),
        ],
        [
            KeyboardButton(text='Guide'),
            KeyboardButton(text='About'),
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder="What are you interested in?"
)

delete_kb = ReplyKeyboardRemove()
