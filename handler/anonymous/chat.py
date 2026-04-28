import telebot
from telebot import TeleBot
#мои модули
from database import Database, User
from handler import likes_dislikes as l_likes
from handler.import_bot import bot_import

bot = bot_import()
db = Database()

def filters_chat(message):
    return db.get_user(message.from_user.id).is_status("chatting")

def not_filters_chat(message):
    return not filters_chat(message)


@bot.message_handler(func=lambda message: message.text == "стоп" and filters_chat(message))
def stop(message):
    user_id = message.from_user.id
    user = db.get_user(user_id)

    if user and user.is_status("chatting"):
        markup = l_likes.markup_likes_dislikes()

        partner: User = user.get_partner()
        user.update_status("idle")
        partner.update_status("idle")

        bot.send_message(user_id, f"Вы завершили диалог с {partner.name}. Оцените беседу", reply_markup=markup)
        bot.send_message(partner.chat_id, f"Собеседник {user.name} завершил диалог. Оцените беседу", reply_markup=markup)


@bot.message_handler(func=filters_chat)
def anonymous_conversation(message):
    user_id = message.from_user.id
    user = db.get_user(user_id)

    partner: User = user.get_partner()

    if partner:
        try:
            # Исправлено: берем поле 'chat_id' у партнера
            bot.copy_message(chat_id=partner.chat_id, from_chat_id=message.chat.id, message_id=message.message_id)
        except Exception as e:
            print(f"Ошибка при копировании: {e}")
            bot.send_message(user_id, "Не удалось отправить сообщение собеседнику.")


@bot.message_handler(func=not_filters_chat)
def ad_chat(message):
    return bot.send_message(message.chat.id, "Вы не находитесь в чате. Нажмите 'Найти собеседника'.")
#lol
#lol