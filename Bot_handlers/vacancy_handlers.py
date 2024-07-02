import asyncio

from aiogram import types, Router, F
from aiogram.filters import Command, or_f, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(max_workers=1)

from bot_keyboards import reply
from vacancy import get_vacancy_bot, cancel_get_vacancy_bot, is_running
from vacancy import connect

class CurrentID:
    id = 1

class Parsing_v_states(StatesGroup):
    waiting_for_vacancy_name = State()
    showing_vacancy = State()

vacancy_router = Router()


@vacancy_router.message(StateFilter(None), or_f(Command('vacancy'), (F.text.lower() == 'вакансии')))
async def vacancy(message: types.Message, state: FSMContext):
    await message.answer(text='<b> Введите интересующую Вас должность с помощью клавиатуры </b>', reply_markup=reply.del_kb)
    await state.set_state(Parsing_v_states.waiting_for_vacancy_name)

@vacancy_router.message(Parsing_v_states.showing_vacancy, or_f(F.text.lower() == 'начать просмотр', F.text.lower() == 'следующая вакансия'))
async def vacancy_show(message: types.Message, state: FSMContext):
    try:
        with connect.cursor() as cursor:
            cursor.execute(f'SELECT * FROM data WHERE id = {CurrentID.id}')
            row = cursor.fetchone()
            while row is not None:
                await message.answer(text=f'{row}', reply_markup=reply.vacancy_play_kb)
                CurrentID.id += 1
                break
    except Exception as e:
        await message.answer(f'Ошибка: {e}')
    await state.set_state(Parsing_v_states.showing_vacancy)

@vacancy_router.message(Parsing_v_states.waiting_for_vacancy_name, ~(F.text.lower() == 'начать просмотр'))
async def vacancy_parsing(message: types.Message, state: FSMContext):
    await message.answer(f"Начинаю загрузку вакансий <b>'{message.text}'</b> в базу данных...", reply_markup=reply.vacancy_start_kb)
    await state.set_state(Parsing_v_states.showing_vacancy)
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(executor, get_vacancy_bot(message.text))










