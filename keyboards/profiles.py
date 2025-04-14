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
Создание кнопок для команды /profile
"""

from aiogram import types

# Создаем кнопки

svoy_button = types.InlineKeyboardButton(
    text="👤 Узнать свой профиль",
    callback_data="sv_profilee"
)
chyzoy_button = types.InlineKeyboardButton(
    text="🕵️ Просмотреть другой профиль",
    callback_data="ch_profilee"
)

# Создаем клавиатуру

Pr_keyboard = types.InlineKeyboardMarkup(
    inline_keyboard=[[svoy_button, chyzoy_button]]
)
