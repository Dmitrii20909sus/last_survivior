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
    if user[13]:  
        return
    if user:
        story = user[7]
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    
        if story == 0:
            markup.add("Профиль", "Начать сюжет")
    
        elif story == 1:
            markup.add("Профиль", "Охота", "Построить дом")
           
        elif story == 2:
            markup.add("Профиль", "Охота", "Построить дом")
            
        elif story == 3:
            markup.add("Профиль", "Охота", "Построить дом", "Путешествие")
           
        elif story == 4:
            markup.add("Профиль", "Охота", "Улучшить дом", "Путешествие")
           
        elif story == 5: 
           markup.add("Профиль", "Охота", "Улучшить дом", "Путешествие", "Продолжить сюжет")
        
        elif story == 6: 
           markup.add("Профиль", "Охота", "Улучшить дом", "Путешествие", "Артефакты")
            
        elif story == 7: 
           markup.add("Профиль", "Охота", "Улучшить дом", "Путешествие", "Артефакты", "Продолжить сюжет")
        
        elif story == 8: 
           markup.add("Профиль", "Охота", "Улучшить дом", "Путешествие", "Артефакты", "Поселение")
        
        elif story == 9: 
           markup.add("Профиль", "Охота", "Улучшить дом", "Путешествие", "Артефакты", "Поселение", "Продолжить сюжет")
        
        elif story == 10: 
           markup.add("Профиль", "Охота", "Улучшить дом", "Путешествие", "Артефакты", "Поселение")

        elif story == 11: 
           markup.add("Профиль", "Охота", "Улучшить дом", "Путешествие", "Артефакты", "Поселение", "Продолжить сюжет")

    
        bot.send_message(user_id, f"Выберете действие:", reply_markup=markup)   

@bot.message_handler(func=lambda message: message.text == "Профиль")
def handle_profile(message):
    manager.profile(message)


@bot.message_handler(func=lambda message: message.text == "Начать сюжет")
def work_keyboard(message):
    user = manager.select_user(message)
    user_id = message.chat.id

    if user:
        story = user[7]
        if story != 0:
            bot.send_message(user_id, f"""Вы уже прошли начало сюжета""")
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
         bot.send_message(user_id, f"""Сначала начните сюжет """)
         

@bot.message_handler(func=lambda message: message.text in ["Построить дом", "Улучшить дом"])
def handle_house(message):
    user_id = message.chat.id
    user = manager.select_user(message)

    if user:
        story = user[7]
        if story >= 2:
         manager.house(message)

@bot.message_handler(func=lambda message: message.text == "Путешествие")
def handle_adventure(message):
    user_id = message.chat.id
    user = manager.select_user(message)

    if user:
        story = user[7]
        if story >= 3:
         manager.adventure(message)

@bot.message_handler(func=lambda message: message.text == "Продолжить сюжет")
def handle_house(message):
    user_id = message.chat.id
    user = manager.select_user(message)

    if user:
        story = user[7]
        if story == 5:
         manager.story_lvl2(message)
        if story == 7:
         manager.story_lvl3(message)
        if story == 9:
         manager.story_lvl4(message)
        if story == 11:
         manager.story_lvl5(message)
        
   
@bot.message_handler(func=lambda message: message.text == "Артефакты")
def show_artifacts(message):
    user_id = message.chat.id
    manager.get_user_artifacts(user_id)

@bot.message_handler(func=lambda message: message.text == "Поселение")
def _population(message):
   manager.population(message)


@bot.callback_query_handler(func=lambda call: True)
def handle_call_back(call):
     call_data = call.data 
     user_id = call.message.chat.id
     try:
         bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None) 
     except Exception:
         pass

     if call.data == "buyNewHouse":
         manager.house_bought(call)
         return
     if call.data == "resqueZolo":
         manager.story_ivan_resqued(call.message)
         return
     if call.data == "LetInZolo":
         manager.story_ivan_let_in(call.message)
         return
     if call.data == "dora":
         manager.story_dora(call.message)
         return
     if call.data == "LetInDora":
         manager.Ivan_Dora_plan(call.message)
         return
     if call.data == "HuntWithZolo":
         manager.hunt_with_zolik(call.message)
         return
     if call.data == "take_weapon":
         manager.zolo_is_dead(call.message)
         return
     if call.data == "stop_dora":
         manager.stop_dora(call.message)
         return
     if call.data == "listen_dora":
         manager.dora_in_prison(call.message)
         return

     if call.data.startswith("send_sticker_profile_"):  
            entire = call.data.split("_")
            call_stick = entire[-1]
            method_name = f"return_sticker_{call_stick}"
            method = getattr(manager, method_name, None)

            if method: 
                method(call) 
            return
     
     if call_data == "WithoutBadWords":
        manager.understand(call)
        return
     if call_data == "WithBadWords":
        manager.understand2(call)
        return

     if call.data == "incest":
        manager.incest(call.message)
        return
     if call.data == "boost_lvl":
        manager.shop(call.message)
        return
     if call.data.startswith("buy_"):
        manager.buy_item(call)
        return
     with manager.conn:     
      cur = manager.conn.cursor()
      cur.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
      user = cur.fetchone()
      if call.data == "understand":
         manager.understand(call)
      if call.data == "head":
         if user[13] == 0:
          return
         call_data = 'Голова'
         cur.execute("UPDATE users SET call_data = ? WHERE user_id = ?", (call_data, user_id))
         manager.handle_zombie(message=call) 
      if call.data == "liver":
         if user[13] == 0:
          return
         call_data = 'Печень'
         cur.execute("UPDATE users SET call_data = ? WHERE user_id = ?", (call_data, user_id))
         manager.handle_zombie(message=call) 
      if call.data == "chest":
         if user[13] == 0:
          return
         call_data = 'Грудь'
         cur.execute("UPDATE users SET call_data = ? WHERE user_id = ?", (call_data, user_id))
         manager.handle_zombie(message=call) 
      if call.data == "leg":
         if user[13] == 0:
          return
         call_data = 'Нога'
         cur.execute("UPDATE users SET call_data = ? WHERE user_id = ?", (call_data, user_id))
         manager.handle_zombie(message=call)          
     
     
    

if __name__ == "__main__":
    manager.create_tables()
    manager.insert_houses()
    manager.insert_population_boosts()
    manager.insert_artifacts()
    bot.remove_webhook()
    bot.infinity_polling()

