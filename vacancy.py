import requests
from bs4 import BeautifulSoup
import time
import pymysql
from config import host, user, password, db_name



is_running = True

def get_links(text):
    # ua = fake_useragent.UserAgent()
    data = requests.get(
        url=f"https://hh.ru/search/vacancy?text={text}&from=suggest_post&region=113&page=0",
        headers={"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 YaBrowser/24.6.0.0 Safari/537.36"}
    )
    if data.status_code != 200:
        return
    soup = BeautifulSoup(data.content, "lxml")
    try:
        page_count = int(soup.find("div", attrs={"class":"pager"}).find_all("span", recursive=False)[-1].find("a").find("span").text)
    except:
        return

    for page in range(page_count):
        try:
            data = requests.get(
                url=f"https://hh.ru/search/vacancy?text={text}&page={page}",
                headers={"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 YaBrowser/24.6.0.0 Safari/537.36"}
            )
            if data.status_code != 200:
                continue
            soup = BeautifulSoup(data.content, "lxml")
            for a in soup.find_all("span", attrs={"class":"serp-item__title-link-wrapper"}):
                for b in a.find_all("a", attrs={"class": "bloko-link"}):
                    yield f"{b.attrs['href'].split('?')[0]}"
        except Exception as e:
            print(f"{e}")
        time.sleep(1)





def get_vacancy(link):
    data = requests.get(
        url=link,
        headers={"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 YaBrowser/24.6.0.0 Safari/537.36"}
    )
    if data.status_code != 200:
        return
    soup = BeautifulSoup(data.content,"lxml")
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
    return vacancy


def insert_in_db(vacancy, connect):
    if vacancy == None:
        pass
    else:
        try:
            name = vacancy.get("name", 'не указано')
            salary = vacancy.get("salary", '')
            skills = ', '.join(vacancy.get("skills", ["пусто"]))
            experience = vacancy.get("experience", 'не указан')
            employment_mode = ', '.join(vacancy.get("employment_mode", ["пусто"]))
            description = vacancy.get("description", 'не указан')
            vacancy_link = vacancy.get("vacancy_link", 'none')
            location = vacancy.get("location","none")
            employer = vacancy.get("employer", "none")
        except Exception as e:
            print(f"Произошла ошибка при извлечении данных: {e}")
            return

        try:
            with connect.cursor() as cursor:
                insert_query = """
                INSERT INTO data (name, salary, skills, experience, employment_mode, description, vacancy_link, location, employer)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
                """
                cursor.execute(insert_query, (name, salary, skills, experience, employment_mode, description, vacancy_link, location, employer))
                connect.commit()
        except Exception as e:
            print(f"Произошла ошибка: {e}")

try:
    connect = pymysql.connect(
        host=host,
        port=3303,
        user=user,
        password=password,
        database=db_name,
        cursorclass=pymysql.cursors.DictCursor
    )
    print("Successfully connected")
except Exception as ex:
    print("Connection refused")
    print(ex)

def get_vacancy_bot(text):
    global is_running
    while is_running:
        try:
            with connect.cursor() as cursor:
                insert_query = "TRUNCATE TABLE data;"
                cursor.execute(insert_query)
                connect.commit()
        except Exception as e:
            print(f"Не удалось очистить таблицу: {e}")

        try:
            for a in get_links(f"{text}"):
                insert_in_db(get_vacancy(a), connect)
                time.sleep(1)
        except Exception as e:
            print(f"Ошибка при вставке данных: {e}")
            if not is_running:
                connect.close()
                break


async def cancel_get_vacancy_bot():
    global is_running
    is_running = False





