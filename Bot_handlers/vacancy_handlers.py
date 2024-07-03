import aiomysql

from aiogram import types, Router, F
from aiogram.filters import Command, or_f, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from bot_keyboards import reply
from async_mysql import loop, clear_vacancy_table
from async_vacancy import insert_in_db_vacancy
from config import *


class Parsing_v_states(StatesGroup):
    waiting_for_vacancy_name = State()
    showing_vacancy = State()


vacancy_router = Router()


@vacancy_router.message(StateFilter('*'), Command('restart'))
@vacancy_router.message(StateFilter('*'), F.text.lower() == 'вернуться к выбору')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await message.answer("<b>Выберите желаемый раздел поиска...</b>", reply_markup=reply.start_kb)


@vacancy_router.message(StateFilter(None), or_f(Command('vacancy'), (F.text.lower() == 'вакансии')))
async def vacancy(message: types.Message, state: FSMContext):
    await clear_vacancy_table()
    await message.answer(text='<b> Введите интересующую Вас должность с помощью клавиатуры </b>',
                         reply_markup=reply.del_kb)
    await state.set_state(Parsing_v_states.waiting_for_vacancy_name)


@vacancy_router.message(Parsing_v_states.showing_vacancy,
                        or_f(F.text.lower() == 'начать просмотр вакансий', F.text.lower() == 'следующая вакансия'))
async def vacancy_show(message: types.Message, state: FSMContext):
    data = await state.get_data()
    current_id = int(data.get('current_id', 0))
    text = data.get('v_name_text', 'none')
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
                       SELECT * FROM vacancy WHERE id > %s AND name LIKE %s
                       '''
        await cursor.execute(insert_query, (current_id, f'%{text}%'))
        row = await cursor.fetchone()
        if row is not None:
            print(row)
            id_v = row[0]
            name = row[1]
            salary = row[2]
            skills = row[3]
            experience = row[4]
            emp_mode = row[5]
            vacancy_link = row[7]
            location = row[8]
            employer = row[9]
            await message.answer(
                text=f'Название: <b>{name}</b> \n'
                     f'Уровень дохода: <b>{salary}</b> \n'
                     f'Требуемый опыт: <b>{experience}</b> \n'
                     f'График работы: <b>{emp_mode}</b> \n'
                     f'Местоположение: <b>{location}</b> \n'
                     f'Работодатель: <b>{employer}</b> \n'
                     f'Навыки: <b>{skills}</b> \n'
                     f'Узнать подробнее: {vacancy_link}',
                reply_markup=reply.vacancy_play_kb
            )
            await state.update_data(current_id=id_v)
            print(f'id резюме обновлено {current_id}')
        else:
            await message.answer('Подождите, идет загрузка...', reply_markup=reply.vacancy_play_kb)
    except Exception as e:
        await message.answer(f'Ошибка: {e}')
    finally:
        await cursor.close()
        connect.close()
    await state.set_state(Parsing_v_states.showing_vacancy)


@vacancy_router.message(Parsing_v_states.waiting_for_vacancy_name, ~(F.text.lower() == 'начать просмотр'))
async def vacancy_parsing(message: types.Message, state: FSMContext):
    await message.answer(f"Начинаю загрузку вакансий <b>'{message.text}'</b> в базу данных...",
                         reply_markup=reply.vacancy_start_kb)
    await state.set_state(Parsing_v_states.showing_vacancy)
    await state.update_data(v_name_text=message.text)
    await insert_in_db_vacancy(message.text)
