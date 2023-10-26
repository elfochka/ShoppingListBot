import os
from dotenv import set_key

bot_token = os.environ.get('BOT_TOKEN')
host = os.environ.get('HOST')
user = os.environ.get('USER')
db_password = os.environ.get('DB_PASSWORD')

set_key('.env', 'BOT_TOKEN', bot_token)
set_key('.env', 'HOST', host)
set_key('.env', 'USER', user)
set_key('.env', 'DB_PASSWORD', db_password)
