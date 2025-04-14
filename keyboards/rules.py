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
Создание кнопок для команды /rules
"""

from aiogram import types

# Создаем кнопки

link_button = types.InlineKeyboardButton(
    text="Ознакомиться с правилами",
    url="https://telegra.ph/Pravila-ScohWorld-04-06"
)
action_button = types.InlineKeyboardButton(
    text="Прочитал и согласен",
    callback_data="rules_agree"
)

# Создаем клавиатуру

R1_keyboard = types.InlineKeyboardMarkup(
    inline_keyboard=[[link_button, action_button]]
)

R2_keyboard = types.InlineKeyboardMarkup(
    inline_keyboard=[[link_button]]
)
