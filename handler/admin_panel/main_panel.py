from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
#мои модули
from database import Database
from handler.import_bot import bot_import
from config import load_json

bot = bot_import()
db = Database()

def is_admin(message):
    return load_json()["admin_id"] == message.chat.id

#@TODO: 243589703289075
@bot.message_handler(func=is_admin)
def main_panel():
    pass