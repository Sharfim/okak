import telebot
import config

CONFIG = config.load_json()
bot = telebot.TeleBot(CONFIG["api_token"])