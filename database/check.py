#
#           Контакты разработчика:
#               VK: vk.com/andr3y_scoh
#               Telegram: t.me/andr3y_scoh
#               Github: github.com/SCOH-dev
#
#     ░██████╗░█████╗░░█████╗░██╗░░██╗
#     ██╔════╝██╔══██╗██╔══██╗██║░░██║
#     ╚█████╗░██║░░╚═╝██║░░██║███████║
#     ░╚═══██╗██║░░██╗██║░░██║██╔══██║
#     ██████╔╝╚█████╔╝╚█████╔╝██║░░██║
#     ╚═════╝░░╚════╝░░╚════╝░╚═╝░░╚═╝

"""
Поиск по БазеДанных Sqlite3
"""

import sqlite3

async def import_db(user_id):
    """
    Поиск последней заявки по user_id
    """
    # Подключение к БД, создание курсора
    db = sqlite3.connect("ScohWorld.db")
    cursor = db.cursor()

    try:
        # Поиск в БД записей по user_id с возвратом последней заявки по последнему aplication_id
        cursor.execute(
            """
            SELECT * FROM users 
            WHERE user_id = ?
            ORDER BY aplication_id DESC
            LIMIT 1
            """,
            (user_id,)
            )
        result = cursor.fetchone()

        if result is None:
            raise ValueError(f"User {user_id} was not found in the database")

        return result

    # Обработка ошибок c БД
    except sqlite3.Error as e:
        print(f"An error occurred: {e.args[0]}")

    # Закрытие соединений
    finally:
        cursor.close()
        db.close()


async def check_reg(user_id):
    """
    Проверка есть ли участник в базе

    Если да, возвращаем его статус и номер заявки
    Если нет, возвращаем False
    """
    try:
        # Подключение к БД и создание курсора
        db = sqlite3.connect("ScohWorld.db")
        cursor = db.cursor()

        # Поиск в БД статуса последней записи по user_id
        cursor.execute(
            """
            SELECT * FROM users 
            WHERE user_id = ?
            ORDER BY aplication_id DESC
            LIMIT 1
            """,
            (user_id,)
        )
        result = cursor.fetchone()
        # Возврат данных
        if not result:
            return False
        else:
            return result[8], result[1]

    # Обработка ошибок с БД
    except sqlite3.Error as e:
        print(f"Error with database: {e}")
        return False

    # Закрытие соединений
    finally:
        cursor.close()
        db.close()


async def check_adm(user_id):
    """
    Проверка есть ли участник админ права

    Если да, возвращаем его True
    Если нет, возвращаем False
    """
    try:
        # Подключение к БД и создание курсора
        db = sqlite3.connect("ScohWorld.db")
        cursor = db.cursor()

        # Поиск в БД статуса последней записи по user_id
        cursor.execute(
            """
            SELECT * FROM users 
            WHERE user_id = ?
            ORDER BY aplication_id DESC
            LIMIT 1
            """,
            (user_id,)
        )
        result = cursor.fetchone()
        # Возврат данных
        if not result:
            return False
        else:
            if result[9] == 1:
                return True
            else:
                return False

    # Обработка ошибок с БД
    except sqlite3.Error as e:
        print(f"Error with database: {e}")
        return False

    # Закрытие соединений
    finally:
        cursor.close()
        db.close()

async def check_dbl_nick(user_id, nick):
    """
    Проверка, не совпадает ли ник игрока с ником другого игрока.

    Args:
        user_id (int): ID пользователя в Telegram.
        nick (str): Игровой ник для проверки.

    Returns:
        bool: 
            True, если ник занят другим игроком,
            False, если ник свободен или принадлежит текущему игроку.
    """
    try:
        # Подключение к базе данных
        db = sqlite3.connect("ScohWorld.db")
        cursor = db.cursor()

        # Проверяем, есть ли ник у других пользователей (исключая текущего user_id)
        cursor.execute(
            """
            SELECT user_id FROM users 
            WHERE game_name = ? AND user_id != ?
            """,
            (nick, user_id)
        )
        result = cursor.fetchone()

        # Если найдена запись с таким ником у другого user_id, возвращаем True
        if result:
            return True
        else:
            return False

    except sqlite3.Error as e:
        print(f"Ошибка базы данных: {e}")
        return False

    finally:
        cursor.close()
        db.close()

async def get_admin_ids():
    """
    Поиск всех айди, где Admin = 1

    Args:
        user_id (int): ID пользователя в Telegram.

    Returns:
        bool: 
            True, если ник занят другим игроком,
            False, если ник свободен или принадлежит текущему игроку.
    """
    try:
        # Подключение к базе данных
        db = sqlite3.connect("ScohWorld.db")
        cursor = db.cursor()

        # Выполнение запроса
        cursor.execute("SELECT user_id FROM users WHERE Admin = 1")
        result = cursor.fetchall()

        # Преобразование результата в плоский список
        admin_ids = [row[0] for row in result]  # Извлекаем user_id из каждого кортежа

        return admin_ids  # Вернет [], если записей нет, или [id1, id2, ...]

    except sqlite3.Error as e:
        print(f"Ошибка базы данных: {e}")
        return []

    finally:
        cursor.close()
        db.close()
