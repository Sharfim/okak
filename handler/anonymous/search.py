from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
#мои модули
from database import Database

db = Database()

def anonymous_message(user:dict)->str:
    return (f"Уникальный ID партнёра: {user['rowid']}\n"
            f"Его анонимное имя: {user['name']}\n\nЕго описание: {user['description']}"
            f"\n\nЕго рейтинг:{user['likes']}👍 {user['dislikes']}👎\
            n\nесли хотите скипнуть напишите стоп")


def search_partner(message, bot: TeleBot):
    user_id = message.from_user.id
    bot.send_message(user_id, "🔍 Ищу собеседника...")

    partners = db.query(
        "SELECT rowid, * FROM users WHERE status = 'searching' AND user_id != ? LIMIT 1",
        (user_id,),
        is_select=True
    )

    if partners:
        partner = partners[0]
        # Соединяем
        db.unification_of_users(user_id, partner['user_id'])

        # Отправляем тебе инфу о партнере
        bot.send_message(user_id, "Партнер найден!\n" + anonymous_message(partner))

        # Берем свои данные. ВАЖНО: убедись, что get_user возвращает словарь!
        me = db.get_user(user_id)
        if me:
            bot.send_message(partner['chat_id'], "Партнер найден!\n" + anonymous_message(me))
    else:
        db.change_status(user_id, "searching")



def stop_search(message, bot: TeleBot):
    user_status = db.get_user(message.from_user.id)['status']

    if user_status == "searching":
        db.query("UPDATE users SET status = 'idle' WHERE user_id = ?", (message.from_user.id,))
        bot.send_message(message.chat.id, "Поиск остановлен")
    else:
        bot.send_message(message.chat.id, "Вы не находитесь в активном поиске")