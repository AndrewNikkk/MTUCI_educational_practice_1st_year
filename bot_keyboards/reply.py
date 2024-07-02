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
            KeyboardButton(text='Начать просмотр')
        ],
    ],
    resize_keyboard=True,
    input_field_placeholder="Нажмите, чтобы начать просмотр загруженных вакансий"
)

vacancy_play_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Следующая вакансия')
        ],
    ],
    resize_keyboard=True
)

resume_start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Начать просмотр')
        ],
    ],
    resize_keyboard=True,
    input_field_placeholder="Нажмите, чтобы начать просмотр загруженных резюме"
)

vacancy_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Следующая'),
            KeyboardButton(text='Вернуться назад')
        ],
    ],
    resize_keyboard=True,
    input_field_placeholder="Воспользуйтесь клавиатурой ниже"
)



del_kb = ReplyKeyboardRemove()

