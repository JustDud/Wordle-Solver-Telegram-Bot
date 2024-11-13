from string import punctuation

from aiogram import types, Router, F

from filters.chat_types import ChatTypesFilter

user_group_router = Router()
user_group_router.message.filter(ChatTypesFilter(['group', 'supergroup']))


restricted_words = {'ban'}


def clean_text(text: str):
    return text.translate(str.maketrans('', '', punctuation))


@user_group_router.edited_message()
@user_group_router.message()
async def cleaner(message: types.Message):
    if restricted_words.intersection(clean_text(message.text.lower()).split()):
        await message.answer(f"{message.from_user.first_name}, follow the chat rules!")
        await message.delete()
        # await message.chat.ban(message.from_user.id)
