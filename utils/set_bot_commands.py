from telebot.types import BotCommand
import handlers
from config_data.config import DEFAULT_COMMANDS, CUSTOM_COMMANDS


def set_commands(bot):
    bot.set_my_commands(
        [BotCommand(*i) for i in DEFAULT_COMMANDS] + [
            BotCommand(*i) for i in CUSTOM_COMMANDS]
    )
