from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
#мои модули
from database import Database
from handler.import_bot import bot_import

bot = bot_import()
db = Database()


@bot.message_handler(func=lambda message: message.text == "Мой профиль")
def user_profile(message):
    # 1. Получаем данные
    user = db.get_user(message.from_user.id)

    # 4. Формируем кнопки и сообщение
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text="изменить профиль", callback_data="change_profile"))

    # Теперь ошибки TypeError не будет, так как мы проверили profile_info выше
    message_profile = (
        f"твой уникальный id: {user.anonymous_id}\n"
        f"твоё анонимное имя: {user.name}\n"
        f"твоё анонимное описание: {user.description}\n\n"
        f"рейтинг: {user.likes['likes']}👍 {user.dislikes['dislikes']}👎"
    )

    bot.send_message(message.chat.id, message_profile, reply_markup=markup)
    return None


@bot.callback_query_handler(func=lambda call: call.data.startswith("change_profile_"))
def change_profile(call, bot:TeleBot):
    if call.data == "change_profile_":
        markup = InlineKeyboardMarkup()
        markup.add(
            InlineKeyboardButton(text="Никнэйм", callback_data="change_profile_name"),
            InlineKeyboardButton(text="Описание",callback_data="change_profile_description")
        )

        bot.send_message(call.message.chat.id, "что вы хотите изменить?", reply_markup=markup)

    if call.data == "change_profile_name":
        msg = bot.send_message(call.message.chat.id, "напишите своё новое анонимное имя")
        bot.register_next_step_handler(msg, func_change_profile_, bot, "name")

    if call.data == "change_profile_description":
        msg = bot.send_message(call.message.chat.id, "напишите своё новое анонимное описание")
        bot.register_next_step_handler(msg, func_change_profile_, bot, "description")


def func_change_profile_(message, bot:TeleBot, action: str):
    if action == "name":
        db.query("UPDATE users SET name = ? WHERE user_id = ?", (message.text, message.from_user.id))
        bot.send_message(message.chat.id, f"✅ Твоё новое имя: {message.text}")

    if action == "description":
        db.query("UPDATE users SET description = ? WHERE user_id = ?", (message.text, message.from_user.id))
        bot.send_message(message.chat.id, "✅ Описание профиля обновлено!")