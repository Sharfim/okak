from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
#мои модули
from database import Database
from handler import likes_dislikes as l_likes

db = Database()

def stop(message, bot: TeleBot):
    user_id = message.from_user.id
    user = db.get_user(user_id)

    if user and user['status'] == 'chatting':
        markup = l_likes.markup_likes_dislikes()

        partner = db.partner_information(user_id)
        db.change_status(user_id, "idle")
        db.change_status(partner['user_id'], "idle")

        bot.send_message(user_id, f"Вы завершили диалог с {partner['name']}. Оцените беседу", reply_markup=markup)
        bot.send_message(partner['chat_id'], f"Собеседник {user['name']} завершил диалог. Оцените беседу", reply_markup=markup)
    else:
        bot.send_message(user_id, "Вы не находитесь в поиске или чате.")


def anonymous_conversation(message, bot: TeleBot):
    user_id = message.from_user.id
    user_data = db.get_user(user_id)

    if not user_data or user_data['status'] != 'chatting':
        # Если юзер просто пишет в бота вне чата
        return bot.send_message(message.chat.id, "Вы не находитесь в чате. Нажмите 'Найти собеседника'.")

    partner = db.partner_information(user_id)

    if partner:
        try:
            # Исправлено: берем поле 'chat_id' у партнера
            bot.copy_message(chat_id=partner['chat_id'], from_chat_id=message.chat.id, message_id=message.message_id)
        except Exception as e:
            print(f"Ошибка при копировании: {e}")
            bot.send_message(user_id, "Не удалось отправить сообщение собеседнику.")