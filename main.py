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

if __name__ == "__main__":
    manager.create_tables()
    bot.infinity_polling()
