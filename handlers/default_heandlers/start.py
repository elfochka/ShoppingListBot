from telebot.types import Message
from config_data.config import DEFAULT_COMMANDS, CUSTOM_COMMANDS
from loader import bot
from my_logging import my_log


@bot.message_handler(commands=['start', 'main'])
def bot_start(message: Message) -> None:
    """
    Ловим команду start и help и выдаем список дефолтных команд
    :param message:
    :return: (None)
    """
    try:
        # start_parameter = message.text[7:]
        # if start_parameter ==
        text = [f"Привет, *{message.from_user.full_name}*!\n"
                f"Это бот для составления списков покупок.\n"
                f"Список команд, которые понимает бот."] + \
               [f'/{command} - {desk}' for command, desk in DEFAULT_COMMANDS] + \
               [f'/{command} - {desk}' for command, desk in CUSTOM_COMMANDS]
        bot.reply_to(message, '\n'.join(text), parse_mode='MarkDown')
    except Exception as e:
        my_log.logger.exception(e)
