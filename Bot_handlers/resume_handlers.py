import aiomysql

from aiogram import types, Router, F
from aiogram.filters import Command, or_f, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from bot_keyboards import reply
from async_mysql import loop
from async_resume import insert_in_db_resume
from config import *


class Parsing_r_states(StatesGroup):
    waiting_for_resume_name = State()
    showing_resume = State()


resume_router = Router()


@resume_router.message(StateFilter(None), or_f(Command('resume'), (F.text.lower() == 'резюме')))
async def resume(message: types.Message, state: FSMContext):
    await message.answer("<b>Введите интересующую Вас должность с помощью клавиатуры</b>",  reply_markup=reply.del_kb)
    await state.set_state(Parsing_r_states.waiting_for_resume_name)


@resume_router.message(Parsing_r_states.showing_resume, or_f(F.text.lower() == 'начать просмотр резюме', F.text.lower() == 'следующее резюме'))
async def resume_show(message: types.Message, state: FSMContext):
    data = await state.get_data()
    current_id = int(data.get('current_id', 0))
    text = data.get('r_name_text')
    try:
        connect = await aiomysql.connect(
            host=host,
            port=3303,
            user=user,
            password=password,
            db=db_name,
            loop=loop
        )
        print("соединение с бд успешно установлено")
        cursor = await connect.cursor()
        insert_query = '''
                       SELECT * FROM resume WHERE id > %s AND name LIKE %s
                       '''
        await cursor.execute(insert_query, (current_id, f'%{text}%'))
        row = await cursor.fetchone()
        print(row)
        if row is not None:
            print(row)
            id_r = row[0]
            name = row[1]
            salary = row[2]
            specialization = row[3]
            busyness_mode = row[4]
            work_schedule = row[5]
            work_experience = row[6]
            key_skills = row[7]
            citizenship = row[8]
            location = row[9]
            job_search_status = row[10]
            resume_link = row[11]
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
            await state.update_data(current_id=id_r)
            print(f'id резюме обновлено {current_id}')
            await cursor.close()
            connect.close()
        else:
            await message.answer('Подождите, идет загрузка...', reply_markup=reply.resume_play_kb)
    except Exception as e:
        await message.answer(f'Ошибка: {e}')
    await state.set_state(Parsing_r_states.showing_resume)


@resume_router.message(Parsing_r_states.waiting_for_resume_name, ~(F.text.lower() == 'начать просмотр резюме'))
async def resume_parsing(message: types.Message, state: FSMContext):
    await message.answer(f"Начинаю загрузку резюме <b>'{message.text}'</b> в базу данных...", reply_markup=reply.resume_start_kb)
    await state.set_state(Parsing_r_states.showing_resume)
    await state.update_data(r_name_text=message.text)
    await insert_in_db_resume(message.text)
