import time
import aiohttp
import asyncio
import aiomysql
from bs4 import BeautifulSoup

from async_mysql import filling_vacancy_table, loop
from config import *

flag_v = True


async def get_links(text):
    async with aiohttp.ClientSession() as session:
        data = await session.get(
            url=f"https://hh.ru/search/vacancy?text={text}&from=suggest_post&region=113&page=0",
            headers={"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 YaBrowser/24.6.0.0 Safari/537.36"}
        )
        if data.status != 200:
            return
        soup = BeautifulSoup(await data.text(), "lxml")
        try:
            page_count = int(soup.find("div", attrs={"class":"pager"}).find_all("span", recursive=False)[-1].find("a").find("span").text)
        except:
            return

        for page in range(page_count):
            try:
                data = await session.get(
                    url=f"https://hh.ru/search/vacancy?text={text}&page={page}",
                    headers={"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 YaBrowser/24.6.0.0 Safari/537.36"}
                )
                if data.status!= 200:
                    continue
                soup = BeautifulSoup(await data.text(), "lxml")
                for a in soup.find_all("span", attrs={"class":"serp-item__title-link-wrapper"}):
                    for b in a.find_all("a", attrs={"class": "bloko-link"}):
                        yield f"{b.attrs['href'].split('?')[0]}"
            except Exception as e:
                print(f"{e}")
            await asyncio.sleep(1)


async def get_vacancy(link):
    connect = await aiomysql.connect(
        host=host,
        port=3303,
        user=user,
        password=password,
        db=db_name,
        loop=loop
    )
    cursor = await connect.cursor()
    insert_query = '''SELECT COUNT(*) FROM vacancy WHERE vacancy_link = %s;'''
    await cursor.execute(insert_query, (link,))
    print('Проверяем наличие ссылки в бд')
    link_exists = await cursor.fetchone()
    if link_exists[0] == 0:
        print('Ссылка на вакансию не найдена, начинаем загрузку в базу')
        await cursor.close()
        connect.close()
        async with aiohttp.ClientSession() as session:
            data = await session.get(
                url=link,
                headers={"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 YaBrowser/24.6.0.0 Safari/537.36"}
            )
            if data.status != 200:
                return
            soup = BeautifulSoup(await data.text(),"lxml")
            try:
                name = soup.find("h1", attrs={"class":"bloko-header-section-1"}).text
            except:
                try:
                    name = soup.find(attrs={"class":"W_DJwxf___vacancy-title"}).text
                except:
                    name = "не указано"
            try:
                salary = soup.find("div", attrs={"data-qa":"vacancy-salary"}).text.replace('\xa0', " ")
            except:
                salary = "уровень дохода не указан"
            try:
                skills = [skill.text for skill in soup.find("ul", attrs={"class":"vacancy-skill-list--COfJZoDl6Y8AwbMFAh5Z"}).find_all(attrs={"class":"magritte-tag__label___YHV-o_3-0-0"})]
            except:
                skills = ["не указаны"]
            try:
                experience = soup.find(attrs={"data-qa":"vacancy-experience"}).text
            except:
                experience = "не указан"
            try:
               employment_mode = [mode.text for mode in soup.find_all(attrs={"data-qa": "vacancy-view-employment-mode"})]
            except:
                employment_mode = ["не указан"]
            try:
                description = soup.find(attrs={"data-qa":"vacancy-description"}).text
            except:
                description = "отсутствует"
            try:
                location = soup.find(attrs={"data-qa":"vacancy-view-link-location-text"}).text
            except:
                try:
                    location = soup.find(attrs={"data-qa":"vacancy-view-location"}).text
                except:
                    location = 'не указано'
            try:
                employer = soup.find(attrs={"data-qa":"vacancy-company__details"}).text
            except:
                employer = "неизвестен"

            vacancy_link = f"{link.replace('tver.', '')}"

            vacancy = {
                "name":name,
                "salary":salary,
                "skills":skills,
                "experience":experience,
                "employment_mode":employment_mode,
                "description":description,
                "vacancy_link":vacancy_link,
                "location":location,
                "employer":employer
            }
            time.sleep(1)
            return vacancy
    else:
        print('Ссылка уже есть в базе')
        await cursor.close()
        connect.close()
        return



async def insert_in_db_vacancy(text):
    if flag_v:
        async for a in get_links(f'{text}'):
            if flag_v:
                vacancy = await get_vacancy(a)
            else:
                print('Выполнение функции insert_vacancy остановлено  flag = 0')
                return
            if vacancy:
                try:
                    name = vacancy.get("name", 'не указано')
                    salary = vacancy.get("salary", '')
                    skills = ', '.join(vacancy.get("skills", ["пусто"]))
                    experience = vacancy.get("experience", 'не указан')
                    employment_mode = ', '.join(vacancy.get("employment_mode", ["пусто"]))
                    description = vacancy.get("description", 'не указан')
                    vacancy_link = vacancy.get("vacancy_link", 'none')
                    location = vacancy.get("location", "none")
                    employer = vacancy.get("employer", "none")
                except Exception as e:
                    print(f"Произошла ошибка при извлечении данных: {e}")
                    return
                try:
                    await filling_vacancy_table(
                        name,
                        salary,
                        skills,
                        experience,
                        employment_mode,
                        description,
                        vacancy_link,
                        location,
                        employer
                    )
                except Exception as e:
                    print(f'что-то пошло не так: {e}')
    else:
        print('Выполнение функции insert_vacancy остановлено  flag = 0')
        return


async def stop_vacancy():
    global flag_v
    flag_v = False
    return


async def start_vacancy():
    global flag_v
    flag_v = True
    print('flag_v=1')
    return



if __name__ == '__main__':
    asyncio.run(insert_in_db_vacancy('python'))