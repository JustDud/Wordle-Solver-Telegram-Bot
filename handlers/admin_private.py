from aiogram import F, Router, types
from aiogram.filters import Command

from filters.chat_types import ChatTypesFilter, IsAdmin
from keyboards.reply import get_keyboard

admin_router = Router()
admin_router.message.filter(ChatTypesFilter(['private']), IsAdmin())

ADMIN_KB = get_keyboard("Statistics", "AdminBTN2", placeholder='Choose an action', sizes=(2, ))


@admin_router.message(Command("admin"))
async def admin_start(message:types.Message):
    await message.answer(f"Welcome What would you like to do?",
                         reply_markup=ADMIN_KB)
# , {message.from_user.first_name}!


@admin_router.message(F.text == 'Statistics')
async def show_stats(message:types.Message):
    await message.answer("Stats:")
