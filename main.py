import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
#модули
from database import Database
import config
from bot import bot
from handler import profile, likes_dislikes
from handler.anonymous import chat, search

db = Database()


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


if __name__ == "__main__":
    bot.infinity_polling()