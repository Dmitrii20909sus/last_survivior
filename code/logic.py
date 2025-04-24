from telebot import TeleBot, types 
import sqlite3
from config import *
import os
import time
import random
from datetime import datetime, timedelta

bot = TeleBot(token)

class DB_Manager:
    def __init__(self, database):
        self.database = database
        self.conn = sqlite3.connect(self.database, check_same_thread=False)
    
        self.animals = {
            "🐇 Заяц": 5,
            "🦊 Лиса": 8,
            "🦌 Косуля": 10,
            "🐺 Волк": 15,
            "🐗 Кабан": 20,
            "🐻 Медведь": 30
                        }
        
        self.results = {animal: 0 for animal in self.animals}

    def create_tables(self):
        with self.conn:
            self.conn.execute("""CREATE TABLE IF NOT EXISTS users(
                             id INTEGER PRIMARY KEY,
                             username TEXT,
                             user_id TEXT UNIQUE,
                             food INTEGER DEFAULT 0,
                             gold INTEGER DEFAULT 0,
                             wood INTEGER DEFAULT 0,
                             stone INTEGER DEFAULT 0,
                             story INTEGER DEFAULT 0,
                             last_hunt_time REAL DEFAULT 0,
                             house_lvl INTEGER DEFAULT 0)
                             """)
            self.conn.execute("""CREATE TABLE IF NOT EXISTS house(
                              id INTEGER PRIMARY KEY,
                              level INTEGER,
                              gold_cost INTEGER,
                              wood_cost INTEGER,
                              stone_cost INTEGER)""")
            
    def insert_houses(self):
       houses = [
          (1, 1, 2, 10, 8),
          (2, 2, 5, 20, 15),
          (3, 3, 10, 40, 30),
          (4, 4, 20, 100, 80),
          (5, 5, 40, 200, 180)]
       with self.conn:
          cur = self.conn.cursor()
          cur.executemany("""INSERT OR IGNORE INTO house (id, level, gold_cost, wood_cost, stone_cost) VALUES (?, ?, ?, ?, ?)""", houses)
       
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
              food = 0
              gold = 0
              wood = 0
              stone = 0
              story = 0
              house_lvl = 0
              cur.execute('''INSERT INTO users (user_id, username, food, gold, wood, stone, story, house_lvl) VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', (user_id, username, food, gold, wood, stone, story, house_lvl))
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
       markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
       markup.add("Профиль", "Охота")
       bot.send_message(user_id, """*Бог:* Здравствуй, сын мой божий. Ты один из единственных, кому удалось пережить это несчастье.""", parse_mode="Markdown")
       time.sleep(2.5)
       bot.send_message(user_id,"""*Бог:* Ну что-же, для начала награжу ка я тебя как избранного ресурсами, в которых ты сейчас очень нуждаешься, держи 10 кусочков золота🏅, 20 кусков дерева🪵 и 20 камней🪨, с ними ты сможешь построить свой первый дом""", parse_mode="Markdown") 
       time.sleep(2)
       with self.conn:
          cur = self.conn.cursor()
          cur.execute("""
            UPDATE users SET gold = gold + 10, wood = wood + 20, stone = stone + 20, story = 1 
            WHERE user_id = ?
        """, (user_id,))    
       bot.send_message(user_id, "<i>Вам зачисленно: </i> +20🏅, +20🪵, +20🪨", parse_mode="HTML")  
      
       bot.send_message(user_id, """*Бог:* Скоро ты построишь себе новый дом, но сначала, иди ка ты на охоту, ты очень голодный, тебе стоило бы поесть, поэтому нажми в меню на кнопку *Охота*, чтобы добыть еды""", parse_mode="Markdown", reply_markup=markup)
       
    def hunt(self, message):
       user = self.select_user(message)
       user_id = message.chat.id
       now = time.time()
       cooldown = 60   
          
       cur = self.conn.cursor()
       cur.execute("SELECT last_hunt_time FROM users WHERE user_id = ?", (user_id,))
       result = cur.fetchone()
       last_hunt = result[0] if result else 0
       now = time.time()

       if now - last_hunt < cooldown:
          remaining = int(cooldown - (now - last_hunt))
          bot.send_message(user_id, f"🕑 Подожди ещё {remaining} сек. перед следующей охотой.")
          return
       
       
       bot.send_message(user_id, "🏹 Вы отправились на охоту...")
        
       results = {animal: 0 for animal in self.animals}
       total_points = 0

       for i in range(5):
            time.sleep(1)  
            if random.random() < 0.3:
                bot.send_message(user_id, f"❌ Попытка {i+1}: Ничего не поймано.")
                continue

           
            choices = []
            for animal, points in self.animals.items():
                weight = max(1, 40 - points)
                choices.extend([animal] * weight)

            caught = random.choice(choices)
            results[caught] += 1
            total_points += self.animals[caught]
            bot.send_message(user_id, f"✅ Попытка {i+1}: Пойман {caught} (+{self.animals[caught]} очков)")

       
       msg = "<i>📊 Ваша добыча:</i>\n"
       for animal, count in results.items():
            if count > 0:
                msg += f"{animal}: {count} шт.\n"

       msg += f"\n<i>Всего очков:</i> {total_points} 🏆"

       bot.send_message(user_id, msg, parse_mode="HTML")

       markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
       markup.add("Профиль", "Охота", "Построить дом")
       self.conn.execute("UPDATE users SET food = food + ?, last_hunt_time = ? WHERE user_id = ?", (total_points, now, user_id))
       if user[7] == 1: 
        time.sleep(2)
        if total_points < 20:
           bot.send_message(user_id, """*Бог:* Мда... Не очень конечно сегодня охота вышла, но ничего, Ещё научишся. Теперь тебе стоит подумать о строительстве твоего дома.""", parse_mode="Markdown")
        else:
           bot.send_message(user_id, """*Бог:* Хорошая охота, сын мой. Ты показал, что способен выжить. Теперь тебе стоит подумать о строительстве твоего дома.""", parse_mode="Markdown")
       
        time.sleep(2)
        self.conn.execute("UPDATE users SET story = 2 WHERE user_id = ?", (user_id,))
        bot.send_message(user_id, """*Бог:* Построй себе дом. Для этого тебе понадобятся 2🏅 10🪵 и 8🪨. Нажми на кнопку *Построить дом* в меню""", parse_mode="Markdown", reply_markup=markup)

    def house(self, message):
        user_id = message.chat.id
        with self.conn:
          cur = self.conn.cursor()
          cur.execute('''SELECT u.gold, u.wood, u.stone, u.house_lvl,  u.story,
                      h.gold_cost, h.wood_cost, h.stone_cost FROM users u
                      INNER JOIN house h ON u.house_lvl + 1 = h.level
                      WHERE u.user_id = ?
                    ''', (user_id,))
          data = cur.fetchone()       
          if data:
           gold, wood, stone, house_lvl, story, gold_cost, wood_cost, stone_cost = data

           if gold < gold_cost or wood < wood_cost or stone < stone_cost:
            bot.send_message(user_id, "Недостаточно ресурсов для следующего уровня дома!")
            return

           cur.execute("""
           UPDATE users
           SET gold = gold - ?, wood = wood - ?, stone = stone - ?, house_lvl = house_lvl + 1
           WHERE user_id = ?
           """, (gold_cost, wood_cost, stone_cost, user_id))

           bot.send_message(user_id, f"🎉 Вы построили дом уровня {house_lvl + 1}!\nВаш баланс: 🏅 {gold - gold_cost}, 🪵 {wood - wood_cost}, 🪨 {stone - stone_cost}")
           house_photo = f"C:\\Users\\Admin\\OneDrive\\Desktop\\simulator\\images\\lvl{house_lvl + 1}.jpg"
           if os.path.exists(house_photo):
               with open(house_photo, "rb") as f:
                  bot.send_photo(user_id, f)
                  if story == 2:
                     markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                     markup.add("Профиль", "Охота", "Построить дом", "Путешествие")
                     bot.send_message(user_id, "*Бог: *Ну чтож, сын мой божий, вот твой первый дом, скромноватый, но жить можно, потом лучше сделаешь. Теперь тебе нужно добыть ресурсов чтобы начать выживать. Теперь нажми на кнопку *Путешествие* чтобы начать, но учти, что ты не можешь отправлятся в путешествие на голодный желудок!", parse_mode="Markdown", reply_markup=markup)
                     cur.execute("""UPDATE users
                                    SET story = 3""")
                 
          else:
           bot.send_message(user_id, "🏚️ Максимальный уровень дома достигнут.")
           

    def adventure(self, message):
     with self.conn:
        cur = self.conn.cursor()
        user_id = message.chat.id
        player_hp = 6
        user = self.select_user(message)

        if user[7] < 3:
            bot.send_message(user_id, "Ты ещё не можешь путешествовать.")
            return

        if user[3] < 20:
            bot.send_message(user_id, f"Ты голодный, нужно минимум 20 единиц 🍖, а у тебя их {user[3]}")
            return

        events = ["Zombie", "Wood", "Stone"]
        killed_zombies = 0
        extracted_gold = 0
        extracted_wood = 0
        extracted_stone = 0

        if user[7] >= 3:
            event_list = ["Zombie", "Wood", "Stone"]
        else:
            foundings = random.randint(2, 5)
            event_list = [random.choice(events) for _ in range(foundings)]
        
        for event in event_list:
            if player_hp <= 0:
                break

            if event == "Zombie":
                zombie_hp = random.randint(2, 6)
                zombie_hp_start = zombie_hp
                letters = ["A", "B", "C", "D", "E", "F"]
                target_letter = ""

                bot.send_message(user_id, "На вас напал зомби🧟‍♂, защишайтесь!")

                if user[7] == 3:
                    bot.send_message(user_id, "Пиши букву (*на латыни*), которая будет задана. Если правильно — урон зомби, иначе — урон тебе.", parse_mode="Markdown")
                    time.sleep(3)
                    bot.send_message(user_id, "Итак, начнём:")
        
                def new_letter():
                  nonlocal zombie_hp, player_hp, target_letter
                  target_letter = random.choice(letters)
                  bot.send_message(user_id, f"👉 Напиши букву: {target_letter}")
                  bot.register_next_step_handler(message, fight_step)
                

                def fight_step(message):
                  nonlocal zombie_hp, player_hp, target_letter, killed_zombies, extracted_gold
                  answer = message.text.strip().upper()

                  if answer == target_letter:
                    zombie_hp -= 1
                    percent = round(zombie_hp / zombie_hp_start * 100) if zombie_hp > 0 else 0
                    bot.send_message(user_id, f"✅ Бам! У зомби осталось {percent}% HP.")
                    if zombie_hp  or player_hp <= 0: 
                      new_letter()
                  else:
                   player_hp -= 1
                   percent = round(player_hp / 6 * 100) if player_hp > 0 else 0
                   bot.send_message(user_id, f"❌ Ай! У тебя осталось {percent}% HP.")
                   if zombie_hp  or player_hp <= 0: 
                      new_letter()
                   if zombie_hp <= 0:
                    gold = zombie_hp_start // 2
                    bot.send_message(user_id, f"🏆 Победа! Ты получил {gold} кусочков золота.")
                    extracted_gold += gold
                    killed_zombies += 1 
                   elif player_hp <= 0:
                    bot.send_message(user_id, "💀 Ты проиграл! Зомби прокусил твои доспехи.")
                    time.sleep(2)
                   if user[7] == 3:
                    cur.execute(""" UPDATE users SET story = 4 WHERE user_id = ? """,(user_id,))
                    bot.send_message(user_id, "*Бог: * К сожалению, ты не победил зомби. Но не переживай, это только начало...", parse_mode="Markdown")
                  

                
                  
                if player_hp > 0 and zombie_hp > 0:
                    pass

                if player_hp <= 0:
                    break  

                else:
                   new_letter()
            elif event == "Wood":
                wood_gained = random.randint(2, 7)
                if user[3] == 3:
                   bot.send_message(user_id, f"Если ты находишь дерево, ты поличшь случайное количество дров.")
                bot.send_message(user_id, f"Ты добыл {wood_gained} {'куска' if wood_gained < 5 else 'кусков'} дерева 🌲.")
                extracted_wood += wood_gained

            elif event == "Stone":
                stone_gained = random.randint(2, 5)
                if user[3] == 3:
                   bot.send_message(user_id, f"Если ты находишь камень, то как и с деревом ты поличшь случайное количество кусков камня🪨.")
                bot.send_message(user_id, f"Ты нашёл {stone_gained} {'кусочка ' if wood_gained < 5 else 'кусков '} камней 🪨.")
                extracted_stone += stone_gained

            time.sleep(2)

      
        cur.execute("""
            UPDATE users
            SET gold = gold + ?, wood = wood + ?, stone = stone + ?, food = food - 20
            WHERE user_id = ?
        """, (extracted_gold, extracted_wood, extracted_stone, user_id))

        summary = (
            f"🌍 Приключение окончено!\n"
            f"🧟 Убито зомби: {killed_zombies}\n"
            f"🏅 Найдено золота: {extracted_gold}\n"
            f"🌲 Найдено дерева: {extracted_wood}\n"
            f"🪨 Найдено камня: {extracted_stone}\n"
            f"🍖 -20 еды"
        )
        bot.send_message(user_id, summary)
        
        if user[7] == 3:
           time.sleep(2)
           cur.execute("""
            UPDATE users
            SET story = 4
            WHERE user_id = ?
        """, (user_id,))

           bot.send_message(user_id, "*Бог: * Хорошее было сегодня приключение, воин!\nТы сражался достойно и вернулся с добычей. Я оставлю тебя на время, иди на охоту, строй дома и развивайся, потом увидишь как судьба с тобой поиграет...", parse_mode="Markdown")
        
        
   # Next step funktion!!!!!!!!