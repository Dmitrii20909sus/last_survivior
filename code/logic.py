from telebot import TeleBot, types 
import sqlite3
from config import *
import os

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
        bot.send_message(message.chat.id, "hello")
        video_path = "C:\\Users\\Admin\\OneDrive\\Desktop\\simulator\\images\\Billy.mp4"
        if os.path.exists(video_path):
         with open(video_path, "rb") as f:
           bot.send_video(message.chat.id, f)

