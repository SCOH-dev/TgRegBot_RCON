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
Взаимодействие с консолью майнкрафта через RCON
"""

from aiomcrcon import Client
from config import RCON_HOST, RCON_PORT, RCON_PASSWORD

async def wl_add(name):
    """
    Добавления игрока в белый список

    Аргументы: 
        name - ник игрока
    """
    async with Client(RCON_HOST, RCON_PORT, RCON_PASSWORD) as client:
        command = f"simplewl add {name}"
        response = await client.send_cmd(command)
        print(response)
