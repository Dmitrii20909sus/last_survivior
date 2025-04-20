from telebot import TeleBot, types 
import sqlite3
from config import *
import os
import time

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
                             balance REAL DEFAULT 0)
                             """)
    
    def start(self, message):
        user_id = message.chat.id
        username = message.from_user.username or "Anonymous"
        with self.conn:
           cur = self.conn.cursor()
           cur.execute("SELECT * FROM USERS WHERE user_id = ?", (user_id,))
           user = cur.fetchone()
           
           if user is None:
              balance = 0
              cur.execute('''INSERT INTO users (user_id, username, balance) VALUES (?, ?, ?)''', (user_id, username, balance))
              bot.send_message(user_id, "Данный проект был создан Дмитрием Горским и Родионом Кундянок")
              bot.send_message(user_id, "Вступление начинается, подождите немного.")
              bot.send_chat_action(user_id, "upload_video") 
        
              video_path = "C:\\Users\\Admin\\OneDrive\\Desktop\\simulator\\images\\vstuplenie.mp4"
              if os.path.exists(video_path):
               with open(video_path, "rb") as f:
                bot.send_video(user_id, f)

              time.sleep(2)
            
           elif user is not None:
              pass
       

             