from aiogram import types, Router, F
from aiogram.filters import Command, or_f, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


from bot_keyboards import reply
from resume import get_resume_bot

class Parsing_r_states(StatesGroup):
    waiting_for_resume_name = State()

resume_router = Router()

@resume_router.message(StateFilter(None), or_f(Command('resume'), (F.text.lower() == 'резюме')) )
async def resume(message: types.Message, state: FSMContext):
    await message.answer("<b>Введите интересующую Вас должность с помощью клавиатуры</b>",  reply_markup=reply.del_kb)
    await state.set_state(Parsing_r_states.waiting_for_resume_name)

@resume_router.message(Parsing_r_states.waiting_for_resume_name, F.text)
async def resume_parsing(message: types.Message, state: FSMContext):
    await message.answer(f"Начинаю загрузку резюме <b>'{message.text}'</b> в базу данных...", reply_markup=reply.resume_start_kb)
    await get_resume_bot(message.text)