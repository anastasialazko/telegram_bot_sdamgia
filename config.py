import ujson
import logging
logging.basicConfig(level=logging.INFO)


TOKEN = "***"
# База данных хранит выбранные юзером предметы
BOT_DB_NAME = "users_exams"
# Тестовые данные поддерживаемых экзаменов
BASE_DOMAIN = 'sdamgia.ru'
SUBJECT_BASE_URL = {
            'math': f'https://math-ege.{BASE_DOMAIN}',
            'mathb': f'https://mathb-ege.{BASE_DOMAIN}',
            'phys': f'https://phys-ege.{BASE_DOMAIN}',
            'inf': f'https://inf-ege.{BASE_DOMAIN}',
            'rus': f'https://rus-ege.{BASE_DOMAIN}',
            'bio': f'https://bio-ege.{BASE_DOMAIN}',
            'en': f'https://en-ege.{BASE_DOMAIN}',
            'chem': f'https://chem-ege.{BASE_DOMAIN}',
            'geo': f'https://geo-ege.{BASE_DOMAIN}',
            'soc': f'https://soc-ege.{BASE_DOMAIN}',
            'de': f'https://de-ege.{BASE_DOMAIN}',
            'fr': f'https://fr-ege.{BASE_DOMAIN}',
            'lit': f'https://lit-ege.{BASE_DOMAIN}',
            'sp': f'https://sp-ege.{BASE_DOMAIN}',
            'hist': f'https://hist-ege.{BASE_DOMAIN}',
        }

BOT_SUBJECTS = {
    "math": "Математика",
    "mathb": "Математика база",
    "phys": "Физика",
    "inf": "Информатика",
    "rus": "Русский язык",
    "bio": "Биология",
    "chem": "Химия",
    "geo": "География",
    "soc": "Обществознание",
    "lit": "Литература",
    "hist": "История",
}
