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
Модуль для выдачи информации о пользователе
"""

from aiogram import Router, types
from aiogram.types import ReplyKeyboardRemove
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from colorama import Fore

from keyboards.profiles import Pr_keyboard
from database.check import check_reg, import_db, check_adm
from utils.msk_time import get_msk_time_now

profile_router = Router(name="profile_router")

class ProfileStates(StatesGroup):
    """
    Класс для управления состояниями FSM при работе с профилем пользователя.
    """
    waiting_for_id = State()

@profile_router.message(Command("profile"))
async def get_profile(message: types.Message):
    """
    Инициализатор команды /profile
    """
    print(
        "🌟  "
        + Fore.BLUE +
        f"[{get_msk_time_now()}] "
        + Fore.RED +
        f"{message.from_user.id} Использовал команду /profile"
    )
    user_id = message.from_user.id
    if not await check_adm(user_id):
        states = await check_reg(user_id)
        if states is not False:
            data = await import_db(user_id)
            await message.bot.send_message(
                user_id,
                f"👤 <b>Профиль</b> <u>{message.from_user.full_name}</u>\n\n"
                f"🆔 <i>ID:</i> <code>{user_id}</code>\n"
                f"📛 <i>UserName:</i> @{message.from_user.username}\n\n"
                "📅 <u>Регистрация:</u>\n"
                f"<code>{data[5]}</code>\n\n"
                "🎂 <u>Возраст:</u>\n"
                f"<code>{data[4]}</code>\n\n"
                "⛏️ <u>Minecraft-ник:</u>\n"
                f"<code>{data[7]}</code>\n\n"
                "📝 <u>Источник:</u>\n"
                f"<code>{data[6]}</code>\n\n"
                "📊 <u>Статистика:</u>\n"
                f"• Заявок: <code>{data[1]}</code>\n"
                f"• Статус: <code>{data[8]}</code>",
                reply_markup=ReplyKeyboardRemove(),
                parse_mode="HTML"
                )
        else:
            await message.answer(
                f"👤 <b>Профиль</b> <u>{message.from_user.full_name}</u>\n\n"
                f"🆔 <i>ID:</i> <code>{user_id}</code>\n"
                f"📛 <i>UserName:</i> @{message.from_user.username}\n\n"
                "📊 <u>Статистика:</u>\n"
                "• Заявок: <code>0</code>\n"
                "• Статус: <code>None</code>", 
                reply_markup=ReplyKeyboardRemove(),
                parse_mode="HTML"
                )
    else:
        await message.answer(
            "🔍 <b>Выберите действие:</b>\n\n"
            "👤 Узнать свой профиль\n"
            "🕵️ Просмотреть другой профиль", 
            reply_markup=Pr_keyboard,
            parse_mode="HTML"
            )

@profile_router.callback_query(lambda c: c.data == "ch_profilee")
async def process_ch_profile(callback_query: types.CallbackQuery, state: FSMContext):
    """
    Обработчик нажатия кнопки "🕵️ Просмотреть другой профиль"
    """
    await callback_query.message.answer("🕵️ Введи ID пользователя:")
    # Устанавливаем состояние ожидания ID
    await state.set_state(ProfileStates.waiting_for_id)
    await callback_query.answer()

@profile_router.message(ProfileStates.waiting_for_id)
async def process_user_id_input(message: types.Message, state: FSMContext):
    """
    Обработчик ввода ID пользователя 
    """
    try:
        target_id = message.text  # Пробуем превратить текст в число
        # Здесь можно добавить логику проверки и вывода профиля
        data = await import_db(target_id)
        await message.answer(
                f"👤 <b>Профиль</b> <u>{data[3]}</u>\n\n"
                f"🆔 <i>ID:</i> <code>{target_id}</code>\n"
                f"📛 <i>UserName:</i> @{data[2]}\n\n"
                "📅 <u>Регистрация:</u>\n"
                f"<code>{data[5]}</code>\n\n"
                "🎂 <u>Возраст:</u>\n"
                f"<code>{data[4]}</code>\n\n"
                "⛏️ <u>Minecraft-ник:</u>\n"
                f"<code>{data[7]}</code>\n\n"
                "📝 <u>Источник:</u>\n"
                f"<code>{data[6]}</code>\n\n"
                "📊 <u>Статистика:</u>\n"
                f"• Заявок: <code>{data[1]}</code>\n"
                f"• Статус: <code>{data[8]}</code>",
                reply_markup=ReplyKeyboardRemove(),
                parse_mode="HTML"
                )
    except ValueError:
        await message.answer("❌ Введи нормальный числовой ID!")
    finally:
        # Сбрасываем состояние, чтобы бот не ждал ID дальше
        await state.clear()

@profile_router.callback_query(lambda c: c.data == "sv_profilee")
async def process_sv_profile(callback_query: types.CallbackQuery):
    """
    Обработчик нажатия кнопки "👤 Узнать свой профиль"
    """
    try:
        data = await import_db(callback_query.from_user.id)
        await callback_query.answer(
                f"👤 <b>Профиль</b> <u>{data[3]}</u>\n\n"
                f"🆔 <i>ID:</i> <code>{callback_query.from_user.id}</code>\n"
                f"📛 <i>UserName:</i> @{data[2]}\n\n"
                "📅 <u>Регистрация:</u>\n"
                f"<code>{data[5]}</code>\n\n"
                "🎂 <u>Возраст:</u>\n"
                f"<code>{data[4]}</code>\n\n"
                "⛏️ <u>Minecraft-ник:</u>\n"
                f"<code>{data[7]}</code>\n\n"
                "📝 <u>Источник:</u>\n"
                f"<code>{data[6]}</code>\n\n"
                "📊 <u>Статистика:</u>\n"
                f"• Заявок: <code>{data[1]}</code>\n"
                f"• Статус: <code>{data[8]}</code>",
                reply_markup=ReplyKeyboardRemove(),
                parse_mode="HTML"
                )
    except Exception as e: # pylint: disable=broad-exception-caught
        print(
                Fore.YELLOW +
                f"Ошибка: {e}"
        )
