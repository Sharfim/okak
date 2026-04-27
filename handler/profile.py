from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
#мои модули
from database import Database

db = Database()


def user_profile(message, bot: TeleBot):
    # 1. Получаем данные
    profile_info = db.get_user(message.from_user.id)

    # 2. Если пользователь есть в базе, пробуем достать расширенные данные
    if profile_info:
        storage_info = db.get_user_storage(message.from_user.id, message.chat.id, message.from_user.username)
        # Если storage_info нашелся, используем его, если нет — оставляем основной профиль
        if storage_info:
            profile_info = storage_info

    # 3. КРИТИЧЕСКАЯ ПРОВЕРКА: если профиля всё еще нет в базе
    if not profile_info:
        return bot.send_message(message.chat.id, "❌ Профиль не найден. Введите /start")

    # 4. Формируем кнопки и сообщение
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text="изменить профиль", callback_data="change_profile"))

    # Теперь ошибки TypeError не будет, так как мы проверили profile_info выше
    message_profile = (
        f"твой уникальный id: {profile_info['rowid']}\n"
        f"твоё анонимное имя: {profile_info['name']}\n"
        f"твоё анонимное описание: {profile_info['description']}\n\n"
        f"рейтинг: {profile_info['likes']}👍 {profile_info['dislikes']}👎"
    )

    bot.send_message(message.chat.id, message_profile, reply_markup=markup)
    return None


def change_profile(call, bot:TeleBot):
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(text="Никнэйм", callback_data="change_profile_name"),
        InlineKeyboardButton(text="Описание",callback_data="change_profile_description")
    )

    bot.send_message(call.message.chat.id, "что вы хотите изменить?", reply_markup=markup)


def change_profile_(call, bot:TeleBot):
    if call.data == "change_profile_name":
        msg = bot.send_message(call.message.chat.id, "напишите своё новое анонимное имя")
        bot.register_next_step_handler(msg, func_change_profile_name, bot)

    if call.data == "change_profile_description":
        msg = bot.send_message(call.message.chat.id, "напишите своё новое анонимное описание")
        bot.register_next_step_handler(msg, func_change_profile_description, bot)


def func_change_profile_name(message, bot:TeleBot):
    db.query("UPDATE users SET name = ? WHERE user_id = ?", (message.text, message.from_user.id))
    bot.send_message(message.chat.id, f"✅ Твоё новое имя: {message.text}")


def func_change_profile_description(message, bot:TeleBot):
    db.query("UPDATE users SET description = ? WHERE user_id = ?", (message.text, message.from_user.id))
    bot.send_message(message.chat.id, "✅ Описание профиля обновлено!")