import aiomysql

from aiogram import types, Router, F
from aiogram.filters import Command, or_f, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from bot_keyboards import reply
from async_mysql import loop
from async_resume import insert_in_db_resume, start_resume, stop_resume
from config import *


class Parsing_r_states(StatesGroup):
    waiting_for_resume_name = State()
    waiting_for_location_name = State()
    showing_resume = State()
    waiting_for_filter = State()
    waiting_for_location_filter = State()


resume_router = Router()


@resume_router.message(StateFilter(None), F.text.lower() == 'резюме')
async def resume(message: types.Message, state: FSMContext):
    await state.update_data(location_filter='не имеет значения')
    await state.update_data(status_filter='не имеет значения')
    await state.update_data(schedule_filter='не имеет значения')
    await start_resume()
    await message.answer(text='<b> Введите название города (необязательно) </b>',
                         reply_markup=reply.resume_location_filter_kb)
    await state.set_state(Parsing_r_states.waiting_for_location_name)


@resume_router.message(Parsing_r_states.waiting_for_location_name, F.text)
async def resume_parsing(message: types.Message, state: FSMContext):
    await message.answer(f"<b>Введите интересующую Вас должность с помощью клавиатуры</b>",
                         reply_markup=reply.del_kb)
    await state.set_state(Parsing_r_states.showing_resume)
    await state.update_data(location_filter=message.text)
    if message.text == 'Оставить поле пустым':
        await state.update_data(location_filter='не имеет значения')
    await state.set_state(Parsing_r_states.waiting_for_resume_name)


