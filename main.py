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
Создание бота
"""
import asyncio
from colorama import Fore, init
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from utils.commands import set_commands, set_adm_commands
from database.create import create_db
from database.check import get_admin_ids
from handlers import routers

from config import TG_TOKEN, USERS

init(autoreset=True)

async def do_router(dp: Dispatcher) -> None:
    """
    Объявление роутеров
    """
    for router in routers:
        print(Fore.MAGENTA + f"⚖️  Объявил роутер {router.name}!")
        dp.include_router(router)

async def on_startup(bot: Bot) -> None:
    """
    Функция при запуске бота
    """
    print(Fore.GREEN + "👷‍ Бот запущен!")

    await create_db()
    print(Fore.GREEN + "✅ База данных создана!")

    print(Fore.YELLOW + "⌛ Установка команд для обычных пользователей")
    try:
        for user in USERS:
            await set_commands(bot, user)
            print(Fore.GREEN + f"⚡ Команды для пользователя {user} установлены!")
    except Exception as e: # pylint: disable=broad-exception-caught
        print(Fore.RED + f"‼️ Ошибка установки команд: {e}")

    try:
        admins = await get_admin_ids()
        for admin_id in admins:
            await set_adm_commands(bot, admin_id)
            print(Fore.GREEN + f"⚡ Команды для админа {admin_id} установлены!")
    except Exception as e: # pylint: disable=broad-exception-caught
        print(Fore.RED + f"‼️ Ошибка установки команд: {e}")

    print(Fore.GREEN + "🦟 Все команды успешно созданы!")

async def on_shutdown(bot: Bot) -> None:
    """
    Функция при завершении работы бота
    """
    print(Fore.RED + "⌛ Завершение работы...")
    try:
        await bot.session.close()  # Просто закрываем сессию без проверки
        print(Fore.YELLOW + "✅ Сессия бота закрыта")
    except Exception as e: # pylint: disable=broad-exception-caught
        print(Fore.RED + f"❌ Ошибка закрытия сессии: {e}")

async def main() -> None:
    """
    Основная функция для запуска бота
    """

    storage = MemoryStorage()
    bot = Bot(token=TG_TOKEN)
    dp = Dispatcher(storage=storage)

    await do_router(dp)
    print(Fore.MAGENTA + "⚖️ Все Роутеры успешно объявлены!")

    # Регистрируем функции запуска и остановки
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    # Запускаем polling
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(Fore.RED + "\n🚫 Работа прервана пользователем")
    except Exception as e: # pylint: disable=broad-exception-caught
        print(Fore.RED + f"‼️ Фатальная ошибка: {e}")
