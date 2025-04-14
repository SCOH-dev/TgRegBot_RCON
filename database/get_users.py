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
Добавление нового пользователя в список
"""

def update_config_users(user_id):
    """Обновляет список USERS в config.py"""
    # Читаем текущий config.py
    with open("config.py", "r", encoding="utf-8") as file:
        lines = file.readlines()

    # Ищем строку с USERS и обновляем её
    for i, line in enumerate(lines):
        if line.strip().startswith("USERS ="):
            # Извлекаем часть строки после "USERS ="
            users_str = line.strip().replace("USERS =", "").strip()
            # Убираем квадратные скобки и разбиваем по запятым
            users_str = users_str.strip("[]")
            if users_str:
                # Если строка не пустая, преобразуем в список чисел
                users = [int(x.strip()) for x in users_str.split(",")]
            else:
                # Если список пустой (USERS = []), начинаем с пустого списка
                users = []
            # Добавляем user_id, если его нет
            if user_id not in users:
                users.append(user_id)
                # Формируем новую строку
                lines[i] = f"USERS = {users}\n"
                print(f"Добавлен {user_id} в config.py")
            break
    else:
        # Если строка USERS не найдена, добавляем её в конец
        lines.append(f"USERS = [{user_id}]\n")
        print(f"Создан новый список USERS с {user_id}")

    # Переписываем config.py
    try:
        with open("config.py", "w", encoding="utf-8") as file:
            file.writelines(lines)
    except Exception as e: # pylint: disable=broad-exception-caught
        print(f"Ошибка при записи в config.py: {e}")
