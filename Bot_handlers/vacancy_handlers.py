import aiomysql

from aiogram import types, Router, F
from aiogram.filters import Command, or_f, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from bot_keyboards import reply
from async_mysql import loop
from async_vacancy import insert_in_db_vacancy, start_vacancy
from config import *


class Parsing_v_states(StatesGroup):
    waiting_for_vacancy_name = State()
    showing_vacancy = State()
    waiting_for_filter = State()
    waiting_for_location_filter = State()


vacancy_router = Router()


@vacancy_router.message(StateFilter(None), or_f(Command('vacancy'), (F.text.lower() == 'вакансии')))
async def vacancy(message: types.Message, state: FSMContext):
    await state.update_data(location_filter='не имеет значения')
    await state.update_data(exp_filter='не имеет значения')
    await state.update_data(emp_mode_filter='не имеет значения')
    await start_vacancy()
    await message.answer(text='<b> Введите интересующую Вас должность с помощью клавиатуры </b>',
                         reply_markup=reply.del_kb)
    await state.set_state(Parsing_v_states.waiting_for_vacancy_name)


@vacancy_router.message(Parsing_v_states.showing_vacancy,
                        or_f(F.text.lower() == 'начать просмотр вакансий', F.text.lower() == 'следующая вакансия'))
async def vacancy_show(message: types.Message, state: FSMContext):
    data = await state.get_data()
    current_id = int(data.get('current_id', 0))
    text = data.get('v_name_text', 'none')
    location_filter = data.get('location_filter', 'не имеет значения')
    exp_filter = data.get('exp_filter', 'не имеет значения')
    emp_mode_filter = data.get('emp_mode_filter', 'не имеет значения')
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
        values = [current_id, f'%{text}%']

        if location_filter != 'не имеет значения':
            insert_query += " AND location LIKE %s"
            values.append(f'%{location_filter}%')
        if exp_filter != 'не имеет значения':
            insert_query += " AND experience LIKE %s"
            values.append(f'%{exp_filter}%')
        if emp_mode_filter != 'не имеет значения':
            insert_query += " AND employment_mode LIKE %s"
            values.append(f'%{emp_mode_filter}%')
        await cursor.execute(insert_query, values)
        row = await cursor.fetchone()
        print(f'{insert_query}, \n  {values}')
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
            print(f'id вакансии обновлено {current_id}')
            await cursor.close()
            connect.close()
        else:
            await message.answer('Подождите, идет загрузка...', reply_markup=reply.vacancy_play_kb)
    except Exception as e:
        await message.answer(f'Ошибка: {e}')
    await state.set_state(Parsing_v_states.showing_vacancy)


@vacancy_router.message(Parsing_v_states.waiting_for_vacancy_name, ~(F.text.lower() == 'начать просмотр'))
async def vacancy_parsing(message: types.Message, state: FSMContext):
    await message.answer(f"Начинаю загрузку вакансий <b>'{message.text}'</b> в базу данных...",
                         reply_markup=reply.vacancy_start_kb)
    await state.set_state(Parsing_v_states.showing_vacancy)
    await state.update_data(v_name_text=message.text)
    await insert_in_db_vacancy(message.text)


@vacancy_router.message(StateFilter('*'), or_f(Command('filters'), F.text.lower() == 'настроить фильтры'))
async def v_filter_start(message: types.Message, state: FSMContext):
    await state.set_state(Parsing_v_states.waiting_for_filter)
    await message.answer(text='Выберите от одного до трех фильтров, а затем нажмите "Применить фильтры"', reply_markup=reply.vacancy_filter_start_kb)


@vacancy_router.message(Parsing_v_states.waiting_for_filter, F.text == 'Город')
async def v_wait_filter_location(message: types.Message, state: FSMContext):
    await message.answer(text='Введите название города', reply_markup=reply.vacancy_location_filter_kb)
    await state.set_state(Parsing_v_states.waiting_for_location_filter)


