import telebot
from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot import types
#мои модули
from database import Database
from .anonymous.chat import stop

db = Database()

def markup_likes_dislikes() -> types.InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("👍", callback_data="add_l_likes"),
        InlineKeyboardButton("👎", callback_data="add_l_dislikes"),
    )
    markup.add(InlineKeyboardButton("пропустить", callback_data="add_l_None"))

    return markup


def likes_dislikes(call, bot: TeleBot):
    partner_id = db.get_user(call.from_user.id)['partner_id']

    if call.data == "add_l_likes":
        db.add_likes_dislikes(partner_id, "likes")
    elif call.data == "add_l_dislikes":
        db.add_likes_dislikes(partner_id, "dislikes")

    bot.edit_message_text("Вы оценили беседу!", call.message.chat.id, call.message.message_id)
    stop(call, bot)

"""def likes_dislikes(call, bot: TeleBot, on_finished=None):
    partner_id = db.get_user(call.from_user.id)['partner_id']

    if call.data == "add_l_likes":
        db.add_likes_dislikes(partner_id, "likes")
    elif call.data == "add_l_dislikes":
        # Тут была опечатка в твоем коде (add_likes_dislikes), исправил
        db.add_likes_dislikes(partner_id, "dislikes")

    bot.edit_message_text("Вы оценили беседу!", call.message.chat.id, call.message.message_id)

    # Если функция передана — вызываем её
    if on_finished:
        on_finished(call, bot)"""