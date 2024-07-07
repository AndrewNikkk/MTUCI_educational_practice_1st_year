import asyncio
import os

from aiogram import Bot, Dispatcher, types, F
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, StateFilter
#
# from dotenv import load_dotenv, find_dotenv
#
# load_dotenv(find_dotenv())

from Bot_handlers.vacancy_handlers import vacancy_router
from Bot_handlers.resume_handlers import resume_router
from bot_cmds_list import private
from bot_keyboards import reply
from async_vacancy import stop_vacancy
from async_resume import stop_resume
from config import TOKEN

ALLOWED_UPDATES = ["message, edited_message"]

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


dp.include_router(vacancy_router)
dp.include_router(resume_router)


@dp.message(CommandStart())
async def start_cmd(message: types.Message, state: FSMContext):
    await message.answer("Здравствуйте, начнем поиск!", reply_markup=reply.start_kb)
    await state.clear()
    await stop_vacancy()
    await stop_resume()


@dp.message(StateFilter('*'), F.text.lower() == 'вернуться к выбору')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await stop_vacancy()
    await stop_resume()
    await state.clear()
    await message.answer("<b>Выберите раздел поиска...</b>", reply_markup=reply.start_kb)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)


asyncio.run(main())
