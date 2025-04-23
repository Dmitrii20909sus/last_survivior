from logic import *
from config import *
from telebot import TeleBot, types
import sqlite3
import os

bot = TeleBot(token)
manager = DB_Manager(database)

@bot.message_handler(commands=['start'])
def start_command(message):
    user_id = message.chat.id
    manager.start(message)

    user = manager.select_user(message)

    if user:
        story = user[7]
        if story == 0:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add("Профиль", "Начать сюжет")
            bot.send_message(user_id, f"""Выберете действие:
            """, reply_markup=markup)
        if story == 1:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add("Профиль", "Охота")
            bot.send_message(user_id, f"""Выберете действие:
            """, reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "Начать сюжет")
def work_keyboard(message):
    user = manager.select_user(message)
    user_id = message.chat.id

    if user:
        story = user[7]
        if story != 0:
            bot.send_message(user_id, f"""Вы уже прошли начало сюжета  """)
        elif story == 0:
          manager.story_0(message)

@bot.message_handler(func=lambda message: message.text == "Охота")
def handle_hunt(message):
    user_id = message.chat.id
    user = manager.select_user(message)

    if user:
        story = user[7]
        if story >= 1:
         manager.hunt(message)
        else: 
         bot.send_message(user_id, f"""Сначала начните сюжет """, )
         

@bot.message_handler(func=lambda message: message.text == "Построить дом")
def handle_house(message):
    user_id = message.chat.id
    user = manager.select_user(message)

    if user:
        story = user[7]
        if story >= 2:
         manager.house(message)

    

if __name__ == "__main__":
    manager.create_tables()
    manager.insert_houses()
    bot.infinity_polling()
