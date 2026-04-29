import telebot
from config import load_evn
token = load_evn()
bot = telebot.TeleBot(token)