from config_data import config
import pymysql.cursors

from my_logging import my_log
import datetime


def create_connection():
    return pymysql.connect(host=config.HOST,
                           user=config.USER,
                           password=config.DB_PASSWORD,
                           database='u1771772_default',
                           cursorclass=pymysql.cursors.DictCursor)


def add_list(user_id: str, user_name: str, list_name: str) -> int:
    """
    Добавляем новый список в БД
    :param user_id:
    :param user_name:
    :param list_name:
    :return: list_id: int
    """
    try:
        connection = create_connection()
        with connection:
            with connection.cursor() as cursor_add:
                sql_add = "INSERT INTO `ShoppingList` (`user_id`, `user_name`, `list_name`) VALUES (%s, %s, %s)"
                cursor_add.execute(sql_add, (
                    user_id, user_name, list_name))

                # Получаем автоматически сгенерированный list_id
                cursor_add.execute("SELECT LAST_INSERT_ID() as list_id")
                result = cursor_add.fetchone()
                list_id = result['list_id']

                connection.commit()

        return list_id

    except BaseException as e:
        my_log.logger.exception(e)
        # return None


def add_product(list_id: int, product: str) -> None:
    """
    Добавляем новый продукт в список
    :param list_id:
    :param product:
    :return:
    """
    try:
        connection = create_connection()
        with connection:
            with connection.cursor() as cursor_add:
                sql_add = "INSERT INTO `ShoppingProducts` (`list_id`, `product_name`) VALUES (%s, %s)"
                cursor_add.execute(sql_add, (list_id, product))
            connection.commit()
        connection.close()

    except BaseException as e:
        my_log.logger.exception(e)


def get_lists(user_id: int) -> dict:
    """
    Возвращает все списки покупок для данного пользователя.

    :param user_id: идентификатор пользователя
    :return: словарь со списками покупок
    """
    try:
        shopping_lists = {}
        connection = create_connection()
        with connection:
            with connection.cursor() as cursor:
                sql_query = "SELECT `date`, `list_id`, `list_name` FROM `ShoppingList` WHERE `user_id` = %s"
                cursor.execute(sql_query, (user_id,))

                for row in cursor.fetchall():
                    list_status = '📄'
                    date = row['date'].strftime("%d.%m.%Y")
                    list_id = int(row['list_id'])
                    list_name = str(row['list_name'])
                    products = get_products(list_id)
                    true_count = 0
                    for key, values in products.items():
                        if values['status']:
                            true_count += 1
                    # if  0 < true_count < len(products):
                    #     list_status = '🟡'
                    # elif true_count >= len(products):
                    #     list_status = '✅'
                    if true_count >= len(products):
                        list_status = '✅'
                    shopping_lists.update({list_id: {'name': list_name, 'date': date, 'list_status': list_status}})

        connection.close()



    except BaseException as e:
        my_log.logger.exception(e)
        return {}

    finally:
        return shopping_lists


def get_products(list_id: int) -> dict:
    """
    Возвращает все продукты для данного списка.

    :param list_id: id списка продуктов
    :return: словарь со списками покупок
    """
    try:
        products = {}
        connection = create_connection()
        with connection:
            with connection.cursor() as cursor:
                sql_query = "SELECT `product_id`, `product_name`, " \
                            "`status` FROM `ShoppingProducts` WHERE `list_id` = %s"
                cursor.execute(sql_query, (list_id,))
                for row in cursor.fetchall():
                    product_id = int(row['product_id'])
                    product_name = str(row['product_name'])
                    # product_quantity = str(row['product_quantity'])
                    status = bool(row['status'])
                    products.update({product_id: {'product_name': product_name,
                                                  'status': status}})

        connection.close()

    except BaseException as e:
        my_log.logger.exception(e)
        return {}

    finally:
        return products


def check_products(list_id: int, product_id: int) -> None:
    """
    Отмечает купленные продукты.

    :param list_id: id списка продуктов
    :param product_id: id продукта
    :return: None
    """
    try:
        connection = create_connection()
        with connection:
            with connection.cursor() as cursor:
                sql_query = "UPDATE `ShoppingProducts` SET `status` = TRUE WHERE `list_id` = %s AND `product_id` = %s"
                cursor.execute(sql_query, (list_id, product_id,))
            connection.commit()
        connection.close()

    except BaseException as e:
        my_log.logger.exception(e)


def del_products(list_id: int, product_id: int) -> None:
    """
    Удаляет выбранный продукт.

    :param list_id: id списка продуктов
    :param product_id: id продукта
    :return: None
    """
    try:
        connection = create_connection()
        with connection:
            with connection.cursor() as cursor:
                sql_query = "DELETE FROM `ShoppingProducts` WHERE `list_id` = %s AND `product_id` = %s"
                cursor.execute(sql_query, (list_id, product_id,))
            connection.commit()
        connection.close()

    except BaseException as e:
        my_log.logger.exception(e)


def clear_list(list_id: int) -> None:
    """
        Очищает список.
        :param list_id: id списка продуктов
        :return: None
        """
    try:
        connection = create_connection()
        with connection:
            with connection.cursor() as cursor:
                sql_query = "DELETE FROM `ShoppingProducts` WHERE `list_id` = %s"
                cursor.execute(sql_query, (list_id,))
            connection.commit()
        connection.close()

    except BaseException as e:
        my_log.logger.exception(e)


def delete_list(list_id: int) -> None:
    """
        Удаляет список и все связанные продукты.
        :param list_id: id списка продуктов
        :return: None
        """
    try:
        clear_list(list_id)

        connection = create_connection()
        with connection:
            with connection.cursor() as cursor:
                sql_query = "DELETE FROM `ShoppingList` WHERE `list_id` = %s"
                cursor.execute(sql_query, (list_id,))
            connection.commit()
        connection.close()

    except BaseException as e:
        my_log.logger.exception(e)
