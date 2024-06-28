import requests
from bs4 import BeautifulSoup
# import fake_useragent
import time
import json


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


    vacancy = {
        "name":name,
        "salary":salary,
        "skills":skills,
        "experience":experience,
        "employment_mode":employment_mode,
        "description":description
    }
    return vacancy





if __name__ == "__main__":
    data = []
    for a in get_links("python"):
        data.append(get_vacancy(a))
        time.sleep(1)
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

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




