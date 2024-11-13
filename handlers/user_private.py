from aiogram import types, Router, F
from aiogram.filters import CommandStart, Command, or_f
from filters.chat_types import ChatTypesFilter

from keyboards import reply

user_private_router = Router()
user_private_router.message.filter(ChatTypesFilter(['private']))


@user_private_router.message(CommandStart())
async def start_command(message: types.Message):
    await message.answer("Hi, I'm your virtual assistant", reply_markup=reply.start_kb)


@user_private_router.message(or_f(Command("solve"), (F.text.lower().contains("guess")), (F.text.lower().contains("solve"))))
async def menu_command(message: types.Message):
    await message.answer("For your first guess enter - CRANE", reply_markup=reply.delete_kb)


@user_private_router.message(or_f(Command("guide"), (F.text.lower().contains("instruction")), (F.text.lower().contains("how")), (F.text.lower().contains("guide"))))
async def menu_command(message: types.Message):
    await message.answer("How to use")


@user_private_router.message(or_f(Command("about"), (F.text.lower().contains("project")), (F.text.lower().contains("company")), (F.text.lower().contains("about"))))
async def menu_command(message: types.Message):
    await message.answer("This project is about")





# @user_private_router.message(F.text.lower().contains("guess"))
# async def menu_command(message: types.Message):
#     await message.answer("magic filter")
