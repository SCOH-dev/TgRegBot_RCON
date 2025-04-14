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
Модуль для обработки ответов на заявки
Содержит обрабочкик callback-кнопок
"""

from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardRemove
from colorama import Fore

from config import SERVER_TEXT
from database.upload import update_db
from database.check import check_reg, import_db, check_adm, get_admin_ids
from keyboards.otvet_bt import create_otv_keyboard
from utils.rcon_use import wl_add
from utils.msk_time import get_msk_time_now
from classes.otvet_st import Otvet

otvet_router = Router(name="otvet_router")

@otvet_router.message(Command("otvet"))
async def otvet(message: types.Message, state: FSMContext):
    """
    Обработчик команды /otvet
    """
    print(
        "👷  " 
        + Fore.BLUE +
        f"[{get_msk_time_now()}] "
        + Fore.YELLOW +
        f"{message.from_user.id} Использовал команду /otvet"
        )
    user_id = message.from_user.id
    if not await check_adm(user_id):
        await message.answer(
            "⛔ <b>Доступ запрещён</b>", 
            reply_markup=ReplyKeyboardRemove(),
            parse_mode="HTML"
        )
        return
    else:
        await message.answer(
            "🆔 <b>Введите ID игрока</b>\n"
            "📤 <i>Чтобы ответить на его заявку</i>\n\n"
            "<code>(пример: 12345678910)</code>",
            reply_markup=ReplyKeyboardRemove(),
            parse_mode="HTML"
        )
        await state.set_state(Otvet.Us_id)


@otvet_router.message(Otvet.Us_id)
async def get_id(message: types.Message, state: FSMContext):
    """
    Получение ID игрока
    Отправка ему сообщения с взаимодействием
    """
    user_id = message.text.strip()

    if not user_id.isdigit():
        await message.answer(
            "ID игрока должен быть числом. Попробуйте снова.", 
            reply_markup=ReplyKeyboardRemove()
            )
        await state.clear()
        return

    user_id = int(user_id)
    last_application_id = await check_reg(user_id)[1]

    if not last_application_id:
        await message.answer(
            "❌ <b>У пользователя не найдена ни одна заявка</b>",
            reply_markup=ReplyKeyboardRemove(),
            parse_mode="HTML"
        )
        return

    # Сохраняем данные о пользователе и заявке в состояние
    await state.update_data(Us_id=user_id, App_id=last_application_id)
    await message.reply(
        f"🛠️ <b>Управление заявкой #<code>{user_id}</code></b>\n"
        "🔍 Выберите действие:",
        reply_markup=create_otv_keyboard(user_id),
        parse_mode="HTML"
    )
    await state.clear()

# Обработчики нажатия кнопок

@otvet_router.callback_query(lambda c: c.data.startswith("accept_"))
async def accept_b(callback_query: types.CallbackQuery):
    """
    Обработчик кнопки для изменения стастуза анкеты

    Кнопка принятия участника
    """
    user_id = int(callback_query.data.split("_")[1])
    await accept_status(user_id, callback_query)

@otvet_router.callback_query(lambda c: c.data.startswith("reject_"))
async def reject_b(callback_query: types.CallbackQuery):
    """
    Обработчик кнопки для изменения стастуза анкеты

    Кнопка отклонения участника
    """
    user_id = int(callback_query.data.split("_")[1])
    await reject_status(user_id, callback_query)

@otvet_router.callback_query(lambda c: c.data.startswith("ban_"))
async def ban_b(callback_query: types.CallbackQuery):
    """
    Обработчик кнопки для изменения стастуза анкеты

    Кнопка блокировки участника
    """
    user_id = int(callback_query.data.split("_")[1])
    await ban_status(user_id, callback_query)



async def accept_status(user_id, callback_query):
    """
    Изменение статуса заявки на 
    Accepted
    """
    state = await check_reg(user_id)

    if state[0] == "Pending":
        await update_db(user_id, "Accepted")

        aplic = await import_db(user_id)

        if aplic:
            try:
                await wl_add(aplic[7])
                await callback_query.message.bot.send_message(
                    callback_query.from_user.id,
                    "✅ <b>Успешное добавление в вайтлист!</b>\n\n"
                    f"🎮 <i>Игрок:</i> <code>{aplic[7]}</code>",
                    parse_mode="HTML"
                )
            except Exception as e: # pylint: disable=broad-exception-caught
                print(f"Не удалось добавить пользователя в белый список через RCON: {e}")

            try:
                await callback_query.message.bot.send_message(
                    user_id,
                    "🎉 <b>Уважаемый игрок</b>,\n"
                    "✅ <u>Ваша анкета принята</u>!\n\n"
                    f"{SERVER_TEXT}",
                    parse_mode="HTML"
                )
                try:
                    admins = await get_admin_ids()
                    for ids in admins:
                        await callback_query.message.bot.send_message(
                            ids,
                            f"👤 <b>Заявка #<code>{user_id}</code></b>\n"
                            "🟢 <u>Принята</u>!\n\n"
                            "<tg-spoiler>👤 Доступ к серверу предоставлен</tg-spoiler>",
                            parse_mode="HTML"
                        )
                except Exception as e: # pylint: disable=broad-exception-caught
                    print(f"Не удалось отправить сообщение админу {ids}: {e}")
            except Exception as e: # pylint: disable=broad-exception-caught
                print(f"Не удалось отправить сообщение пользователю {user_id}: {e}")
        else:
            await callback_query.message.bot.send_message("Ошибка, Заявки нет")
    else:
        await callback_query.message.bot.send_message(
            callback_query.from_user.id,
            "🔻Ошибка\n\n"
            f"🫰 Статус последней заявки: <b>{state[0]}</b>",
            parse_mode="HTML"
            )

async def reject_status(user_id, callback_query):
    """
    Изменение статуса заявки на 
    Rejected
    """
    state = await check_reg(user_id)

    if state[0] == "Pending":
        await update_db(user_id, "Rejected")

        try:
            await callback_query.message.bot.send_message(
                user_id,
                "❌ <b>Уважаемый игрок</b>,\n"
                "⚠️ <u>Ваша анкета отклонена</u>!\n\n"
                "<tg-spoiler>📝 Вы можете:\n"
                "• Подать заявку повторно</tg-spoiler>",
                parse_mode="HTML"
            )
            try:
                admins = await get_admin_ids()
                for ids in admins:
                    await callback_query.message.bot.send_message(
                        ids,
                        f"👤 <b>Заявка #<code>{user_id}</code></b>\n"
                        "🔻 <i>Отклонена</i>!\n\n"
                        "<tg-spoiler>✅ Пользователь может "
                        "создавать новую заявку</tg-spoiler>",
                        parse_mode="HTML"
                    )
            except Exception as e: # pylint: disable=broad-exception-caught
                print(f"Не удалось отправить сообщение админу {ids}: {e}")
        except Exception as e: # pylint: disable=broad-exception-caught
            print(f"Не удалось отправить сообщение пользователю {user_id}: {e}")
    else:
        await callback_query.message.bot.send_message(
            callback_query.from_user.id,
            "🔻Ошибка\n\n"
            f"🫰 Статус последней заявки: <b>{state[0]}</b>",
            parse_mode="HTML"
            )
        return

async def ban_status(user_id, callback_query):
    """
    Изменение статуса заявки на 
    Banned
    """
    state = await check_reg(user_id)

    if state[0] == "Pending":
        await update_db(user_id, "Banned")


        try:
            await callback_query.message.bot.send_message(
                user_id,
                "🔒 <b>Уважаемый игрок</b>,\n"
                "⚠️ <u>Ваша аккаунт заблокирован</u>!",
                parse_mode="HTML"
            )
            try:
                admins = await get_admin_ids()
                for ids in admins:
                    await callback_query.message.bot.send_message(
                        ids,
                        f"👤 <b>Заявка #<code>{user_id}</code></b>\n"
                        "🚫 <i>заблокирована</i>!\n\n"
                        "<tg-spoiler>🔒 Пользователь не может "
                        "создавать новые заявки</tg-spoiler>",
                        parse_mode="HTML"
                    )
            except Exception as e: # pylint: disable=broad-exception-caught
                print(f"Не удалось отправить сообщение админу {ids}: {e}")
        except Exception as e: # pylint: disable=broad-exception-caught
            print(f"Не удалось отправить сообщение пользователю {user_id}: {e}")
    else:
        await callback_query.message.bot.send_message(
            callback_query.from_user.id,
            "🔻Ошибка\n\n"
            f"🫰 Статус последней заявки: <b>{state[0]}</b>",
            parse_mode="HTML"
            )
        return
