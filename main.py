import requests
from bs4 import BeautifulSoup
import fake_useragent
import time
import json


def get_links(text):
    pass

def get_vacancy(link):
    pass


url = "https://hh.ru/search/vacancy?page=0&disableBrowserCache=true&hhtmFrom=vacancy_search_list"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 YaBrowser/24.6.0.0 Safari/537.36'
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "lxml")

data = soup.find_all("div", class_="vacancy-card--z_UXteNo7bRGzxWVcL7y font-inter")

for i in data:
    mini_info = i.find("div", class_="info-section--N695JG77kqwzxWAnSePt")

    name = i.find("span", class_="vacancy-name--c1Lay3KouCl7XasYakLk serp-item__title-link").text
    salary = i.find("span", class_="fake-magritte-primary-text--Hdw8FvkOzzOcoR4xXWni compensation-text--kTJ0_rp54B2vNeZ3CTt2 separate-line-on-xs--mtby5gO4J0ixtqzW38wh").text
    link = i.find("a", class_="bloko-link").get("href")
    employer = mini_info.find("span", class_="separate-line-on-xs--mtby5gO4J0ixtqzW38wh").text
    address = mini_info.find("span", class_="fake-magritte-primary-text--Hdw8FvkOzzOcoR4xXWni").text

    print(name)
    print(salary)
    print(link)
    print(employer)
    print(address)




