import aiohttp
import asyncio


async def get_areas_json():
    async with aiohttp.ClientSession() as session:
        try:
            response = await session.get(
                url="https://api.hh.ru/areas/113",
                headers={"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 YaBrowser/24.6.0.0 Safari/537.36"}
            )
        except Exception as e:
            print(e)
        if response.status != 200:
            return None
        return await response.json()


def find(response, area_name):
    if response.get("name") == area_name.title():
        return response.get('id'), response.get('parent_id')
    for area in response.get('areas', []):
        area_id, parent_id = find(area, area_name)
        if area_id is not None:
            return area_id, parent_id
    return None, None


async def find_areas_id(location):
    areas_data = await get_areas_json()
    if areas_data:
        area_id, parent_id = find(areas_data, f'{location}')
        if area_id:
            print(f'id населенного пункта {location}: {area_id}, {parent_id}')
            return area_id, parent_id
        else:
            print(f'Населенный пункт {location} не найден')
            return None, None


if __name__ == "__main__":
    asyncio.run(find_areas_id('Тверь'))
