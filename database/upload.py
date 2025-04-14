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
Взаимодействие с БД

Загрузка данных в базу
"""

import sqlite3
from utils.msk_time import get_msk_time_now

async def upload_db(
        user_id,
        aplication_id = 1,
        username_tg = None,
        username = None,
        user_age = None,
        date = get_msk_time_now(),
        info = None,
        game_name = None,
        state = "Pending"
        ):
    """
    Загрузка данных в базу данных
    """
    try:
        db = sqlite3.connect("ScohWorld.db")

        cursor = db.cursor()

        cursor.execute(
            """
            INSERT INTO users (
            user_id,
            aplication_id,
            username_tg,
            username,
            user_age,
            date,
            info,
            game_name,
            state
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (user_id, aplication_id, username_tg, username, user_age, date, info, game_name, state),
            )

        db.commit()

    except sqlite3.Error as e:
        print(f"An error occurred: {e.args[0]}")
    finally:
        cursor.close()
        db.close()

async def update_db(user_id, value):
    """
    Изменение данных в базе данных
    """
    try:
        db = sqlite3.connect("ScohWorld.db")

        cursor = db.cursor()

        cursor.execute(
            """
            UPDATE users
            SET state = ?
            WHERE user_id = ?
            AND aplication_id = (SELECT MAX(aplication_id) FROM users WHERE user_id = ?)
            """,
            (value, user_id, user_id),
            )

        db.commit()

    except sqlite3.Error as e:
        print(f"An error occurred: {e.args[0]}")
    finally:
        cursor.close()
        db.close()
