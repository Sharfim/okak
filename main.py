import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
#модули
from database import Database
import config
from handler import profile, likes_dislikes
from handler.anonymous import chat, search

db = Database()
db.create_table()
CONFIG = config.load_json()

bot = telebot.TeleBot(CONFIG["api_token"])


def start_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("Мой профиль"))
    markup.add(KeyboardButton("Найти собеседника"), KeyboardButton("Найти собеседника по ID"))

    return markup


@bot.message_handler(commands=['start'])
def start(message):
    db.get_user_storage(message.from_user.id, message.chat.id, message.from_user.username)
    markup=start_markup()

    bot.send_message(message.chat.id, "Привет! Это аноним чат бот!", reply_markup=markup)


#раздел профиля
@bot.message_handler(func=lambda message: message.text == "Мой профиль")
def user_profile(message):
    profile.user_profile(message, bot)


@bot.callback_query_handler(func=lambda call: call.data.startswith("change_profile_"))
def change_profile_(call):
    profile.change_profile_(call, bot)



#раздел найти собеседника
@bot.message_handler(func=lambda message: message.text == "Найти собеседника")
def search_partner(message):
    search.search_partner(message, bot)


@bot.callback_query_handler(func=lambda call: call.data == "stop_search")
def stop_search(message):
    search.stop_search(message, bot)


@bot.message_handler(func=lambda message: message.text == "стоп")
def evaluation_message(message):
    chat.stop(message, bot)


@bot.callback_query_handler(func=lambda call: call.data.startswith("add_l_"))
def handle_likes(call): # Даем другое имя
    likes_dislikes.likes_dislikes(call, bot) # Теперь модуль вызывается правильно


@bot.message_handler(func=lambda message: True)
def anonymous_conversation(message):
    chat.anonymous_conversation(message, bot)


bot.infinity_polling()