from aiogram import types, Router, F
from aiogram.filters import CommandStart, Command, or_f, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from filters.chat_types import ChatTypesFilter
from keyboards.reply import get_keyboard
from main import solve_wordle
from ui.text import start_text, about_text, solve_start_text
from ui.text import guide_text

# Initialise the router for private chats
user_private_router = Router()
user_private_router.message.filter(ChatTypesFilter(['private']))


START_KB = get_keyboard("Solve", "Guide", "About", placeholder='What are you interested in?', sizes=(1, 2))


# Define the states for solving Wordle using a Finite State Machine (FSM)
class SolveWordle(StatesGroup):
    first_guess = State()
    second_guess = State()
    third_guess = State()
    fourth_guess = State()
    fifth_guess = State()
    sixth_guess = State()


# Manage clue data and reset state
async def clue_data_manage(message: types.Message, state: FSMContext) -> list[str]:
    await state.update_data(clue=message.text)
    data = await state.get_data()
    clue = list(data['clue'])
    await state.set_data({})
    return clue


# Handle the /start command
@user_private_router.message(StateFilter(None), CommandStart())
async def start_command(message: types.Message, state: FSMContext):
    await message.answer(start_text, reply_markup=START_KB)


# Handle the stop command or "stop" messages
@user_private_router.message(StateFilter('*'), Command('stop'))
@user_private_router.message(StateFilter('*'), or_f(F.text.lower().contains('stop'), F.text.lower().contains('22222')))
async def stop_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await message.answer(f"Solving has been stopped!", reply_markup=START_KB)


# Handle the change word command (NOT FULLY FUNCTIONAL)
@user_private_router.message(StateFilter('*'), Command('change'))
@user_private_router.message(StateFilter('*'), or_f(F.text.lower().contains('change'), F.text.lower().contains('fix')))
async def change_word_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    guess = solve_wordle([], False, True)
    await message.answer(f"Type in the new word - '{guess.upper()}', and send me the clue back!")


# Handle the solve command
@user_private_router.message(StateFilter(None), Command("solve"))
@user_private_router.message(or_f(F.text.lower().contains("guess"), F.text.lower().contains("solve"), F.len() == 5))
async def solve_command(message: types.Message, state: FSMContext):
    await message.answer(solve_start_text, reply_markup=types.ReplyKeyboardRemove())
    solve_wordle([], True, False)
    await state.set_state(SolveWordle.first_guess)


# Handle the first guess
@user_private_router.message(SolveWordle.first_guess, F.text)
@user_private_router.message(F.len() == 5)
async def solve_first_guess(message: types.Message, state: FSMContext):
    clue = await clue_data_manage(message, state)
    guess = solve_wordle(clue, False, False)
    # print(f"G1 Guess TG and Clue: {guess, clue}")
    await message.answer(f"Type in the word - '{guess.upper()}', and send me the clue back!")
    await state.set_state(SolveWordle.second_guess)

# Handle invalid clue format for the first guess. Not added for other states
@user_private_router.message(SolveWordle.first_guess)
async def solve_first_guess(message: types.Message, state: FSMContext):
    await message.answer(f"Clue format is incorrect, try again")


# Handle subsequent guesses (second to sixth)
@user_private_router.message(SolveWordle.second_guess, F.text)
async def solve_second_guess(message: types.Message, state: FSMContext):
    clue = await clue_data_manage(message, state)
    guess = solve_wordle(clue, False, False)
    # print(f"G2 Guess TG and Clue: {guess, clue}")
    await message.answer(f"Type in the word - '{guess.upper()}', and send me the clue back!")
    await state.set_state(SolveWordle.third_guess)


@user_private_router.message(SolveWordle.third_guess, F.text)
async def solve_third_guess(message: types.Message, state: FSMContext):
    clue = await clue_data_manage(message, state)
    guess = solve_wordle(clue, False, False)
    await message.answer(f"Type in the word - '{guess.upper()}', and send me the clue back!")
    await state.set_state(SolveWordle.fourth_guess)


@user_private_router.message(SolveWordle.fourth_guess, F.text)
async def solve_fourth_guess(message: types.Message, state: FSMContext):
    clue = await clue_data_manage(message, state)
    guess = solve_wordle(clue, False, False)
    await message.answer(f"Type in the word - '{guess.upper()}', and send me the clue back!")
    await state.set_state(SolveWordle.fifth_guess)


@user_private_router.message(SolveWordle.fifth_guess, F.text)
async def solve_fifth_guess(message: types.Message, state: FSMContext):
    clue = await clue_data_manage(message, state)
    guess = solve_wordle(clue, False, False)
    await message.answer(f"Type in the word - '{guess.upper()}', and send me the clue back!")
    await state.set_state(SolveWordle.sixth_guess)


@user_private_router.message(SolveWordle.sixth_guess, F.text)
async def solve_sixth_guess(message: types.Message, state: FSMContext):
    clue = await clue_data_manage(message, state)
    guess = solve_wordle(clue, False, False)
    await message.answer(f"Type in the word - '{guess.upper()}'", reply_markup=START_KB)
    await stop_handler()


# Handle the guide command
@user_private_router.message(StateFilter(None), Command("guide"))
@user_private_router.message(or_f(F.text.lower().contains("instruction"), F.text.lower().contains("how"), F.text.lower().contains("guide")))
async def guide_command(message: types.Message, state: FSMContext):
    await message.answer(guide_text)


# Handle the about command
@user_private_router.message(StateFilter(None), or_f(Command("about"), (F.text.lower().contains("project")), (F.text.lower().contains("company")), (F.text.lower().contains("about"))))
async def about_command(message: types.Message, state: FSMContext):
    await message.answer(about_text)
