import asyncio

from aiogram import types, Router, F
from aiogram.filters import Command, or_f, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(max_workers=1)

from resume import connect
from bot_keyboards import reply
from resume import get_resume_bot

class Parsing_r_states(StatesGroup):
    waiting_for_resume_name = State()
    showing_resume = State()

resume_router = Router()

@resume_router.message(StateFilter(None), or_f(Command('resume'), (F.text.lower() == 'резюме')) )
async def resume(message: types.Message, state: FSMContext):
    await message.answer("<b>Введите интересующую Вас должность с помощью клавиатуры</b>",  reply_markup=reply.del_kb)
    await state.set_state(Parsing_r_states.waiting_for_resume_name)

@resume_router.message(Parsing_r_states.showing_resume, or_f(F.text.lower() == 'начать просмотр резюме', F.text.lower() == 'следующее резюме'))
async def resume_show(message: types.Message, state: FSMContext):
    try:
        current_id = await state.get_data()
        current_id = current_id.get('current_id', 1)

        data = await state.get_data()
        text = data.get('r_message_text', '')
        print(text)

        with (connect.cursor() as cursor):
            query = 'SELECT * FROM resume WHERE id = %s AND name LIKE %s'
            cursor.execute(query, (current_id, f"%{text}%"))
            row = cursor.fetchone()
            if row is not None:
                print(row)
                name = row["name"]
                salary = row["salary"]
                specialization = row["specialization"]
                busyness_mode = row["busyness_mode"]
                work_schedule = row["work_schedule"]
                work_experience = row["work_experience"]
                key_skills = row["key_skills"]
                citizenship = row["citizenship"]
                location = row["location"]
                job_search_status = row["job_search_status"]
                resume_link = row["resume_link"]
                await message.answer(
                    text=f'Название: <b>{name}</b> \n'
                         f'Уровень дохода: <b>{salary}</b> \n'
                         f'Статус: <b>{job_search_status}</b> \n'
                         f'График работы: <b>{work_schedule}</b> \n'
                         f'Тип занятости: <b>{busyness_mode}</b> \n'
                         f'Местоположение: <b>{location}</b> \n'
                         f'Специализация: <b>{specialization}</b> \n'
                         f'Навыки: <b>{key_skills}</b> \n'
                         f'Гражданство: <b>{citizenship}</b> \n'
                         f'Опыт работы:<b>{work_experience}</b> \n'
                         f'Подробнее:{resume_link}',
                    reply_markup=reply.resume_play_kb
                )
                await state.update_data(current_id=current_id + 1)
            else:
                await message.answer('Резюме закончились.')
    except Exception as e:
        await message.answer(f'Ошибка: {e}')
    await state.set_state(Parsing_r_states.showing_resume)
@resume_router.message(Parsing_r_states.waiting_for_resume_name, ~(F.text.lower() == 'начать просмотр резюме'))
async def resume_parsing(message: types.Message, state: FSMContext):
    await message.answer(f"Начинаю загрузку резюме <b>'{message.text}'</b> в базу данных...", reply_markup=reply.resume_start_kb)
    await state.update_data(r_message_text=message.text)
    await state.set_state(Parsing_r_states.showing_resume)
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, get_resume_bot, message.text)