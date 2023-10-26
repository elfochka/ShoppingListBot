from telebot.types import Message
from config_data.config import DEFAULT_COMMANDS, CUSTOM_COMMANDS
from loader import bot
from my_logging import my_log


@bot.message_handler(commands=['help'])
def bot_start(message: Message) -> None:
    """
    Ловим команду help и выдаем описание
    :param message:
    :return: (None)
    """
    try:
        text = [f"Привет, *{message.from_user.full_name}*!\n"
                f"Это бот для составления списков покупок.\n"
                f"Список команд, которые понимает бот."] + \
               [f'/{command} - {desk}' for command, desk in DEFAULT_COMMANDS] + \
               [f'/{command} - {desk}' for command, desk in CUSTOM_COMMANDS]
        bot.reply_to(message, '\n'.join(text), parse_mode='MarkDown')
    except Exception as e:
        my_log.logger.exception(e)
