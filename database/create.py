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
Создание базы данных для хранения заявок пользователей
"""

import sqlite3

async def create_db():
    """
    Создание/обновление новой базы данных
    """
    try:
        # Создание/поделючение к БД
        db = sqlite3.connect("ScohWorld.db")

        cursor = db.cursor()

        # Создание таблиц
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER,
                aplication_id INTEGER,
                username_tg TEXT,
                username TEXT,
                user_age INTEGER,
                date TEXT,
                info TEXT,
                game_name TEXT,
                state TEXT,
                Admin INTEGER NOT NULL DEFAULT 0
            )
            """)

    except sqlite3.Error as e:
        print(f"An error occurred: {e.args[0]}")

    # Закрытие соедений
    finally:
        cursor.close()
        db.close()
