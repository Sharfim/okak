from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
#мои модули lol
from database import Database, User
from handler.import_bot import bot_import

bot = bot_import()
db = Database()

def anonymous_message(user:User)->str:
    return (f"Уникальный ID партнёра: {user.anonymous_id}\n"
            f"Его анонимное имя: {user.name}\n\nЕго описание: {user.description}"
            f"\n\nЕго рейтинг:{user.likes}👍 {user.dislikes}👎")


@bot.message_handler(func=lambda message: message.text == "Найти собеседника")
def search_partner(message):
    user_id = message.from_user.id
    user: User = db.get_user(user_id)

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text="стоп поиск", callback_data="stop_search"))

    bot.send_message(user_id, "🔍 Ищу собеседника...", reply_markup=markup)

    partners = db.query(
        "SELECT * FROM users WHERE status = 'searching' AND user_id != ? LIMIT 1",
        (user_id,),
        is_select=True
    )

    if partners:
        partner: User = db.get_user(partners[0])
        # Соединяем
        db.unification_of_users(user_id, partner.user_id)

        # Отправляем тебе инфу о партнере
        bot.send_message(user_id, "Партнер найден!\n" + anonymous_message(partner))

        if user:
            bot.send_message(partner.chat_id, "Партнер найден!\n" + anonymous_message(user))
    else:
        db.change_status(user_id, "searching")


@bot.callback_query_handler(func=lambda call: call.data == "stop_search")
def stop_search(message):
    user: User = db.get_user(message.from_user.id)

    if user.is_status("searching"):
        user.update_status("idle")
        bot.send_message(message.chat.id, "Поиск остановлен")
    else:
        bot.send_message(message.chat.id, "Вы не находитесь в активном поиске")
