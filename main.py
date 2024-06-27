import requests
from bs4 import BeautifulSoup

url = "https://hh.ru/search/vacancy?page=0&disableBrowserCache=true&hhtmFrom=vacancy_search_list"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 YaBrowser/24.6.0.0 Safari/537.36'
}

response = requests.get(url, headers=headers)

soup = BeautifulSoup(response.text, "lxml")

data = soup.find("div", class_="vacancy-card--z_UXteNo7bRGzxWVcL7y font-inter")
compensation_labels_data = data.find("div", class_="compensation-labels--uUto71l5gcnhU2I8TZmz")

name = data.find("span", class_="vacancy-name--c1Lay3KouCl7XasYakLk serp-item__title-link").text
salary = data.find("span", class_="fake-magritte-primary-text--Hdw8FvkOzzOcoR4xXWni compensation-text--kTJ0_rp54B2vNeZ3CTt2 separate-line-on-xs--mtby5gO4J0ixtqzW38wh").text
experience = compensation_labels_data.find("span", class_="label--rWRLMsbliNlu_OMkM_D3 label_light-gray--naceJW1Byb6XTGCkZtUM").text


print(name)
print(salary)
print(experience)