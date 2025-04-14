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
Создание команд для участников
"""

from aiogram.types import BotCommand, BotCommandScopeChat, BotCommandScopeAllPrivateChats

async def set_commands(bot, user_id = None):
    """
    Создание команд для пользователей
    """
    commands = [
        BotCommand(command="/start", description="Начать регистрацию"),
        BotCommand(command="/profile", description="Просмотреть свой профиль"),
        BotCommand(command="/help", description="soon..."),
    ]
    if user_id:
        await bot.delete_my_commands(scope=BotCommandScopeChat(chat_id=user_id))
        await bot.set_my_commands(commands, scope=BotCommandScopeChat(chat_id=user_id))
    else:
        await bot.delete_my_commands(scope=BotCommandScopeAllPrivateChats())
        await bot.set_my_commands(commands)



async def set_adm_commands(bot, admin_id):
    """
    Создание команд для админов
    """
    commands = [
        BotCommand(command="/start", description="Начать регистрацию"),
        BotCommand(command="/help", description="soon..."),
        BotCommand(command="/otvet", description="Ответить пользователю по анкете"),
        BotCommand(command="/broadcast", description="Рассылка сообщения всем пользователям"),
        BotCommand(command="/profile", description="Просмотреть свой профиль"),
    ]
    await bot.delete_my_commands(scope=BotCommandScopeAllPrivateChats())
    await bot.set_my_commands(commands, scope=BotCommandScopeChat(chat_id=admin_id))
