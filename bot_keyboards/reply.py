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


resume_filter_start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Применить фильтр")
        ],
        [
            KeyboardButton(text='Город'),
            KeyboardButton(text='Статус'),
            KeyboardButton(text='График работы')
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


resume_location_filter_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Оставить поле пустым')
        ],
    ],
    resize_keyboard=True,
    input_field_placeholder='Введите название города'
)


resume_status_filter_kb = ReplyKeyboardMarkup(
    keyboard=[

            [KeyboardButton(text='Не ищет работу')],
            [KeyboardButton(text='Рассматривает предложения')],
            [KeyboardButton(text='Активно ищет работу')],
            [KeyboardButton(text='Предложили работу, решает')],
            [KeyboardButton(text='Вышел на новое место')],
            [KeyboardButton(text='Без статуса поиска')],
            [KeyboardButton(text='Очистить статус поиска')]


    ],
    resize_keyboard=True,
    input_field_placeholder='Выберите статус поиска'
)


resume_work_schedule_filter_kb = ReplyKeyboardMarkup(
    keyboard=[

            [KeyboardButton(text='Полный день')],
            [KeyboardButton(text='Удаленная работа')],
            [KeyboardButton(text='Гибкий график')],
            [KeyboardButton(text='Сменный график')],
            [KeyboardButton(text='Вахтовый метод')],
            [KeyboardButton(text='Очистить график работы')]

    ],
    resize_keyboard=True,
    input_field_placeholder='Выберите график работы'
)
del_kb = ReplyKeyboardRemove()


vacancy_continue_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Начать просмотр вакансий')
        ],
        [
            KeyboardButton(text='Настроить фильтры')
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder="Нажмите, чтобы начать просмотр загруженных вакансий или настроить фильтры"
)


resume_continue_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Начать просмотр резюме')
        ],
        [
            KeyboardButton(text='Настроить фильтры')
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder="Нажмите, чтобы начать просмотр загруженных резюме или настроить фильтры"
)

