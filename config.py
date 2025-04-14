# pylint: disable=line-too-long
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
Конфигурация для бота
"""

import os
from dotenv import load_dotenv

load_dotenv()

TG_TOKEN = os.getenv('TG_TOKEN')

RCON_HOST = os.getenv('RCON_HOST')

RCON_PORT = os.getenv('RCON_PORT')

RCON_PASSWORD = os.getenv('RCON_PASSWORD')


FILENAME_USERS = "users.json"

FILENAME_TICKETS = "tickets.json"

SERVER_TEXT = (
    "🌐 <b>Информация о сервере</b>\n\n"
    "⚙️ <u>Версия</u>:\n"
    "<code>Forge 1.20.1</code> (без Optifine)\n\n"
    "📍 <u>Адрес подключения</u>:\n"
    "<code>node4.sunder.su:25700</code>\n\n"
    "📦 <b>Список модов</b>:\n"
    "• <a href=\"https://disk.yandex.com/ВАШ_ИДЕНТИФИКАТОР\">Яндекс Диск</a>\n"
    "• <a href=\"https://drive.google.com/ВАШ_ИДЕНТИФИКАТОР\">Google Диск</a>\n"
    "• <a href=\"https://www.dropbox.com/scl/fi/90e28h0ub2ap77j7zuw5z/ScohWorld.zip?rlkey=t5kygzufaam7qm13pjf354wdp&st=0c9lxodp&dl=0\">Dropbox</a>\n\n"
    "📜 <a href=\"https://telegra.ph/Pravila-ScohWorld-04-06\">Правила сервера</a>"
)

USERS = [1194911765, 7007777856]
