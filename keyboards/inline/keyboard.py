from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def inline_yes_or_no() -> InlineKeyboardMarkup:
    """
    Инлайн клавиатура "да" или "нет"
    :return: (markup_inline) возвращает саму клавиатуру
    """
    markup_inline = InlineKeyboardMarkup()
    item_yes = InlineKeyboardButton(text='Ещё', callback_data='y')
    item_no = InlineKeyboardButton(text='Завершить', callback_data='stop')
    markup_inline.add(item_yes, item_no)
    return markup_inline


def inline_operation() -> InlineKeyboardMarkup:
    """
    Инлайн клавиатура "Закупка" или "Редактировать"
    :return: (markup_inline) возвращает саму клавиатуру
    """
    markup_inline = InlineKeyboardMarkup()
    item_shop = InlineKeyboardButton(text='Закупка', callback_data='shop')
    item_edit = InlineKeyboardButton(text='Редактировать', callback_data='edit')

    markup_inline.add(item_shop, item_edit)
    return markup_inline


def inline_lists(lists: dict) -> InlineKeyboardMarkup:
    """
    Инлайн клавиатура с выводом списка списков продуктов
    :param lists:
    :return: (markup_inline) возвращает саму клавиатуру
    """
    markup_inline = InlineKeyboardMarkup()
    buttons = []

    for list_id, values in lists.items():
        name = str(values['name'])
        date = str(values['date'])
        list_status = str(values['list_status'])

        button_text = f"{list_status}{date}: {name}"
        # button_text = f"{list_id}|{str(values['date'])}"
        callback_data = f"{list_id}|{date}|{name}"

        markup_inline.add(InlineKeyboardButton(text=button_text, callback_data=callback_data), )

    #     buttons.append(InlineKeyboardButton(text=button_text, callback_data=callback_data))
    #
    # for i in range(0, len(buttons), 2):
    #     if i + 1 < len(buttons):
    #         markup_inline.row(buttons[i], buttons[i + 1])
    #     else:
    #         markup_inline.row(buttons[i])

    return markup_inline


def inline_products(kb_type: str, products: dict) -> InlineKeyboardMarkup:
    """
    Инлайн клавиатура с выводом списка продуктов по id списка
    :param kb_type: 
    :param products:
    :return: (markup_inline) возвращает саму клавиатуру
    """
    markup_inline = InlineKeyboardMarkup()
    for product_id, values in products.items():
        mark = '▫️'
        if values['status']:
            mark = '✅ '
        button_text = mark + str(values['product_name'])
        markup_inline.add(InlineKeyboardButton(text=button_text, callback_data=product_id), )
    markup_inline.add(InlineKeyboardButton(text='🆗 Завершить', callback_data='stop'), )

    if kb_type == 'edit':
        markup_inline.add(InlineKeyboardButton(text='❌ Удалить список', callback_data='del_this_list'), )
    # else:
    #     # share_button = InlineKeyboardButton("Поделиться", switch_inline_query="")
    #     markup_inline.add(InlineKeyboardButton("Поделиться", switch_inline_query=""), )
    return markup_inline
