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
Модуль для создания заявки
"""

from aiogram import Router, types, F
from aiogram.types import ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from colorama import Fore

from database.check import check_reg, check_adm, check_dbl_nick, get_admin_ids
from database.get_users import update_config_users
from database.upload import upload_db
from keyboards.rules import R1_keyboard, R2_keyboard
from keyboards.otvet_bt import create_otv_keyboard
from utils.msk_time import get_msk_time_now
from classes.form import Form

from config import SERVER_TEXT

start_router = Router(name="start_router")

@start_router.message(Command("start"))
async def get_nickname(message: types.Message):
    """
    Обработчик команды /start
    """
    print(
        "🪴  "
        + Fore.BLUE +
        f"[{get_msk_time_now()}] "
        + Fore.RED +
        f"{message.from_user.id} Использовал команду /start"
        )
    user_id = message.from_user.id

    update_config_users(user_id)

    # Проверка на администратора
    if not await check_adm(int(user_id)):
        # Если это не администратор
        user_entries = await check_reg(user_id)
        if user_entries:  # Если пользователь зарегистрирован (не False)
            state_user = user_entries[0]  # Распаковываем кортеж (status, nickname или что-то ещё)
            if state_user == "Accepted":
                # Если заявка одобрена
                await message.answer(
                    "✅ <b>Ваша заявка</b>\n"
                    "📌 <u>уже принята</u> в системе!\n\n"
                    f"{SERVER_TEXT}",
                    parse_mode="HTML",
                    reply_markup=ReplyKeyboardRemove()
                )
                return
            elif state_user == "Pending":
                # Если заявка ожидает решения
                await message.answer(
                    "⏳ <b>Ваша заявка</b>\n"
                    "🔄 <u>ожидает решения</u> администратора",
                    parse_mode="HTML",
                    reply_markup=ReplyKeyboardRemove()
                )
                return
            elif state_user == "Rejected":
                # Если заявка отклонена
                await message.answer(
                    "❌ <b>Ваша прошлая заявка отклонена</b>\n"
                    "🔄 <i>Можно подать новую заявку</i>",
                    reply_markup=ReplyKeyboardRemove(),
                    parse_mode="HTML"
                )
            elif state_user == "Banned":
                # Если заявка забанена
                await message.answer(
                    "🔒 <b>Ваша учётная запись заблокирована</b> ⚠️", 
                    reply_markup=ReplyKeyboardRemove(),
                    parse_mode="HTML"
                )
                return
        # Если пользователь не зарегистрирован (user_entries == False)
        sent_message = await message.answer(
            "👋 <b>Здравствуй</b>, <u>многоуважаемый игрок</u>! 🎮\n\n"
            "🤖 Это бот для регистрации на <b>приватный сервер ScohWorld</b> 🌍\n\n"
            "📌 <b>Для регистрации необходимо:</b>\n"
            "✅ <u>Подтвердить согласие</u> с правилами сервера",
            reply_markup=R1_keyboard,
            parse_mode="HTML"
        )
        # Закрепляем сообщение сразу после отправки
        try:
            await message.bot.pin_chat_message(
                chat_id=message.chat.id,
                message_id=sent_message.message_id,
                disable_notification=True  # Отключаем уведомление о закреплении
            )
        except Exception as e: # pylint: disable=broad-exception-caught
            print(f"Не удалось закрепить сообщение: {e}")
    else:
        # Если это администратор
        await message.answer(
            f"👋 <b>Добро пожаловать,</b> <u>{message.from_user.first_name}</u>!\n\n"
            "🛠 <i>Доступные команды админ-панели:</i>\n\n"
            "📨 /otvet - Ответ на заявку\n"
            "📢 /broadcast - Массовая рассылка",
            parse_mode="HTML",
            reply_markup=ReplyKeyboardRemove()
        )

@start_router.callback_query(F.data == "rules_agree")
async def podtverjd(callback_query: types.CallbackQuery, state: FSMContext):
    """
    Обработчик нажатия кнопки
    """
    await callback_query.message.edit_reply_markup(
        reply_markup=R2_keyboard
    )
    # Отправляем сообщение без закрепления
    await callback_query.message.answer(
        "✅ <b>Подтверждение правил ScohWorld</b> принято!\n\n"
        "⛏ Введите ваш <u>Minecraft-ник</u>:\n"
        "<code>(Пример: X0tashiy)</code>",
        reply_markup=ReplyKeyboardRemove(),
        parse_mode="HTML"
    )
    await state.set_state(Form.nickname)

@start_router.message(Form.nickname)
async def update_nickname(message: types.Message, state: FSMContext):
    """
    Обработчик ввода никнейма
    """
    if await check_dbl_nick(message.from_user.id, message.text):
        await message.answer(
            "⛔ <b>Такой ник уже занят</b>!\n\n"
            "📌 <i>Пожалуйста, выберите другой ник</i>",
            reply_markup=ReplyKeyboardRemove(),
            parse_mode="HTML"
        )
        return
    await state.update_data(nickname=message.text)
    await state.set_state(Form.age)
    await message.answer(
        "⛏ <b>Никнейм принят</b>!\n\n"
        "🎂 Введите ваш <b>возраст</b>:\n"
        "<code>(Пример: 17)</code>",
        reply_markup=ReplyKeyboardRemove(),
        parse_mode="HTML"
    )

@start_router.message(Form.age)
async def update_age(message: types.Message, state: FSMContext):
    """
    Обработчик ввода информации
    """
    if not message.text.isdigit():
        await message.answer(
            "⛔ <b>Некорректное значение</b>!\n\n"
            "📌 <i>Пожалуйста, введите число</i>",
            reply_markup=ReplyKeyboardRemove(),
            parse_mode="HTML"
        )
        return
    await state.update_data(age=message.text)
    await state.set_state(Form.yznali)
    await message.answer(
        "✅ <b>Возраст принят</b>\n\n"
        "🌐 <b>Введите откуда вы узнали о проекте:</b>\n"
        "<code>(Пример: Twich/TikTok/Youtube/Telegram)</code>",
        reply_markup=ReplyKeyboardRemove(),
        parse_mode="HTML"
    )

@start_router.message(Form.yznali)
async def update_yznali(message: types.Message, state: FSMContext):
    """
    Обработчик информации для создания и отправки заявки
    """
    await state.update_data(yznali=message.text)

    data_form = await state.get_data()

    apl_id = await check_reg(message.from_user.id)
    if apl_id:
        apl_id = apl_id[1] + 1
    else:
        apl_id = 1

    new_user = {
        "username_tg": message.from_user.username,
        "user_nick": data_form.get("nickname"),
        "user_age": data_form.get("age"),
        "date": get_msk_time_now(),
        "user_yznali": data_form.get("yznali"),
        "state": "Pending",  # Устанавливаем начальный статус заявки
    }

    await upload_db(
        message.from_user.id,
        apl_id,
        message.from_user.username,
        message.from_user.full_name,
        data_form.get("age"),
        get_msk_time_now(),
        data_form.get("yznali"),
        data_form.get("nickname"),
        "Pending"
    )

    otv_keyboard = create_otv_keyboard(message.from_user.id)
    adm = await get_admin_ids()
    if adm:
        try:
            for admin_id in adm:
                await message.bot.send_message(
                    admin_id,
                    f"🔔 <b>Новая анкета создана:</b>\n"
                    f"🆔 <b>ID:</b> <code> {message.from_user.id} </code>\n"
                    f"💾 <b>Тг ник:</b> {message.from_user.full_name}\n"
                    f"💾 <b>Тг тег:</b> @{message.from_user.username}\n"
                    "\n"
                    f"📛 <b>Майнкрафт ник:</b> {new_user.get('user_nick')}\n"
                    f"👶 <b>Возраст:</b> {new_user.get('user_age')}\n"
                    f"📝 <b>Ответ на вопрос:</b>\n{new_user.get('user_yznali')}",
                    parse_mode="HTML",
                    reply_markup=otv_keyboard
                )
                # Отправляем по ID игрока
        except Exception as e: # pylint: disable=broad-exception-caught
            print(
                Fore.YELLOW +
                f"Не удалось отправить сообщение администратору {admin_id}.\nОшибка: {e}"
                )
    else:
        print(
            "🚫 " +
            Fore.YELLOW + "К сожалению, " +
            Fore.RED + "у вас нет администраторов!"
        )


    await message.answer(
        "🎉 <b>Заявка успешно создана!</b> ✅\n\n"
        "⏳ <i>Ожидайте обратной связи в ближайшее время</i>",
        reply_markup=ReplyKeyboardRemove(),
        parse_mode="HTML"
    )

    # Очищаем состояние
    await state.clear()
