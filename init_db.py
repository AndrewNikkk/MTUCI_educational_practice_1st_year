from pymysql import connect, Error
from config import *

try:
    with connect(
            host=host,
            user=user,
            password=password,
            port=3306
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute(f"DROP DATABASE IF EXISTS {db_name}")
            cursor.execute(f"CREATE DATABASE {db_name}")
        print("База данных создана и очищена")
except Error as e:
    print(f"Ошибка при работе с базой данных:\n{e}")


try:
    with connect(
        host=host,
        user=user,
        password=password,
        database=db_name,
    ) as connection:
        create_movies_table_query = """
        CREATE TABLE `vacancy` (
    id int NOT NULL AUTO_INCREMENT,
    name varchar(255),
    salary varchar(255),
    skills text,
    experience varchar(255),
    employment_mode varchar(255),
    description text,
    vacancy_link text,
    location varchar(100),
    employer text,
    PRIMARY KEY (`id`)
    )
        """
        with connection.cursor() as cursor:
            cursor.execute(create_movies_table_query)
        connection.commit()
except Error as e:
    print(f"Ошибка подключения к серверу:\n{e}")


try:
    with connect(
        host=host,
        user=user,
        password=password,
        database=db_name,
    ) as connection:
        create_movies_table_query = """
        CREATE TABLE `resume` (
    id int NOT NULL AUTO_INCREMENT,
    name varchar(255),
    salary varchar(55),
    specialization text,
    busyness_mode text,
    work_schedule text,
    work_experience text,
    key_skills text,
    citizenship text,
    location text,
    job_search_status text,
    resume_link text,
    PRIMARY KEY (`id`)
    )
        """
        with connection.cursor() as cursor:
            cursor.execute(create_movies_table_query)
        connection.commit()

        print("Таблица  построена")
except Error as e:
    print(f"Ошибка подключения к серверу:\n{e}")





























