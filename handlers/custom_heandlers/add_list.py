from database.my_db import get_products
from handlers.custom_heandlers import lists
from keyboards.inline.keyboard import inline_products
from loader import bot
from my_logging import my_log
from states.states_shlist import AddList, Lists
from database import my_db


@bot.message_handler(commands=['add'])
def get_command(message) -> None:
    """
    ловим команды 'add'
    Запрашиваем название списка и записываем команду
    :param message: сообщение пользователя
    :return: (None)
    """
    try:
        bot.set_state(message.from_user.id, AddList.command, message.chat.id)
        bot.reset_data(message.from_user.id)
        text = 'Введите название списка покупок (например, "Продукты на неделю").'
        new_list_message_id = bot.send_message(message.chat.id, text).id
        bot.set_state(message.from_user.id, AddList.list, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['user_id'] = message.chat.id
            data['command'] = message.text
            data['products'] = []
            data['user_name'] = message.from_user.full_name
            data['new_list_message_id'] = new_list_message_id
            data['add_message'] = message
    except Exception as e:
        my_log.logger.exception(e)


@bot.message_handler(state=AddList.list)
def add_list(message) -> None:
    """
    Запрашиваем продукт у пользователя и записываем название списка
    :param message: сообщение пользователя
    :return: (None)
    """
    try:
        if str(message.text)[0] != '/':
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                new_list_message_id = data['new_list_message_id']
            bot.delete_message(message.chat.id, new_list_message_id)

            text = f'Вводите товары в список *{message.text}* ' \
                   f'отдельными сообщениями или одним сообщением, ' \
                   f'каждый товар с новой строки.'
            new_list_message_id = bot.send_message(message.chat.id, text, parse_mode="Markdown").id

            bot.set_state(message.from_user.id, AddList.product, message.chat.id)

            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data['list_name'] = message.text
                data['new_list_message_id'] = new_list_message_id
                data['list_id'] = my_db.add_list(data['user_id'], data['user_name'], data['list_name'])
        else:
            bot.set_state(message.from_user.id, AddList.product, message.chat.id)

    except Exception as e:
        my_log.logger.exception(e)


@bot.message_handler(state=AddList.product)
def add_product_message(message) -> None:
    """
    Запрашиваем количество у пользователя и записываем продукт
    :param message: сообщение пользователя
    :return: (None)
    """
    try:
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            list_name = data['list_name']
            new_list_message_id = data['new_list_message_id']
            #
            list_id = data['list_id']
            products = message.text.split('\n')
            for product in products:
                my_db.add_product(list_id, product)
        bot.delete_message(message.chat.id, new_list_message_id)
        products = get_products(list_id)
        text = f'Вводите товары в список *{list_name}* ' \
               f'отдельными сообщениями или одним сообщением, ' \
               f'каждый товар с новой строки. Когда закончите нажмите "Завершить"'
        new_list_message_id = bot.send_message(message.chat.id, text,
                                               reply_markup=inline_products('', products), parse_mode="Markdown").id
        bot.set_state(message.from_user.id, AddList.product, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['new_list_message_id'] = new_list_message_id

    except Exception as e:
        my_log.logger.exception(e)


@bot.callback_query_handler(func=lambda call: True,
                            state=AddList.product)
def add_product_call(call) -> None:
    try:
        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            add_message = data['add_message']
            new_list_message_id = data['new_list_message_id']

        if call.message.id == new_list_message_id:
            if call.data == 'stop':
                bot.delete_message(call.message.chat.id, new_list_message_id)
                text = 'Список запомнил'
                new_list_message_id = bot.send_message(call.message.chat.id, text).id
                bot.delete_message(call.message.chat.id, new_list_message_id)
                bot.reset_data(call.from_user.id)
                bot.set_state(call.from_user.id, Lists.command, call.message.chat.id)

                lists.get_command(add_message)

    except Exception as e:
        my_log.logger.exception(e)
