from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.keyboard import KeyboardBuilder

start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Вакансии'),
            KeyboardButton(text='Резюме')
        ],
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите нужный раздел"
)


vacancy_start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Начать просмотр вакансий')
        ],
    ],
    resize_keyboard=True,
    input_field_placeholder="Нажмите, чтобы начать просмотр загруженных вакансий"
)

resume_start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Начать просмотр резюме')
        ],
    ],
    resize_keyboard=True,
    input_field_placeholder="Нажмите, чтобы начать просмотр загруженных резюме"
)



vacancy_play_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Следующая вакансия'),
            KeyboardButton(text='Вернуться к выбору')
        ],
    ],
    resize_keyboard=True
)

resume_play_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Следующее резюме'),
            KeyboardButton(text='Вернуться к выбору')
        ],
    ],
    resize_keyboard=True
)



del_kb = ReplyKeyboardRemove()

