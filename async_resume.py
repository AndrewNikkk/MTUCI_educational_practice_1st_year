import time
import aiohttp
import asyncio
from bs4 import BeautifulSoup

from async_mysql import filling_resume_table

async def get_links(text):
    async with aiohttp.ClientSession() as session:
        data = await session.get(
            url=f"https://hh.ru/search/resume?text={text}&area=113&isDefaultArea=true&exp_period=all_time&logic=normal&pos=full_text&page=1",
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
                    url=f"https://hh.ru/search/resume?text={text}&area=113&isDefaultArea=true&exp_period=all_time&logic=normal&pos=full_text&page={page}",
                    headers={"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 YaBrowser/24.6.0.0 Safari/537.36"}
                )
                if data.status != 200:
                    continue
                soup = BeautifulSoup(await data.text(), "lxml")
                for a in soup.find_all("a", attrs={"data-qa": "serp-item__title", "class": "bloko-link"}):
                    yield f"https://hh.ru{a.attrs['href'].split('?')[0]}"
            except Exception as e:
                print(f"Ошибка на странице {page}: {e}")
            await asyncio.sleep(1)


async def get_resume(link):
    async with aiohttp.ClientSession() as session:
        data = await session.get(
            url=link,
            headers={"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 YaBrowser/24.6.0.0 Safari/537.36"}
        )
        if data.status != 200:
            return
        soup = BeautifulSoup(await data.text(),"lxml")
        try:
            name = soup.find(attrs={"class": "resume-block__title-text"}).text
        except:
            name = 'не указано'
        try:
            salary = (soup.find(attrs={"class": "resume-block__salary"}).text).replace("\u2009", " ").replace("\xa0"," ")
        except:
            salary = "желаемый заработок не указан"
        try:
            specialization = soup.find(attrs={"class": "resume-block__specialization"}).text
        except:
            specialization = 'не указаны'
        try:
            busyness_mode = soup.find(attrs={"class": "resume-block-container"}).find("p").text.replace("Занятость: ","")
        except:
            busyness_mode = 'не указана'
        try:
            work_schedule = soup.find(attrs={"class": "resume-block-container"}).find_all("p", recursive=False)[-1].text.replace("График работы: ", "")
        except:
            work_schedule = 'не указан'
        try:
            work_exp = [span.get_text().replace("\xa0", " ") for span in soup.find(attrs={"class": "resume-block__title-text resume-block__title-text_sub"}).find_all("span")] if soup.find(attrs={"class": "resume-block__title-text resume-block__title-text_sub"}) else []
            work_experience = ' '.join(work_exp)
        except:
            work_experience = ''
        try:
            key_skills = [b.get_text() for b in soup.find(attrs={"class": "bloko-tag-list"}).find_all(attrs={"class": "bloko-tag bloko-tag_inline"})]
        except:
            key_skills = 'не указаны'
        try:
            citizenship = soup.find(attrs={"data-qa": "resume-block-additional"}).find("p").text.replace("Гражданство: ", "")
        except:
            citizenship = 'не указано'
        try:
            location = soup.find(attrs={"class": "resume-header-title"}).find(attrs={"class": "bloko-translate-guard"}).text.replace("\xa0", " ")
        except:
            location = "не указана"
        try:
            job_search_status = soup.find(attrs={"data-qa": "job-search-status"}).text.replace("\xa0", " ")
        except:
            job_search_status = "не указан"

        resume_link = f"{link.replace('tver.', '')}"

        resume = {
            "name": name,
            "salary": salary,
            "specialization": specialization,
            "busyness_mode": busyness_mode,
            "work_schedule": work_schedule,
            "work_experience": work_experience,
            "key_skills": key_skills,
            "citizenship": citizenship,
            "location": location,
            "job_search_status": job_search_status,
            "resume_link": resume_link
        }

        return resume

async def insert_in_db_resume(text):
    async for a in get_links(f'{text}'):
        resume = await get_resume(a)
        if resume:
            try:
                name = resume.get("name", 'не указано')
                salary = resume.get("salary", '')
                specialization = resume.get("specialization", '')
                busyness_mode = resume.get("busyness_mode", 'не указан')
                work_schedule = resume.get("work_schedule", 'не указан')
                work_experience = resume.get("work_experience", 'none')
                key_skills = ', '.join(resume.get("key_skills", ["пусто"]))
                citizenship = resume.get("citizenship", "none")
                location = resume.get("location", "none")
                job_search_status = resume.get("job_search_status", "none")
                resume_link = resume.get('resume_link', 'none')
            except Exception as e:
                print(f"Произошла ошибка при извлечении данных: {e}")
                return
            try:
                await filling_resume_table(
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
                )
            except Exception as e:
                print(f'что-то пошло не так: {e}')


if __name__ == '__main__':
    asyncio.run(insert_in_db_resume('python'))