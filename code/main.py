from logic import *
from config import *
from telebot import TeleBot, types
import sqlite3
import os

bot = TeleBot(token)
manager = DB_Manager(database)

@bot.message_handler(commands=['start'])
def start_command(message):
    manager.start(message)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Профиль", "Работа")
    bot.send_message(message.chat.id, f"""Выберете действие:
    """, reply_markup=markup)

if __name__ == "__main__":
    manager.create_tables()
    bot.infinity_polling()
