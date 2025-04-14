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
Создание кнопок для команды /otvet
"""

from aiogram import types
# Создаем кнопки

def create_otv_keyboard(user_id):
    """
    Функция для создания отдельной клавиатуры для каждого пользователя
    """
    accept_button = types.InlineKeyboardButton(
        text="✅ Принять",
        callback_data=f"accept_{user_id}"
    )
    reject_button = types.InlineKeyboardButton(
        text="❌ Отклонить",
        callback_data=f"reject_{user_id}"
    )
    ban_button = types.InlineKeyboardButton(
        text="⛔ Забанить",
        callback_data=f"ban_{user_id}"
    )
    # Создаем клавиатуру
    otv_keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[[accept_button, reject_button, ban_button]]
    )
    return otv_keyboard
