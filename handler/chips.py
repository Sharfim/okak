from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
#мои модули
from database import Database
from handler.import_bot import bot_import

bot = bot_import()
db = Database()

@bot.message_handler(func=lambda message: message.text == "топ по лайкам")
def top_table(message):
    users = db.query("SELECT name, likes FROM users ORDER BY likes DESC LIMIT 10;", is_select=True)

    if users and len(users) >= 3:
        lines = []
        for i, user in enumerate(users, start=1):
            # Извлекаем данные (зависит от того, что возвращает db.query: кортеж или словарь)
            # Если db.query возвращает список кортежей, то: name, likes = user
            name = user[0]
            likes = user[1]
            lines.append(f"{i}: {name} — {likes} 👍")
        
        message_table = "🏆 **Топ пользователей:**\n\n" + "\n".join(lines)
        bot.send_message(message.chat.id, message_table, parse_mode="Markdown")
    else:
        bot.send_message(message.chat.id, "Слишком мало пользователей для топа (нужно хотя бы 3).")
