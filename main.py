import requests
from bs4 import BeautifulSoup
# import fake_useragent
import time
import json
import pymysql
from config import host, user, password, db_name


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
                url=f"https://hh.ru/search/vacancy?text={text}&from=suggest_post&page={page}",
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
        name = ""
    try:
        salary = soup.find("div", attrs={"data-qa":"vacancy-salary"}).text.replace('\xa0', " ")
    except:
        salary = ""
    try:
        skills = [skill.text for skill in soup.find("ul", attrs={"class":"vacancy-skill-list--COfJZoDl6Y8AwbMFAh5Z"}).find_all(attrs={"class":"magritte-tag__label___YHV-o_3-0-0"})]
    except:
        skills = []
    try:
        experience = soup.find(attrs={"data-qa":"vacancy-experience"}).text
    except:
        experience = ""
    try:
       employment_mode = [mode.text for mode in soup.find_all(attrs={"data-qa": "vacancy-view-employment-mode"})]
    except:
        employment_mode = []
    try:
        description = soup.find(attrs={"data-qa":"vacancy-description"}).text
    except:
        description = ""

    vacancy_link = f"{link}"



    vacancy = {
        "name":name,
        "salary":salary,
        "skills":skills,
        "experience":experience,
        "employment_mode":employment_mode,
        "description":description,
        "vacancy_link":vacancy_link
    }
    return vacancy


def insert_in_db(vacancy, connect):
    try:
        name = vacancy.get("name", 'не указано')
        salary = vacancy.get("salary", '')
        skills = ', '.join(vacancy.get("skills", ["пусто"]))
        experience = vacancy.get("experience", 'не указан')
        employment_mode = ', '.join(vacancy.get("employment_mode", ["пусто"]))
        description = vacancy.get("description", 'не указан')
        vacancy_link = vacancy.get("vacancy_link", 'none')
    except Exception as e:
        print(f"Произошла ошибка при извлечении данных: {e}")
        return

    try:
        with connect.cursor() as cursor:
            insert_query = """
            INSERT INTO data (name, salary, skills, experience, employment_mode, description, vacancy_link)
            VALUES (%s, %s, %s, %s, %s, %s, %s);
            """
            cursor.execute(insert_query, (name, salary, skills, experience, employment_mode, description, vacancy_link))
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
    print("Connection refused...")
    print(ex)


if __name__ == "__main__":
    for a in get_links("Инженер"):
        insert_in_db(get_vacancy(a), connect)
        time.sleep(1)








#Подключение к базе данных
# try:
#     connect = pymysql.connect(
#         host=host,
#         port=3303,
#         user=user,
#         password=password,
#         database=db_name,
#         cursorclass=pymysql.cursors.DictCursor
#     )
#     print("Successfully connected")
# except Exception as ex:
#     print("Connection refused...")
#     print(ex)

# try:
    # with connect.cursor() as cursor:
    #     create_table = """
    #     CREATE TABLE DATA (
    #         id int AUTO_INCREMENT,
    #         name varchar(255),
    #         salary varchar(255),
    #         skills varchar(255),
    #         experience varchar(255),
    #         employment_mode varchar(255),
    #         description TEXT,
    #         PRIMARY KEY (id)
    #     )
    #     """
    #     cursor.execute(create_table)
    #     print("Table created successfully")
#     name = "JAVA Developer"
#     with connect.cursor() as cursor:
#         insert = f"INSERT INTO data (name, salary, skills, experience, employment_mode, description) VALUES ('{name}', 100000, 'Python', '1-3 года', 'Полная занятость', 'Здесь должно быть какое-то длинное описание');"
#         cursor.execute(insert)
#         connect.commit()
#
#
# finally:
#     connect.close()


































#
# url = "https://hh.ru/search/vacancy?page=0&disableBrowserCache=true&hhtmFrom=vacancy_search_list"
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 YaBrowser/24.6.0.0 Safari/537.36'
# }
#
# response = requests.get(url, headers=headers)
# soup = BeautifulSoup(response.text, "lxml")
#
# data = soup.find_all("div", class_="vacancy-card--z_UXteNo7bRGzxWVcL7y font-inter")
#
# for i in data:
#     mini_info = i.find("div", class_="info-section--N695JG77kqwzxWAnSePt")
#
#     name = i.find("span", class_="vacancy-name--c1Lay3KouCl7XasYakLk serp-item__title-link").text
#     salary = i.find("span", class_="fake-magritte-primary-text--Hdw8FvkOzzOcoR4xXWni compensation-text--kTJ0_rp54B2vNeZ3CTt2 separate-line-on-xs--mtby5gO4J0ixtqzW38wh").text
#     link = i.find("a", class_="bloko-link").get("href")
#     employer = mini_info.find("span", class_="separate-line-on-xs--mtby5gO4J0ixtqzW38wh").text
#     address = mini_info.find("span", class_="fake-magritte-primary-text--Hdw8FvkOzzOcoR4xXWni").text
#
#     print(name)
#     print(salary)
#     print(link)
#     print(employer)
#     print(address)




