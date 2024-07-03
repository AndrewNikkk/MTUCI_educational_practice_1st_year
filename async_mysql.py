import aiomysql
import asyncio

from config import *

loop = asyncio.get_event_loop()

async def clear_vacancy_table():
    connect = await aiomysql.connect(
        host=host,
        port=3303,
        user=user,
        password=password,
        db=db_name,
        loop=loop
    )
    cursor = await connect.cursor()
    await cursor.execute(
        '''
        TRUNCATE TABLE vacancy;
        '''
    )
    print('Таблица vacancy успешно очищена')
    await cursor.close()
    connect.close()


async def clear_resume_table():
    connect = await aiomysql.connect(
        host=host,
        port=3303,
        user=user,
        password=password,
        db=db_name,
        loop=loop
    )
    cursor = await connect.cursor()
    await cursor.execute(
        '''
        TRUNCATE TABLE resume;
        '''
    )
    print('Таблица resume успешно очищена')
    await cursor.close()
    connect.close()


async def filling_vacancy_table(
        name,
        salary,
        skills,
        experience,
        employment_mode,
        description,
        vacancy_link,
        location,
        employer
):
    connect = await aiomysql.connect(
        host=host,
        port=3303,
        user=user,
        password=password,
        db=db_name,
        loop=loop
    )
    cursor = await connect.cursor()
    insert_query = '''
        INSERT INTO vacancy (name, salary, skills, experience, employment_mode, description, vacancy_link, location, employer)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
        '''
    await cursor.execute(
        insert_query,
        (
            name,
            salary,
            skills,
            experience,
            employment_mode,
            description,
            vacancy_link,
            location,
            employer
        ))
    await connect.commit()
    print('Данные о вакансии успешно внесены в таблицу vacancy')
    await cursor.close()
    connect.close()


async def filling_resume_table(
        name,
        salary,
        specialization,
        busyness_mode,
        work_schedule,
        work_experience,
        key_skills,
        citizenship,
        location,
        job_search_status,
        resume_link
):
    connect = await aiomysql.connect(
        host=host,
        port=3303,
        user=user,
        password=password,
        db=db_name,
        loop=loop
    )
    cursor = await connect.cursor()
    insert_query = '''
        INSERT INTO resume (name, salary, specialization, busyness_mode, work_schedule, work_experience, key_skills, citizenship, location, job_search_status, resume_link)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        '''
    await cursor.execute(
        insert_query,
        (
            name,
            salary,
            specialization,
            busyness_mode,
            work_schedule,
            work_experience,
            key_skills,
            citizenship,
            location,
            job_search_status,
            resume_link
        ))
    await connect.commit()
    print('Данные о резюме успешно внесены в таблицу resume')
    await cursor.close()
    connect.close()


# if __name__ == '__main__':
#     asyncio.run(async for row in send_vacancy_to_bot('Python'):
#         print(row))
