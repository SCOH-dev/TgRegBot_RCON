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
Модуль для массовой рассылки сообщений 
активным пользователям
"""

from aiogram import Router, types
from aiogram.types import ReplyKeyboardRemove
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from colorama import Fore

from config import USERS
from utils.msk_time import get_msk_time_now
from database.check import check_adm

broadcast_router = Router(name="broadcast_router")

# Объявляем класс состояний
class BroadcastStates(StatesGroup):
    """
    Класс состояний для массовой рассылки
    """
    waiting_for_message = State()


@broadcast_router.message(Command("broadcast"))
async def start_broadcast(message: types.Message, state: FSMContext):
    """
    Команда для начала массовой рассылки. Доступно только администраторам.
    """
    print(
        "📚  "
        + Fore.BLUE +
        f"[{get_msk_time_now()}] "
        + Fore.RED +
        f"{message.from_user.id} Использовал команду /broadcast"
    )
    if not await check_adm(int(message.from_user.id)):
        await message.answer(
            "⛔ <b>Доступ запрещён</b>", 
            reply_markup=ReplyKeyboardRemove(),
            parse_mode="HTML"
            )
        return

    await message.answer(
        "📩 <b>Создание массовой рассылки</b>\n\n"
        "✨ <i>Введите текст сообщения</i>\n"
        "🛠️ Доступно <u>HTML-форматирование</u>\n"
        "<code>Пример:\\n<b>Заголовок</b>\\nНовая строка</code>\n\n"
        "📌 Используйте \\n для переноса строки",
        reply_markup=ReplyKeyboardRemove(),
        parse_mode="HTML"
    )
    await state.set_state(BroadcastStates.waiting_for_message)  # Устанавливаем состояние


@broadcast_router.message(StateFilter(BroadcastStates.waiting_for_message))
async def send_broadcast(message: types.Message, state: FSMContext):
    """
    Отправляет сообщение всем пользователям из базы данных.
    """
    # Убираем состояние после получения текста для рассылки
    await state.clear()

    broadcast_text = message.text

    if not USERS:
        await message.answer(
            "🗄️ <b>База данных пуста</b> ℹ️\n\n"
            "📭 <i>Нет зарегистрированных пользователей</i>",
            reply_markup=ReplyKeyboardRemove(),
            parse_mode="HTML"
            )
        return

    success_count = 0
    fail_count = 0

    for user_id in USERS:
        try:
            await message.bot.send_message(
                chat_id=user_id,
                text=broadcast_text,
                parse_mode="HTML"
            )
            success_count += 1
        except Exception as e: # pylint: disable=broad-exception-caught
            print(f"Не удалось отправить сообщение пользователю {user_id}. Ошибка: {e}")
            fail_count += 1

    # Уведомляем администратора о результате рассылки
    await message.answer(
        "📨 <b>Результат рассылки:</b>\n\n"
        f"✅ <u>Успешно</u>: <code>{success_count}</code> пользователей.\n"
        f"❌ Не удалось отправить {fail_count} пользователям.\n",
        reply_markup=ReplyKeyboardRemove(),
        parse_mode="HTML"
    )
