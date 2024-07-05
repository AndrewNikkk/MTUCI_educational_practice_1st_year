import time
import aiohttp
import asyncio
import aiomysql
from bs4 import BeautifulSoup

from async_mysql import filling_vacancy_table, loop
from get_areas_id import find_areas_id
from config import *


async def get_links(text, area_name):
    area_id, parrent_id = await find_areas_id(area_name)
    if area_id is not None:
        async with aiohttp.ClientSession() as session:
            data = await session.get(
                url=f"https://hh.ru/search/resume?text={text}&area={area_id}&isDefaultArea=true&pos=full_text&logic=normal&exp_period=all_time&ored_clusters=true&order_by=relevance&search_period=0&page=1",
                headers={
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 YaBrowser/24.6.0.0 Safari/537.36"}
            )
            print(text, area_id)
            print(data.status)
            if data.status != 200:
                return
            soup = BeautifulSoup(await data.text(), "lxml")
            try:
                page_count = int(
                    soup.find("div", attrs={"class": "pager"}).find_all("span", recursive=False)[-1].find("a").find(
                        "span").text)
            except:
                page_count = 0
            if page_count == 0:
                try:
                    data = await session.get(
                        url=f"https://hh.ru/search/resume?text={text}&area={area_id}&isDefaultArea=true&pos=full_text&logic=normal&exp_period=all_time&ored_clusters=true&order_by=relevance&search_period=0&page=0",
                        headers={
                            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 YaBrowser/24.6.0.0 Safari/537.36"}
                    )
                    if data.status != 200:
                        return
                    soup = BeautifulSoup(await data.text(), "lxml")
                    for a in soup.find_all("a", attrs={"data-qa": "serp-item__title", "class": "bloko-link"}):
                        yield f"https://hh.ru{a.attrs['href'].split('?')[0]}"
                except Exception as e:
                    print(f"{e}")
                await asyncio.sleep(1)
            else:
                for page in range(page_count):
                    try:
                        data = await session.get(
                            url=f"https://hh.ru/search/resume?text={text}&area={area_id}&isDefaultArea=true&pos=full_text&logic=normal&exp_period=all_time&ored_clusters=true&order_by=relevance&search_period=0&page={page}",
                            headers={
                                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 YaBrowser/24.6.0.0 Safari/537.36"}
                        )
                        if data.status != 200:
                            continue
                        soup = BeautifulSoup(await data.text(), "lxml")
                        for a in soup.find_all("a", attrs={"data-qa": "serp-item__title", "class": "bloko-link"}):
                            yield f"https://hh.ru{a.attrs['href'].split('?')[0]}"
                    except Exception as e:
                        print(f"{e}")
                    await asyncio.sleep(1)
    else:
        async with aiohttp.ClientSession() as session:
            data = await session.get(
                url=f"https://hh.ru/search/resume?text={text}&area=113&isDefaultArea=true&pos=full_text&logic=normal&exp_period=all_time&ored_clusters=true&order_by=relevance&search_period=0&page=0",
                headers={
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 YaBrowser/24.6.0.0 Safari/537.36"}
            )
            if data.status != 200:
                return
            soup = BeautifulSoup(await data.text(), "lxml")
            try:
                page_count = int(
                    soup.find("div", attrs={"class": "pager"}).find_all("span", recursive=False)[-1].find("a").find(
                        "span").text)
            except:
                return

            for page in range(page_count):
                try:
                    data = await session.get(
                        url=f"https://hh.ru/search/resume?text={text}&area=113&isDefaultArea=true&pos=full_text&logic=normal&exp_period=all_time&ored_clusters=true&order_by=relevance&search_period=0&page={page}",
                        headers={
                            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 YaBrowser/24.6.0.0 Safari/537.36"}
                    )
                    if data.status != 200:
                        continue
                    soup = BeautifulSoup(await data.text(), "lxml")
                    for a in soup.find_all("a", attrs={"data-qa": "serp-item__title", "class": "bloko-link"}):
                        yield f"https://hh.ru{a.attrs['href'].split('?')[0]}"
                except Exception as e:
                    print(f"{e}")
                await asyncio.sleep(1)
async def main(loc):
    async for a in get_links('Программист', loc):
        print(a)

if __name__ == "__main__":
    asyncio.run(main('Москва'))