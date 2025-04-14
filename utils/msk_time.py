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
Текущее время в МСК
"""

from datetime import datetime
import pytz

def get_msk_time_now():
    """
    Получаем текущее время в Московском часовом поясе
    """
    # Задаем московский часовой пояс (UTC+3)
    moscow_tz = pytz.timezone("Europe/Moscow")

    # Получаем текущее время в UTC и преобразуем в МСК
    moscow_time = datetime.now(pytz.utc).astimezone(moscow_tz)

    # Форматируем время в нужный формат
    formatted_time = moscow_time.strftime("%Y-%m-%d %H:%M:%S")
    return formatted_time
