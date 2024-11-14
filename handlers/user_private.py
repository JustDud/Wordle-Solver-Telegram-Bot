from aiogram import types, Router, F
from aiogram.filters import CommandStart, Command, or_f, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from filters.chat_types import ChatTypesFilter
from keyboards.reply import get_keyboard
from main import guess_word_bot
from main import game_reset
from ui.text import start_text, about_text, solve_start_text
from ui.text import guide_text

global guess
guess = 'crate'

user_private_router = Router()
user_private_router.message.filter(ChatTypesFilter(['private']))


START_KB = get_keyboard("Solve", "Guide", "About",
                             placeholder='What are you interested in?',
                             sizes=(1, 2))


# FSM development
class SolveWordle(StatesGroup):
    first_guess = State()
    second_guess = State()
    third_guess = State()
    fourth_guess = State()
    fifth_guess = State()
    sixth_guess = State()

    # texts = {
    #     'SolveWordle:first_guess': "Enter the first clue again: ",
    #     'SolveWordle:second_guess': "Enter the second clue again: ",
    #     'SolveWordle:third_guess': "Enter the third clue again: ",
    #     'SolveWordle:fourth_guess': "Enter the fourth clue again: ",
    #     'SolveWordle:fifth_guess': "Enter the fifth clue again: ",
    #     'SolveWordle:sixth_guess': "Enter the sixth clue again: ",
    # }


async def clue_data_manage(message: types.Message, state: FSMContext) -> list[str]:
    await state.update_data(clue=message.text)
    data = await state.get_data()
    clue = list(data['clue'])
    await state.set_data({})
    return clue

@user_private_router.message(StateFilter(None), CommandStart())
async def start_command(message: types.Message, state: FSMContext):
    await message.answer(start_text, reply_markup=START_KB)


@user_private_router.message(StateFilter('*'), Command('stop'))
@user_private_router.message(StateFilter('*'), or_f(F.text.lower().contains('stop'), F.text.lower().contains('22222')))
async def stop_handler(message: types.Message, state: FSMContext):
    global guess
    current_state = await state.get_state()
    if current_state is None:
        return

    game_reset()
    guess = 'crate'
    await state.clear()
    await message.answer(f"Solving has been stopped!", reply_markup=START_KB)


@user_private_router.message(StateFilter(None), Command("solve"))
@user_private_router.message(or_f(F.text.lower().contains("guess"), F.text.lower().contains("solve"), F.len() == 5))
async def solve_command(message: types.Message, state: FSMContext):
    await message.answer(solve_start_text,
                         reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(SolveWordle.first_guess)


@user_private_router.message(SolveWordle.first_guess, F.text)
@user_private_router.message(F.len() == 5)
async def solve_first_guess(message: types.Message, state: FSMContext):
    global guess
    clue = await clue_data_manage(message, state)
    guess = guess_word_bot(guess, clue)
    await message.answer(f"Type in the word - '{guess.upper()}', and send me the clue back!")
    await state.set_state(SolveWordle.second_guess)


@user_private_router.message(SolveWordle.first_guess)
async def solve_first_guess(message: types.Message, state: FSMContext):
    await message.answer(f"Clue format is incorrect, try again")


@user_private_router.message(SolveWordle.second_guess, F.text)
async def solve_second_guess(message: types.Message, state: FSMContext):
    global guess
    clue = await clue_data_manage(message, state)
    guess = guess_word_bot(guess, clue)
    await message.answer(f"Type in the word - '{guess.upper()}', and send me the clue back!")
    await state.set_state(SolveWordle.third_guess)


@user_private_router.message(SolveWordle.third_guess, F.text)
async def solve_third_guess(message: types.Message, state: FSMContext):
    global guess
    clue = await clue_data_manage(message, state)
    guess = guess_word_bot(guess, clue)
    await message.answer(f"Type in the word - '{guess.upper()}', and send me the clue back!")
    await state.set_state(SolveWordle.fourth_guess)


@user_private_router.message(SolveWordle.fourth_guess, F.text)
async def solve_fourth_guess(message: types.Message, state: FSMContext):
    global guess
    clue = await clue_data_manage(message, state)
    guess = guess_word_bot(words, guess, clue)
    await message.answer(f"Type in the word - '{guess.upper()}', and send me the clue back!")
    await state.set_state(SolveWordle.fifth_guess)


@user_private_router.message(SolveWordle.fifth_guess, F.text)
async def solve_fifth_guess(message: types.Message, state: FSMContext):
    global guess
    clue = await clue_data_manage(message, state)
    guess = guess_word_bot(guess, clue)
    await message.answer(f"Type in the word - '{guess.upper()}', and send me the clue back!")
    await state.set_state(SolveWordle.sixth_guess)


@user_private_router.message(SolveWordle.sixth_guess, F.text)
async def solve_sixth_guess(message: types.Message, state: FSMContext):
    global guess
    clue = await clue_data_manage(message, state)
    guess = guess_word_bot(guess, clue)
    await message.answer(f"Type in the word - '{guess.upper()}'", reply_markup=START_KB)
    await stop_handler()


@user_private_router.message(StateFilter(None), Command("guide"))
@user_private_router.message(or_f(F.text.lower().contains("instruction"), F.text.lower().contains("how"), F.text.lower().contains("guide")))
async def guide_command(message: types.Message, state: FSMContext):
    await message.answer(guide_text)


@user_private_router.message(StateFilter(None), or_f(Command("about"), (F.text.lower().contains("project")), (F.text.lower().contains("company")), (F.text.lower().contains("about"))))
async def about_command(message: types.Message, state: FSMContext):
    await message.answer(about_text)





# @user_private_router.message(F.text.lower().contains("guess"))
# async def menu_command(message: types.Message):
#     await message.answer("magic filter")


# @user_private_router.message(StateFilter('*'), or_f(F.text.lower().contains('return'), Command('Return')))
# async def return_handler(message: types.Message, state: FSMContext) -> None:
#     current_state = await state.get_state()
#     if current_state == SolveWordle.first_guess:
#         await message.answer(f"There is no previous step. Continue or type in 'cancel'")
#         return
#
#     previous = None
#
#     for step in SolveWordle.__all_states__:
#         if step.state == current_state:
#             await state.set_state(previous)
#             await message.answer(f"You have been returned to the previous step \n {SolveWordle.}")