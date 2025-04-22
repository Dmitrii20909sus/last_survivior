from telebot import TeleBot, types 
import sqlite3
from config import *
import os
import time
from datetime import datetime, timedelta

bot = TeleBot(token)

class DB_Manager:
    def __init__(self, database):
        self.database = database
        self.conn = sqlite3.connect(self.database, check_same_thread=False)
    
    def create_tables(self):
        with self.conn:
            self.conn.execute("""CREATE TABLE IF NOT EXISTS users(
                             id INTEGER PRIMARY KEY,
                             username TEXT,
                             user_id TEXT UNIQUE,
                             gold INTEGER DEFAULT 0,
                             wood INTEGER DEFAULT 0,
                             stone INTEGER DEFAULT 0,
                             story INTEGER DEFAULT 0)
                             """)
    def select_user(self, message):
       user_id = message.chat.id
       with self.conn:
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM USERS WHERE user_id = ?", (user_id,))
        user = cur.fetchone()
       return user

    def start(self, message):
        user_id = message.chat.id
        username = message.from_user.username or "Anonymous"
        with self.conn:
           cur = self.conn.cursor()
           cur.execute("SELECT * FROM USERS WHERE user_id = ?", (user_id,))
           user = cur.fetchone()
           
           if user is None:
              gold = 0
              wood = 0
              stone = 0
              story = 0
              cur.execute('''INSERT INTO users (user_id, username, gold, wood, stone, story) VALUES (?, ?, ?, ?, ?, ?)''', (user_id, username, gold, wood, stone, story))
              bot.send_message(user_id, "Данный проект был создан Дмитрием Горским и Родионом Кундянок")
              video_path = "C:\\Users\\Admin\\OneDrive\\Desktop\\simulator\\images\\vstuplenie.mp4"
              bot.send_message(user_id, "Вступление загружается, подождите немного.")
              bot.send_chat_action(user_id, "upload_video")
            
              time.sleep(1.5)
    
              if os.path.exists(video_path):
               with open(video_path, "rb") as f:
                bot.send_video(user_id, f, timeout=120)
              else:
               bot.send_message(user_id, "Видео не найдено. Короче без вступления :(") 
        
              time.sleep(2)
            
           elif user is not None:
              pass

    def story_0(self, message):
       
       user_id = message.chat.id
       user = self.select_user(message)
       bot.send_message(user_id, """*Бог:* Здравствуй, сын мой божий. 
                        Ты один из единственных, кому удалось пережить
                        это несчастье.""", parse_mode="Markdown")
       time.sleep(2.5)
       bot.send_message(user_id,"""*Бог:* Ну что-же, для начала награжу ка 
                        я тебя как избранного ресурсами, в которых ты сейчас
                        очень нуждаешься, держи 10 кусочков золота🏅, 20 кусков 
                        дерева🪵 и 20 камней🪨, с ними ты сможешь построй 
                        свой первый дом""", parse_mode="Markdown") 
       time.sleep(2)
       with self.conn:
          cur = self.conn.cursor()
          cur.execute("""
            UPDATE users SET gold = gold + 10, wood = wood + 20, stone = stone + 20, story = 1 
            WHERE user_id = ?
        """, (user_id,))    
       bot.send_message(user_id, "<i>Вам зачисленно:</i> +20🏅, +20🪵, +20🪨", parse_mode="HTML")  
      
       bot.send_message(user_id, """*Бог:* Скоро ты построишь себе новый дом,
                        но сначала, иди ка ты на охоту, 
                        ты очень голодный, тебе стоило бы поесть, 
                        поэтому нажми в меню на кнопку *Охота*, 
                        чтобы добыть еды""", parse_mode="Markdown")
       # Ich soll den Markdown Ohota erstellen und dort  2 bis 5 Tiere jagen,
       # jedes Tier gibt mir bestimmte Anzahl an Punkten die dann alle 
       # zusammen summiert werden ---> noch eine Tabelle erstellen (Zweri)
       #Er soll ungefähr so aussehen:
       #Ihre Beute:
       # () Krolikov
       # () Volkov
       # () Kasul
       # ...
       # Ich soll außerdem ein cooldown für die Jagd erstellen
       # Ich muss den Gottes Text an die richtigen Zeilen setzen
       # Profil soll auch angezeigt werden
       

             

              

                

