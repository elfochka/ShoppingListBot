import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit('Переменные окружения не загружены т.к отсутствует файл .env')
else:
    load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
DEFAULT_COMMANDS = (
    ('start', "Вывести справку"),
    ('help', "Вывести справку")
)

CUSTOM_COMMANDS = (
    ('add', "Создать новый список покупок."),
    ('lists', "Просмотреть существующие списки покупок."),
)

HOST = os.getenv('HOST')
USER = os.getenv('USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
