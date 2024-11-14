from aiogram import types, Router, F
from aiogram.filters import CommandStart, Command, or_f, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from filters.chat_types import ChatTypesFilter
from keyboards.reply import get_keyboard
from main import guess_word_bot
from main import words

global guess
global stop

guess = 'crate'
stop = False

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


# async def get_clue(message: types.Message, state: FSMContext):
#     await state.update_data(clue=message.text)
#     data = await state.get_data()
#     clue = list(data['clue'])
#     await print(clue)
#     await state.clear()
#     return clue

@user_private_router.message(StateFilter(None), CommandStart())
async def start_command(message: types.Message, state: FSMContext):
    await message.answer("Hi, I'm your virtual assistant", reply_markup=START_KB)


@user_private_router.message(StateFilter(None), or_f(Command("solve"), (F.text.lower().contains("guess")), (F.text.lower().contains("solve"))))
async def solve_command(message: types.Message, state: FSMContext):
    await message.answer("Rules: enter the clue from Wordle in the form such that:"
                         "Grey -> 0, Yellow -> 1, Green -> 2"
                         "\nIf the word has been guessed, send 'STOP' "
                         "\n\nFor your first guess type in 'CRATE', and send me the clue back!",
                         reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(SolveWordle.first_guess)


@user_private_router.message(StateFilter(SolveWordle.first_guess), F.text.lower() != 'stop')
async def solve_first_guess(message: types.Message, state: FSMContext):
    global guess
    global stop
    await state.clear()
    await state.update_data(clue=message.text)
    data = await state.get_data()
    clue = list(data['clue'])
    guess = guess_word_bot(stop, words, guess, clue)
    await message.answer(f"Type in the word - '{guess}', and send me the clue back!")
    await state.set_state(SolveWordle.second_guess)


@user_private_router.message(StateFilter(SolveWordle.second_guess), F.text.lower() != 'stop')
async def solve_second_guess(message: types.Message, state: FSMContext):
    global guess
    global stop
    await state.clear()
    await state.update_data(clue=message.text)
    data = await state.get_data()
    clue = list(data['clue'])
    guess = guess_word_bot(stop, words, guess, clue)
    await message.answer(f"Type in the word - '{guess}', and send me the clue back!")
    await state.set_state(SolveWordle.third_guess)


@user_private_router.message(StateFilter(SolveWordle.third_guess), F.text.lower() != 'stop')
async def solve_third_guess(message: types.Message, state: FSMContext):
    global guess
    global stop
    await state.clear()
    await state.update_data(clue=message.text)
    data = await state.get_data()
    clue = list(data['clue'])
    guess = guess_word_bot(stop, words, guess, clue)
    await message.answer(f"Type in the word - '{guess}', and send me the clue back!")
    await state.set_state(SolveWordle.fourth_guess)


@user_private_router.message(StateFilter(SolveWordle.fourth_guess), F.text.lower() != 'stop')
async def solve_fourth_guess(message: types.Message, state: FSMContext):
    global guess
    global stop
    await state.clear()
    await state.update_data(clue=message.text)
    data = await state.get_data()
    clue = list(data['clue'])
    guess = guess_word_bot(stop, words, guess, clue)
    await message.answer(f"Type in the word - '{guess}', and send me the clue back!")
    await state.set_state(SolveWordle.fifth_guess)


@user_private_router.message(StateFilter(SolveWordle.fifth_guess), F.text.lower() != 'stop')
async def solve_fifth_guess(message: types.Message, state: FSMContext):
    global guess
    global stop
    await state.clear()
    await state.update_data(clue=message.text)
    data = await state.get_data()
    clue = list(data['clue'])
    guess = guess_word_bot(stop, words, guess, clue)
    await message.answer(f"Type in the word - '{guess}', and send me the clue back!")
    await state.set_state(SolveWordle.sixth_guess)


@user_private_router.message(StateFilter(SolveWordle.sixth_guess), F.text.lower() != 'stop')
async def solve_sixth_guess(message: types.Message, state: FSMContext):
    global guess
    global stop
    await state.clear()
    await state.update_data(clue=message.text)
    data = await state.get_data()
    clue = list(data['clue'])
    guess = guess_word_bot(stop, words, guess, clue)
    await message.answer(f"Type in the word - '{guess}'", reply_markup=START_KB)
    await state.set_state(None)


@user_private_router.message(F.text.lower().contains('stop'))
async def solve_stop(message: types.Message, state: FSMContext):
    await message.answer(f"Solving has been stopped!", reply_markup=START_KB)
    await state.set_state(None)


@user_private_router.message(StateFilter(None), or_f(Command("guide"), (F.text.lower().contains("instruction")), (F.text.lower().contains("how")), (F.text.lower().contains("guide"))))
async def guide_command(message: types.Message, state: FSMContext):
    await message.answer("How to use")


@user_private_router.message(StateFilter(None), or_f(Command("about"), (F.text.lower().contains("project")), (F.text.lower().contains("company")), (F.text.lower().contains("about"))))
async def about_command(message: types.Message, state: FSMContext):
    await message.answer("This project is about")





# @user_private_router.message(F.text.lower().contains("guess"))
# async def menu_command(message: types.Message):
#     await message.answer("magic filter")