@vacancy_router.message(Parsing_v_states.waiting_for_location_filter, or_f(F.text, F.text == 'Оставить поле пустым'))
async def v_get_filter_location(message: types.Message, state: FSMContext):
    await state.update_data(location_filter=message.text)
    if message.text == 'Оставить поле пустым':
        await state.update_data(location_filter='не имеет значения')
    await state.set_state(Parsing_v_states.waiting_for_filter)
    await message.answer(text='Фильтр записан. Выберите следующий или нажмите "Применить фильтр"', reply_markup=reply.vacancy_filter_start_kb)


@vacancy_router.message(Parsing_v_states.waiting_for_filter, F.text == 'Опыт работы')
async def v_wait_filter_emp_mode(message: types.Message):
    await message.answer(text='Выберите опыт работы', reply_markup=reply.vacancy_experience_filter_kb)


@vacancy_router.message(Parsing_v_states.waiting_for_filter, or_f(F.text == 'От 3 до 6 лет', F.text == 'От 1 года до 3 лет', F.text == 'Более 6 лет', F.text == 'Нет опыта', F.text == 'Очистить тип занятости'))
async def v_get_filter_location(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if message.text == 'Нет опыта':
        await state.update_data(exp_filter='не требуется')
    if message.text == 'От 3 до 6 лет':
        await state.update_data(exp_filter='3–6 лет')
    if message.text == 'От 1 года до 3 лет':
        await state.update_data(exp_filter='1–3 года')
    if message.text == 'Более 6 лет':
        await state.update_data(exp_filter='более 6 лет')
    if message.text == 'Очистить тип занятости':
        await state.update_data(exp_filter='не имеет значения')
    await message.answer(text='Фильтр записан. Выберите следующий или нажмите "Применить фильтр"', reply_markup=reply.vacancy_filter_start_kb)


@vacancy_router.message(Parsing_v_states.waiting_for_filter, F.text == 'Тип занятости')
async def v_wait_filter_emp_mode(message: types.Message):
    await message.answer(text='Выберите тип занятости', reply_markup=reply.vacancy_emp_mode_filter_kb)


@vacancy_router.message(Parsing_v_states.waiting_for_filter,
                        or_f(F.text == 'Полная занятость', F.text == 'Частичная занятость', F.text == 'Проектная работа',
                             F.text == 'Волонтерство', F.text == 'Стажировка', F.text == 'Очистить тип занятости'))
async def v_get_filter_location(message: types.Message, state: FSMContext):
    if message.text == 'Очистить тип занятости':
        await state.update_data(emp_mode_filter='не имеет значения')
    await state.update_data(emp_mode_filter=message.text)

    await message.answer(text='Фильтр записан. Выберите следующий или нажмите "Применить фильтр"',
                         reply_markup=reply.vacancy_filter_start_kb)


@vacancy_router.message(Parsing_v_states.waiting_for_filter,or_f(F.text == 'Применить фильтр', F.text == 'Очистить фильтр'))
async def v_chek_filter(message: types.Message, state: FSMContext):
    await state.set_state(Parsing_v_states.showing_vacancy)
    await state.update_data(current_id=0)
    filters = await state.get_data()
    location_f = filters.get('location_filter', 'не имеет значения')
    exp_f = filters.get('exp_filter', 'не имеет значения')
    emp_f = filters.get('emp_mode_filter', 'не имеет значения')
    if message.text == 'Применить фильтр':
        await message.answer(text=f'<b>Фильтр применен</b> \n  <b>Город:</b> {location_f} \n  <b>Опыт работы:</b> {exp_f} \n  <b>Тип занятости:</b> {emp_f}', reply_markup=reply.vacancy_start_kb)
    if message.text == 'Очистить фильтр':
        await state.update_data(location_filter='не имеет значения')
        await state.update_data(exp_filter='не имеет значения')
        await state.update_data(emp_mode_filter='не имеет значения')
        await message.answer(text='Фильтр успешно очищен', reply_markup=reply.vacancy_start_kb)


