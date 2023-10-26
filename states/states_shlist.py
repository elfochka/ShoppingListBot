from telebot.handler_backends import State, StatesGroup


class GeneralStates(StatesGroup):
    main = State()


class AddList(StatesGroup):
    command = State()
    list = State()
    product = State()
    quantity = State()
    finish = State()


class Lists(StatesGroup):
    command = State()
    operation = State()
    select = State()
    check_product = State()
    list = State()

    product = State()
    quantity = State()
    finish = State()
