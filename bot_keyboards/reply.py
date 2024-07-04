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
            KeyboardButton(text='Следующая вакансия')

        ],
        {
            KeyboardButton(text='Вернуться к выбору'),
            KeyboardButton(text='Настроить фильтры')
        }
    ],
    resize_keyboard=True
)

resume_play_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Следующее резюме')

        ],
        {
            KeyboardButton(text='Вернуться к выбору'),
            KeyboardButton(text='Настроить фильтры')
        }
    ],
    resize_keyboard=True
)


vacancy_filter_start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Применить фильтр")
        ],
        [
            KeyboardButton(text='Город'),
            KeyboardButton(text='Опыт работы'),
            KeyboardButton(text='Тип занятости')
        ],
        [
            KeyboardButton(text='Очистить фильтр')
        ]
    ],
    resize_keyboard=True,
)

vacancy_location_filter_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Оставить поле пустым')
        ],
    ],
    resize_keyboard=True,
    input_field_placeholder='Введите название города'
)


vacancy_experience_filter_kb = ReplyKeyboardMarkup(
    keyboard=[

            [KeyboardButton(text='От 3 до 6 лет')],
            [KeyboardButton(text='От 1 года до 3 лет')],
            [KeyboardButton(text='Более 6 лет')],
            [KeyboardButton(text='Нет опыта')],
            [KeyboardButton(text='Очистить опыт работы')]

    ],
    resize_keyboard=True,
    input_field_placeholder='Выберите опыт работы'
)


vacancy_emp_mode_filter_kb = ReplyKeyboardMarkup(
    keyboard=[

            [KeyboardButton(text='Полная занятость')],
            [KeyboardButton(text='Частичная занятость')],
            [KeyboardButton(text='Стажировка')],
            [KeyboardButton(text='Проектная работа')],
            [KeyboardButton(text='Волонтерство')],
            [KeyboardButton(text='Очистить тип занятости')]

    ],
    resize_keyboard=True,
    input_field_placeholder='Выберите тип занятости'
)



del_kb = ReplyKeyboardRemove()

