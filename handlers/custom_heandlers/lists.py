from database.my_db import get_lists, get_products, check_products, del_products, delete_list, add_product
from keyboards.inline.keyboard import inline_lists, inline_operation, inline_products
from loader import bot
from my_logging import my_log
from states.states_shlist import Lists


@bot.message_handler(commands=['lists'])
def get_command(message) -> None:
    """
    ловим команду 'lists'
    И выводим все списки продуктов пользователя
    :param message: сообщение пользователя
    :return: (None)
    """
    try:
        bot.set_state(message.from_user.id, Lists.command, message.chat.id)
        bot.reset_data(message.from_user.id)
        lists = get_lists(message.chat.id)
        if not lists:
            text = 'У Вас пока нет списков.'
            bot.send_message(message.chat.id, text)

        else:
            text = 'Ваши сохраненные списки покупок:'
            list_message_id = bot.send_message(message.chat.id, text, reply_markup=inline_lists(lists)).id
            bot.set_state(message.from_user.id, Lists.operation, message.chat.id)

            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data['user_id'] = message.chat.id
                data['lists'] = lists
                data['list_message_id'] = list_message_id
                data['operation'] = False

    except Exception as e:
        my_log.logger.exception(e)


@bot.callback_query_handler(func=lambda call: True,
                            state=Lists.operation)
def do_select(call) -> None:
    try:
        list_id, list_date, list_name = call.data.split("|", 2)
        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            list_message_id = data['list_message_id']

        bot.delete_message(call.message.chat.id, list_message_id)

        text = f'Вы хотите отмечать покупки или редактировать список *{list_name}* от {list_date}?'
        list_message_id = bot.send_message(call.message.chat.id, text,
                                           reply_markup=inline_operation(), parse_mode="Markdown").id
        bot.set_state(call.from_user.id, Lists.select, call.message.chat.id)

        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            data['now_list_id'] = list_id
            data['now_list_name'] = list_name
            data['list_message_id'] = list_message_id
            data['list_date'] = list_date
    except Exception as e:
        my_log.logger.exception(e)


@bot.callback_query_handler(func=lambda call: True,
                            state=Lists.select)
def do_select_call(call) -> None:
    """
    Выдаем список продуктов внутри выбранного списка
    :param call: отклик пользователя
    :return: (None)
    """
    try:
        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            list_name = data['now_list_name']
            list_message_id = data['list_message_id']
            now_list_id = data['now_list_id']
            list_date = data['list_date']
            if data['operation']:
                operation = data['operation']
            else:
                data['operation'] = call.data
                operation = data['operation']

        if call.data.isdigit():
            if call.message.id == list_message_id:
                if operation == 'shop':
                    check_products(now_list_id, call.data)
                else:
                    del_products(now_list_id, call.data)

        else:
            if call.data == 'stop':
                finish_list(call)
                return
            if call.data == 'del_this_list':
                delete_list(now_list_id)
                finish_list(call)
                return
            if call.data in ['shop', 'edit']:
                with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
                    data['operation'] = call.data

        products = get_products(now_list_id)

        text = f'Продукты по списку *{list_name}* от {list_date}'
        if operation == 'edit':
            text += '\nУдалите список или один продукт. Или можете добавить продукты ' \
                    'отдельными сообщениями или одним сообщением, ' \
                    f'каждый товар с новой строки.\n' \
                    f'Когда закончите нажмите "Завершить"'

        bot.edit_message_text(text, chat_id=call.message.chat.id, message_id=list_message_id,
                              reply_markup=inline_products(operation, products), parse_mode="Markdown")
        bot.set_state(call.from_user.id, Lists.select, call.message.chat.id)

        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            data['list_message_id'] = list_message_id

    except Exception as e:
        my_log.logger.exception(e)


@bot.message_handler(state=Lists.select)
def do_select_message(message) -> None:
    """
    Выдаем список продуктов внутри выбранного списка
    :param message: сообщение пользователя
    :return: (None)
    """
    try:
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            list_message_id = data['list_message_id']
            now_list_id = data['now_list_id']
            operation = data['operation']
            list_name = data['now_list_name']
            list_date = data['list_date']

            products = message.text.split('\n')

            for product in products:
                add_product(now_list_id, product)
        bot.delete_message(message.chat.id, list_message_id)

        products = get_products(now_list_id)
        text = f'Продукты по списку *{list_name}* от {list_date}'
        text += '\nУдалите список или один продукт. Или можете добавить продукты ' \
                'отдельными сообщениями или одним сообщением, ' \
                f'каждый товар с новой строки.\n' \
                f'Когда закончите нажмите "Завершить"'

        list_message_id = bot.send_message(message.chat.id, text,
                                           reply_markup=inline_products(operation, products),
                                           parse_mode="Markdown").id

        # bot.edit_message_reply_markup(message.from_user.id, list_message_id,
        #                               reply_markup=inline_products(operation, products))

        # text = f'Вводите товары в список *{list_name}* ' \
        #        f'отдельными сообщениями или одним сообщением, ' \
        #        f'каждый товар с новой строки. Когда закончите нажмите "Завершить"'
        # new_list_message_id = bot.send_message(message.from_user.id, text,
        #                                        reply_markup=inline_products('', products), parse_mode="Markdown").id
        bot.set_state(message.from_user.id, Lists.select, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['list_message_id'] = list_message_id

    except Exception as e:
        my_log.logger.exception(e)


@bot.callback_query_handler(func=lambda call: True,
                            state=Lists.list)
def finish_list(call) -> None:
    """
    Нажата кнопка завершить, возвращаем пользователю список его списков
    :param call: отклик пользователя
    :return: (None)
    """
    try:
        bot.set_state(call.from_user.id, Lists.list, call.message.chat.id)
        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            list_message_id = data['list_message_id']

        bot.reset_data(call.from_user.id)

        lists = get_lists(call.message.chat.id)
        if not lists:
            text = 'У Вас пока нет списков.'
            bot.edit_message_text(text, chat_id=call.message.chat.id, message_id=list_message_id)

        else:
            text = 'Ваши сохраненные списки покупок:'

            bot.edit_message_text(text, chat_id=call.message.chat.id, message_id=list_message_id,
                                  reply_markup=inline_lists(lists))
            bot.set_state(call.from_user.id, Lists.operation, call.message.chat.id)

            with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
                data['user_id'] = call.from_user.id
                data['lists'] = lists
                data['list_message_id'] = list_message_id
                data['operation'] = False

    except Exception as e:
        my_log.logger.exception(e)