@resume_router.message(Parsing_r_states.showing_resume, or_f(F.text.lower() == 'начать просмотр резюме', F.text.lower() == 'следующее резюме'))
async def resume_show(message: types.Message, state: FSMContext):
    data = await state.get_data()
    current_id = int(data.get('current_id', 0))
    text = data.get('r_name_text')
    location_filter = data.get('location_filter', 'не имеет значения')
    status_filter = data.get('status_filter', 'не имеет значения')
    schedule_filter = data.get('schedule_filter', 'не имеет значения')
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
                               SELECT * FROM resume WHERE id > %s AND (name LIKE %s OR specialization LIKE %s)
                               '''
        values = [current_id, f'%{text}%', f'%{text}%']

        if location_filter != 'не имеет значения':
            insert_query += " AND location LIKE %s"
            values.append(f'%{location_filter}%')
        if status_filter != 'не имеет значения':
            insert_query += " AND job_search_status LIKE %s"
            values.append(f'%{status_filter}%')
        if schedule_filter != 'не имеет значения':
            insert_query += " AND work_schedule LIKE %s"
            values.append(f'%{schedule_filter}%')
        await cursor.execute(insert_query, values)
        row = await cursor.fetchone()
        print(f'{insert_query}, \n  {values}')
        if row is not None:
            try:
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
            except Exception as e:
                print(e)
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


@resume_router.message(Parsing_r_states.waiting_for_resume_name, F.text)
async def resume_parsing(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await message.answer(f"Начинаю загрузку резюме <b>'{message.text}'</b> в базу данных...",
                         reply_markup=reply.resume_start_kb)
    await state.set_state(Parsing_r_states.showing_resume)
    await state.update_data(r_name_text=message.text)
    if data['location_filter'] == 'не имеет значения':
        print("без локации", data['location_filter'])
        await insert_in_db_resume(message.text)
    else:
        print('с локацией', data['location_filter'])
        await insert_in_db_resume(message.text, data['location_filter'])


@resume_router.message(Parsing_r_states.showing_resume, F.text.lower() == 'настроить фильтры')
async def r_filter_start(message: types.Message, state: FSMContext):
    await stop_resume()
    await state.set_state(Parsing_r_states.waiting_for_filter)
    await message.answer(text='Выберите от одного до трех фильтров, а затем нажмите "Применить фильтры"', reply_markup=reply.resume_filter_start_kb)


@resume_router.message(Parsing_r_states.waiting_for_filter, F.text == 'Город')
async def r_wait_location_filter(message: types.Message, state: FSMContext):
    await state.set_state(Parsing_r_states.waiting_for_location_filter)
    await message.answer(text='Введите название города', reply_markup=reply.resume_location_filter_kb)


@resume_router.message(Parsing_r_states.waiting_for_location_filter, or_f(F.text, F.text == 'Оставить поле пустым'))
async def r_get_filter_location(message: types.Message, state: FSMContext):
    await state.update_data(location_filter=message.text)
    if message.text == 'Оставить поле пустым':
        await state.update_data(location_filter='не имеет значения')
    await state.set_state(Parsing_r_states.waiting_for_filter)
    await message.answer(text='Фильтр записан. Выберите следующий или нажмите "Применить фильтр"', reply_markup=reply.resume_filter_start_kb)


@resume_router.message(Parsing_r_states.waiting_for_filter, F.text == 'Статус')
async def r_wait_status_filter(message: types.Message):
    await message.answer(text='Выберите статус', reply_markup=reply.resume_status_filter_kb)


@resume_router.message(Parsing_r_states.waiting_for_filter, or_f(F.text == 'Не ищет работу', F.text == 'Рассматривает предложения', F.text == 'Активно ищет работу', F.text == 'Предложили работу', F.text == 'Вышел на новое место', F.text == 'Без статуса поиска', F.text == 'Очистить статус поиска'))
async def r_get_status_filter(message: types.Message, state: FSMContext):
    if message.text == 'Очистить статус поиска':
        await state.update_data(status_filter='не имеет значения')
    elif message.text == 'Без статуса поиска':
        await state.update_data(status_filter='не указан')
    else:
        await state.update_data(status_filter=message.text)
    await message.answer(text='Фильтр записан. Выберите следующий или нажмите "Применить фильтр"', reply_markup=reply.resume_filter_start_kb)


@resume_router.message(Parsing_r_states.waiting_for_filter, F.text == 'График работы')
async def r_wait_status_filter(message: types.Message):
    await message.answer(text='Выберите график работы', reply_markup=reply.resume_work_schedule_filter_kb)


@resume_router.message(Parsing_r_states.waiting_for_filter,
                        or_f(F.text.lower() == 'полный день', F.text.lower() == 'удаленная работа', F.text.lower() == 'гибкий график',
                             F.text.lower() == 'сменный график', F.text.lower() == 'вахтовый метод', F.text == 'Очистить график работы'))
async def v_get_filter_work_schedule(message: types.Message, state: FSMContext):
    if message.text == 'Очистить график работы':
        await state.update_data(schedule_filter='не имеет значения')
    else:
        await state.update_data(schedule_filter=message.text.lower())
    await message.answer(text='Фильтр записан. Выберите следующий или нажмите "Применить фильтр"',
                         reply_markup=reply.resume_filter_start_kb)


@resume_router.message(Parsing_r_states.waiting_for_filter, or_f(F.text == 'Применить фильтр', F.text == 'Очистить фильтр'))
async def r_chek_filter(message: types.Message, state: FSMContext):
    await start_resume()
    await state.set_state(Parsing_r_states.showing_resume)
    await state.update_data(current_id=0)
    data = await state.get_data()
    location_f = data.get('location_filter', 'не имеет значения')
    status_f = data.get('status_filter', 'не имеет значения')
    schedule_f = data.get('schedule_filter', 'не имеет значения')
    if message.text == 'Применить фильтр':
        await message.answer(text=f'<b>Фильтр применен</b> \n  <b>Город:</b> {location_f} \n  <b>Статус поиска:</b> {status_f.lower()} \n  <b>График работы:</b> {schedule_f}', reply_markup=reply.resume_continue_kb)
        if data['location_filter'] == 'не имеет значения':
            print("без локации", data['location_filter'])
            await insert_in_db_resume(message.text)
        else:
            print('с локацией', data['location_filter'])
            await insert_in_db_resume(data['r_name_text'], data['location_filter'])
    if message.text == 'Очистить фильтр':
        await state.update_data(location_filter='не имеет значения')
        await state.update_data(status_filter='не имеет значения')
        await state.update_data(schedule_filter='не имеет значения')
        await message.answer(text='Фильтр успешно очищен', reply_markup=reply.resume_continue_kb)
        if data['location_filter'] == 'не имеет значения':
            print("без локации", data['location_filter'])
            await insert_in_db_resume(message.text)
        else:
            print('с локацией', data['location_filter'])
            await insert_in_db_resume(data['r_name_text'], data['location_filter'])







