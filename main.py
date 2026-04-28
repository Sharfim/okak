import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

# 1. Сначала база и бот
from database import Database
from bot import bot

# 2. Импортируем модули с хендлерами (они сами привяжутся к bot через декораторы)
from handler import profile, likes_dislikes
from handler.anonymous import search
# Важно: chat импортируем последним, так как там хендлер "на всё подряд"
from handler.anonymous import chat 

db = Database()

def start_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("Мой профиль"))
    markup.add(KeyboardButton("Найти собеседника"), KeyboardButton("Найти собеседника по ID"))
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    db.get_user_storage(message.from_user.id, message.chat.id, message.from_user.username)
    markup = start_markup()
    bot.send_message(message.chat.id, "Привет! Это аноним чат бот!", reply_markup=markup)

if __name__ == "__main__":
    print("Бот запущен...")
    bot.infinity_polling()
