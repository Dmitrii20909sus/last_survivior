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
                             story REAL DEFAULT 0,
                             last_hunt_time REAL DEFAULT 0,
                             house_lvl INTEGER DEFAULT 0,
                             weak_spot TEXT,
                             call_data TEXT,
                             food_for_children INTEGER DEFAULT 0, 
                             people INTEGER DEFAULT 0
                             )
                             """)
            self.conn.execute("""CREATE TABLE IF NOT EXISTS house(
                              id INTEGER PRIMARY KEY,
                              level INTEGER,
                              gold_cost INTEGER,
                              wood_cost INTEGER,
                              stone_cost INTEGER)""")
            self.conn.execute("""CREATE TABLE IF NOT EXISTS artifacts (
                              id INTEGER PRIMARY KEY AUTOINCREMENT,
                              name TEXT,
                              house_level_required INTEGER)""")
            self.conn.execute("""CREATE TABLE IF NOT EXISTS user_artifacts (
                              user_id INTEGER,
                              artifact_id INTEGER,
                              FOREIGN KEY (artifact_id) REFERENCES artifacts(id))""")
            
    def insert_houses(self):
       houses = [
          (1, 1, 2, 10, 8),
          (2, 2, 5, 20, 15),
          (3, 3, 10, 40, 30),
          (4, 4, 20, 60, 40),
          (5, 5, 40, 90, 70)]
       with self.conn:
          cur = self.conn.cursor()
          cur.executemany("""INSERT OR IGNORE INTO house (id, level, gold_cost, wood_cost, stone_cost) VALUES (?, ?, ?, ?, ?)""", houses)
    
    def insert_artifacts(self):
     artifacts = [
        ("🦷🦈 Зуб тралалело тралала", 1),
        ("🌲 Корень Бр бр батапим", 1),
        ("🏏 Дубина Тунг тунг тунг сахура", 2),
        ("🦦 Кокос Борбалони лулилоли", 2),
        ("🐸 Шина Бонека амбалабу", 3),
        ("🐱🦐 Усик Трипи тропи",3),
        ("☕🔪 Катана Капучино асасино", 4),
        ("🐦🔎 Перо Шпиониро голубино",4),
        ("🐘🌵 Иголка Лирили ларила",5),
        ("💣🐊 Бомба Бомбардино крокодило", 5)

    ]
     with self.conn:
      cur = self.conn.cursor()
      cur.executemany("INSERT OR IGNORE INTO artifacts (name, house_level_required) VALUES (?, ?)", artifacts)
    

    def select_user(self, message):
        if hasattr(message, 'chat') and message.chat: 
         user_id = message.chat.id
        elif hasattr(message, 'message') and hasattr(message.message, 'chat'): 
         user_id = message.message.chat.id
        else:
         raise ValueError("Unknown message type!!!!")

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
    def profile(self, message):
       with self.conn:
        cur = self.conn.cursor()
        user_id = message.chat.id
        user = self.select_user(message)
        if user[9] == 0:
          house = str("Нету дома")
          bot.send_message(user_id, f"👤* Твой профиль: *\n\n 🏅 Золото: {user[4]} \n 🪵 Дерево: {user[5]}\n 🪨 Камень: {user[6]} \n🍗 Еда: {user[3]}\n 🏠 Уровень дома: {house}\n 👦Население: {user[13]}\n 🍗👦 Еда для послеления{user[12]}", parse_mode="Markdown")
        elif 0 < user[7] < 10: 
          house = user[9]
          result = " "
          cur.execute("""
            SELECT a.name 
            FROM artifacts a
            JOIN user_artifacts ua ON a.id = ua.artifact_id
            WHERE ua.user_id = ?
        """, (user_id,))
          owned = [row[0] for row in cur.fetchall()]
          if owned:
            result += "\n  ".join(owned) 
          else:
            result += " У тебя пока нет артефактов."
         
          bot.send_message(user_id, f"👤* Твой профиль: *\n\n 🏅 Золото: {user[4]} \n 🪵 Дерево: {user[5]}\n 🪨 Камень: {user[6]} \n🍗 Еда: {user[3]}\n 🏠 Уровень дома: {house} \n 🧿 Артефакты: \n {result}", parse_mode="Markdown")
        else: 
          house = user[9]
          result = " "
          cur.execute("""
            SELECT a.name 
            FROM artifacts a
            JOIN user_artifacts ua ON a.id = ua.artifact_id
            WHERE ua.user_id = ?
        """, (user_id,))
          owned = [row[0] for row in cur.fetchall()]
          if owned:
            result += "\n  ".join(owned) 
          else:
            result += " У тебя пока нет артефактов."    
          bot.send_message(user_id, f"👤* Твой профиль: *\n\n 🏅 Золото: {user[4]} \n 🪵 Дерево: {user[5]}\n 🪨 Камень: {user[6]} \n🍗 Еда: {user[3]}\n 🏠 Уровень дома: {house} 👦Население: {user[13]}\n 🍗👦 Еда для послеления{user[12]} \n 🧿 Артефакты: \n {result}", parse_mode="Markdown")
       if user[9] > 0:
          house_photo = f"C:\\Users\\Admin\\OneDrive\\Desktop\\simulator\\images\\lvl{house}.jpg"
          with open(house_photo, "rb") as f:
             bot.send_photo(user_id, f)
       if user is None:
          bot.send_message(user_id, f"У тебя ещё нету профиля")
       
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
       god = f"C:\\Users\\Admin\\OneDrive\\Desktop\\simulator\\images\\god.jpg"
       if os.path.exists(god):
        with open(god, "rb") as f:
         bot.send_photo(user_id, f)
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
        
       self.results = {animal: 0 for animal in self.animals}
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
            self.results[caught] += 1
            total_points += self.animals[caught]
            bot.send_message(user_id, f"✅ Попытка {i+1}: Пойман {caught} (+{self.animals[caught]} очков)")

       
       msg = "<i>📊 Ваша добыча:</i>\n"
       for animal, count in self.results.items():
            if count > 0:
                msg += f"{animal}: {count} шт.\n"
       if user[7] < 10:
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
        elif user[7] == 10:
        
         time.sleep(2)
         self.conn.execute("UPDATE users SET story = 2 WHERE user_id = ?", (user_id,))
         bot.send_message(user_id, """*Бог:* Построй себе дом. Для этого тебе понадобятся 2🏅 10🪵 и 8🪨. Нажми на кнопку *Построить дом* в меню""", parse_mode="Markdown", reply_markup=markup)
       elif user[7] >= 10:
           child_food = total_points * 0,3
           food_for_you = total_points * 0,7

           child_food = int(round(total_points * 0.3))
           food_for_you = total_points - child_food
           msg += f"\n<i>Всего очков:</i> {total_points} 🏆"
           msg += f"\n<i>Для тебя:</i> {food_for_you} 🏆"
           msg += f"\n<i>Для детей:</i> {child_food} 🏆"
           bot.send_message(user_id, msg, parse_mode="HTML")
         
           self.conn.execute("UPDATE users SET food = food + ?, food_for_children = food_for_children + ?, last_hunt_time = ? WHERE user_id = ?", (food_for_you, child_food, now, user_id))

    def house(self, message):
     user_id = message.chat.id
     user = self.select_user(message)
     markupp = types.InlineKeyboardMarkup()
     buttonp = types.InlineKeyboardButton("Купить дом", callback_data = "buyNewHouse")
     markupp.add(buttonp)
     with self.conn:
        cur = self.conn.cursor()
        cur.execute('''SELECT u.gold, u.wood, u.stone, u.house_lvl, u.story,
                        h.gold_cost, h.wood_cost, h.stone_cost FROM users u
                        INNER JOIN house h ON u.house_lvl + 1 = h.level
                        WHERE u.user_id = ?''', (user_id,))
        data = cur.fetchone()

        if data:
            gold, wood, stone, house_lvl, story, gold_cost, wood_cost, stone_cost = data

            if gold < gold_cost or wood < wood_cost or stone < stone_cost:
                bot.send_message(user_id, f"🏠 *Дом *\n\n Следующий уровень: *{house_lvl + 1}*\n 💰 Золото: {gold_cost} (у вас: {gold})\n Дерево: {wood_cost} (у вас: {wood})\n🪨 Камень: {stone_cost} (у вас: {stone})\n\n", parse_mode="Markdown")
                bot.send_message(user_id, "Недостаточно ресурсов для следующего уровня дома!")
                return
            else:
                bot.send_message(user_id, f"🏠 *Дом*\n\n Следующий уровень: *{house_lvl + 1}*\n 💰 Золото: {gold_cost} (у вас: {gold})\n Дерево: {wood_cost} (у вас: {wood})\n🪨 Камень: {stone_cost} (у вас: {stone})\n\n", parse_mode="Markdown", reply_markup=markupp)
        else:
            bot.send_message(user_id, "🏚️ Максимальный уровень дома достигнут.")
            house_photo = f"C:\\Users\\Admin\\OneDrive\\Desktop\\simulator\\images\\5.jpg"
            if os.path.exists(house_photo):
                with open(house_photo, "rb") as f:
                    bot.send_photo(user_id, f)
    
    def house_bought(self, call):
      user_id = call.message.chat.id
      with self.conn:
       
        cur = self.conn.cursor()
        cur.execute('''SELECT u.gold, u.wood, u.stone, u.house_lvl, u.story,
                        h.gold_cost, h.wood_cost, h.stone_cost FROM users u
                        INNER JOIN house h ON u.house_lvl + 1 = h.level
                        WHERE u.user_id = ?''', (user_id,))
        data = cur.fetchone()

        if data:
            gold, wood, stone, house_lvl, story, gold_cost, wood_cost, stone_cost = data
            cur.execute("""
                UPDATE users
                SET gold = gold - ?, wood = wood - ?, stone = stone - ?, house_lvl = house_lvl + 1
                WHERE user_id = ?
            """, (gold_cost, wood_cost, stone_cost, user_id))
            self.conn.commit()

            bot.send_message(user_id, f"🎉 Вы построили дом уровня {house_lvl + 1}!\nВаш баланс: 🏅 {gold - gold_cost}, 🪵 {wood - wood_cost}, 🪨 {stone - stone_cost}")
            print(house_lvl)
            house_photo = f"C:\\Users\\Admin\\OneDrive\\Desktop\\simulator\\images\\lvl{house_lvl + 1}.jpg"
            if os.path.exists(house_photo):
                with open(house_photo, "rb") as f:
                    bot.send_photo(user_id, f)

            if story == 2:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                markup.add("Профиль", "Охота", "Улучшить дом", "Путешествие")
                bot.send_message(user_id, "*Бог: *Ну чтож, сын мой божий, вот твой первый дом, скромноватый, но жить можно, потом лучше сделаешь. Теперь тебе нужно добыть ресурсов чтобы начать выживать. Теперь нажми на кнопку *Путешествие* чтобы начать, но учти, что ты не можешь отправлятся в путешествие на голодный желудок!", parse_mode="Markdown", reply_markup=markup)

                cur.execute("""UPDATE users SET story = 3 WHERE user_id = ?""", (user_id,))
                self.conn.commit()

            if house_lvl + 1 == 2:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                markup.add("Профиль", "Охота", "Улучшить дом", "Путешествие", "Продолжить сюжет")
                cur.execute("UPDATE users SET story = 5 WHERE user_id = ?", (user_id,))
                bot.send_message(user_id, "Вы можете продолжить сюжет (нажмите в меню)", reply_markup=markup)

            elif house_lvl + 1 == 3:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                markup.add("Профиль", "Охота", "Улучшить дом", "Путешествие", "Артефакты", "Продолжить сюжет")
                cur.execute("UPDATE users SET story = 7 WHERE user_id = ?", (user_id,))
                bot.send_message(user_id, "Вы можете продолжить сюжет (нажмите в меню)", reply_markup=markup)

            elif house_lvl + 1 == 4:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                markup.add("Профиль", "Охота", "Улучшить дом", "Путешествие", "Артефакты", "Продолжить сюжет")
                cur.execute("UPDATE users SET story = 9 WHERE user_id = ?", (user_id,))
                bot.send_message(user_id, "Вы можете продолжить сюжет (нажмите в меню)", reply_markup=markup)        
    def handle_zombie(self, message):
       user = self.select_user(message)
       if user[10] == user[11]:
           return True
       else:
          return False
    def check_for_new_artifacts(self, user_id):
     cur = self.conn.cursor()
     cur.execute("SELECT house_lvl FROM users WHERE user_id = ?", (user_id,))
     row = cur.fetchone()
     if not row:
        return
     house_level = row[0]

   
     cur.execute("""
        SELECT id, name FROM artifacts
        WHERE house_level_required <= ?
        AND id NOT IN (
            SELECT artifact_id FROM user_artifacts WHERE user_id = ?
        )
    """, (house_level, user_id))
    
     available_artifacts = cur.fetchall()

     if not available_artifacts:
        return

     if house_level == 2:
        chance = 2
     elif house_level == 3:
        chance = 3
     elif house_level == 4:
        chance = 5
     elif house_level == 5:
        chance = 15
     else: 
        chance = 0
     

  
     if chance > 0 and random.randint(1, chance) == 1:
        artifact = random.choice(available_artifacts)
        artifact_id, name = artifact
        cur.execute("INSERT INTO user_artifacts (user_id, artifact_id) VALUES (?, ?)", (user_id, artifact_id))
        self.conn.commit()
        bot.send_message(user_id, f"🗿 Ты нашёл древний артефакт: *{name}*", parse_mode="Markdown")  
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

        if user[7] == 3:
            event_list = ["Zombie", "Wood", "Stone"]
        else:
            foundings = random.randint(2, 5)
            event_list = [random.choice(events) for _ in range(foundings)]
        
        for event in event_list:

            if event == "Zombie":
                zombie_hp = random.randint(2, 6)
                zombie_hp_start = zombie_hp
                weak_spots = ["Голова", "Печень", "Грудь", "Нога"]
                target_weak_spot = ""

                bot.send_message(user_id, "На вас напал зомби🧟‍♂, защишайтесь!")
                
                if user[7] == 3:
                    bot.send_message(user_id, "Каждый раз у зомби открытое место. Нажми на правильную кнопку. Если нажмёшь правильно — урон зомби, иначе — урон тебе. Каждый раз у тебя есть 3 секунды на раздумку", parse_mode="Markdown")
                    time.sleep(6)
                    bot.send_message(user_id, "Итак, начнём:")
                markup = types.InlineKeyboardMarkup()
                buttons = [
                        types.InlineKeyboardButton("Голова", callback_data="head"),
                        types.InlineKeyboardButton("Печень", callback_data="liver"),
                        types.InlineKeyboardButton("Грудь", callback_data="chest"),
                        types.InlineKeyboardButton("Нога", callback_data="leg")
                        ]
                markup.add(*buttons)
                while zombie_hp > 0 and player_hp > 0:
                     
                 target_weak_spot = random.choice(weak_spots)
                
                 bot.send_message(user_id, f"👉 Открытое место: {target_weak_spot}", reply_markup=markup) 
                 self.conn.execute("UPDATE users SET weak_spot = ? WHERE user_id = ?", (target_weak_spot, user_id))
                 time.sleep(3)
                 if self.handle_zombie(message) == True:
                    zombie_hp -= 1
                    percent = round(zombie_hp / zombie_hp_start * 100) if zombie_hp > 0 else 0
                
                    bot.send_message(user_id, f"✅ Бам! У зомби осталось {percent}% HP.")
                    if zombie_hp < 0 or player_hp < 0: 
                      target_weak_spot = random.choice(weak_spots)
                   
                    
                      bot.send_message(user_id, f"👉 Открытое место: {target_weak_spot}",
                        reply_markup=markup)
                      self.conn.execute("UPDATE users SET weak_spot = ? WHERE user_id = ?", (target_weak_spot, user_id))
                      time.sleep(3)
                 else:
                   player_hp -= 1
                   percent = round(player_hp / 6 * 100) if player_hp > 0 else 0
              
                   bot.send_message(user_id, f"❌ Ай! У тебя осталось {percent}% HP.")
                   if zombie_hp < 0 and player_hp < 0: 
                      target_weak_spot = random.choice(weak_spots)
                      bot.send_message(user_id, f"👉 Открытое место: {target_weak_spot}",
                       reply_markup=markup)
                      self.conn.execute("UPDATE users SET weak_spot = ? WHERE user_id = ?", (target_weak_spot, user_id))
                      time.sleep(3)
                 if zombie_hp == 0:
                    gold = zombie_hp_start // 2
                    if gold < 5:
                      kusok = 'кусочка'
                    else:
                      kusok = 'кусочек'
                    bot.send_message(user_id, f"🏆 Победа! Ты получил {gold} {kusok} золота.")
                    sus = None
                    self.conn.execute("UPDATE users SET weak_spot = ?, call_data = ? WHERE user_id = ?", (sus, sus, user_id))
                    extracted_gold += gold
                    killed_zombies += 1 
                    break
                 elif player_hp == 0:
                    bot.send_message(user_id, "💀 Ты проиграл! Зомби прокусил твои доспехи, ты не получаешь заработанные награды.")
                    sus = None
                    self.conn.execute("UPDATE users SET weak_spot = ?, call_data = ? WHERE user_id = ?", (sus, sus, user_id))
                    time.sleep(2)
                    if user[7] == 3:
                     cur.execute(""" UPDATE users SET story = 4 WHERE user_id = ? """,(user_id,))
                     bot.send_message(user_id, "*Бог: * К сожалению, ты не победил зомби. Но не переживай, это только начало...", parse_mode="Markdown")
                    return
                   
            elif event == "Wood":
                wood_gained = random.randint(2, 7)
                if wood_gained < 5:
                      kusok = 'дрова'
                else:
                      kusok = 'дров'
                if user[7] == 3:
                   bot.send_message(user_id, f"Если ты находишь дерево, ты получишь случайное количество дров.")
                bot.send_message(user_id, f"Ты добыл {wood_gained} {kusok} дерева 🌲.")
                extracted_wood += wood_gained

            elif event == "Stone":
                stone_gained = random.randint(2, 5)
                if stone_gained < 5:
                      kusok = 'кусочка'
                else:
                      kusok = 'кускочков'
                if user[7] == 3:     
                   bot.send_message(user_id, f"Если ты находишь камень, то как и с деревом ты поличшь случайное количество кусков камня🪨.")
                bot.send_message(user_id, f"Ты нашёл {stone_gained} {kusok} камней 🪨.")
                extracted_stone += stone_gained

            time.sleep(2)
        self.check_for_new_artifacts(user_id)
      
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
      
    def story_lvl2(self, message):
       user_id = message.chat.id
       user = self.select_user(message)
       with self.conn:
          cur = self.conn.cursor()
          cur.execute("UPDATE users SET story = 5 WHERE user_id = ?", (user_id,))
          if user[7] == 5:
           markup = types.InlineKeyboardMarkup()
           resque = types.InlineKeyboardButton("Спасти странствующего", callback_data="resqueZolo")
           markup.add(resque)
           let_in = types.InlineKeyboardButton("Впустить професора", callback_data="LetInZolo")
           bot.send_message(user_id, "*Странствущий:* ААААААА!!!! СПАСИТЕ!!!!!! ЗОМБИ!!!!!", reply_markup=markup, parse_mode="Markdown")         
    def story_ivan_resqued(self, message):
             markup = types.InlineKeyboardMarkup()
             user_id = message.chat.id
             let_in = types.InlineKeyboardButton("Впустить професора", callback_data="LetInZolo")
             markup.add(let_in)
             bot.send_message(user_id, "*Проф. Иван Золо: * Дорогой человек, от всего серда благодарю тебя за спасение моей жизни! Меня зовут профессор иван золо, я учённый в области биологии и я очень хочу поставить точку над этим вирусом, но для этого мне нужны определённые артифакты. Впусти меня в свой дом, у меня собой гостинцы есть.", parse_mode="Markdown", reply_markup=markup)
    def story_ivan_let_in(self, message):
             user_id = message.chat.id        
             bot.send_message(user_id, "<i>Вам зачисленно: </i> +15🍖", parse_mode="HTML")
             time.sleep(2)
             markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
             markup.add("Профиль", "Охота", "Улучшить дом", "Путешествие", "Артефакты")
             bot.send_message(user_id, "*Проф. Иван Золо: * Вобщем, чтобы помочь мне, ты когда путешествовать будешь, передавай артифакты мне, кстати список артефактов ты можешь найти в меню, в каталоге артифакты.", parse_mode="Markdown", reply_markup=markup)
             with self.conn:
              cur = self.conn.cursor()
              cur.execute("UPDATE users SET story = 6 WHERE user_id = ?", (user_id,))             
              Zolik = f"C:\\Users\\Admin\\OneDrive\\Desktop\\simulator\\images\\mrZolo.jpg"
              if os.path.exists(Zolik):
                with open(Zolik, "rb") as f:
                    bot.send_photo(user_id, f)
    def story_lvl3(self, message):      
       user_id = message.chat.id
       markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
       markup.add("Профиль", "Охота", "Улучшить дом", "Путешествие", "Артефакты")
       bot.send_message(user_id, "*Проф. Иван Золо: * Молодец что смог улучшить дом, благодаря тебе я продвинул свои иследования ещё дальше. Теперь я разузнал, какие новые артефакты надо раздобыть. Их ты можешь посмотреть нажав на кнопку артефакты.", parse_mode="Markdown", reply_markup=markup)
       Zolik3 = f"C:\\Users\\Admin\\OneDrive\\Desktop\\simulator\\images\\zolik3lvl.jpg"
       if os.path.exists(Zolik3):
        with open(Zolik3, "rb") as f:
          bot.send_photo(user_id, f)
        
       with self.conn:
        cur = self.conn.cursor()
        cur.execute("UPDATE users SET story = 8 WHERE user_id = ?", (user_id,))

    def story_lvl4(self, message):        
       user_id = message.chat.id
       bot.send_message(user_id, "*Проф. Иван Золо: * Опять же поздравлю тебя с нашим новым тобой постройленным домом. Соответственно я расширил мои исследование я понял какие нам артефакты нам ещё нуж... Погоди, ты это слышишь?", parse_mode="Markdown")
       time.sleep(2)
       markup = types.InlineKeyboardMarkup()
       open = types.InlineKeyboardButton("Открыть дверь", callback_data="dora")
       markup.add(open)
       bot.send_message(user_id, "ТУК ТУК ТУК", reply_markup=markup)

    def story_dora(self, message):
       user_id = message.chat.id
       markup = types.InlineKeyboardMarkup()
       let_in = types.InlineKeyboardButton("Впустить Марию Ивановну", callback_data="LetInDora")
       markup.add(let_in)
       bot.send_message(user_id, "*Мария Ивановна: *Здраствуйте, меня зовут Мария Ивановна, раньше я была учительницой математики, но из-за зомби апокалипсиса я потеряла всё что у меня есть включая мою семью. Впустите меня пожалуйста в дом.", parse_mode="Markdown", reply_markup=markup)
       matematichka = f"C:\\Users\\Admin\\OneDrive\\Desktop\\simulator\\images\\matematichka.jpg"
       if os.path.exists(matematichka):
        with open(matematichka, "rb") as f:
          bot.send_photo(user_id, f)

    def Ivan_Dora_plan(self, message):
       user_id = message.chat.id 
       markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
       markup.add("Профиль", "Охота", "Улучшить дом", "Путешествие", "Артефакты", "Поселение")
       bot.send_message(user_id, "*Проф. Иван Золо:* Здравствуйте, я очень рад за вас что вы выжили, вы нам как раз очень нужны.",parse_mode="Markdown")
       time.sleep(3)
       bot.send_message(user_id, """*Проф. Иван Золо к тебе:* Так, коллега у меня есть план: Нам нужно развить цивилизацию людей чтобы побороть этот вирус усилиями наших потомков. Поэтому ты должен каждый раз после охоты делиться с нами 30% едой,а мы в это время с дорой будет продцуровать новый людей. Они тем временем будут становиться всё умнее и будут оснащать тебя новыми гаджетами которые будут облегчать тебе охоту и путешествие, что поможет тебе добывать больше ресурсов. А за поселением ты можешь следить спомощью кнопки __Поселение__. Я надесь ты всё понял, а теперь иди на охоту, не терпится когда ты уже уйдёшь)""", parse_mode="Markdown", reply_markup=markup)
       with self.conn:
        cur = self.conn.cursor()
        cur.execute("UPDATE users SET story = 10 WHERE user_id = ?", (user_id,))
       dorazolo = f"C:\\Users\\Admin\\OneDrive\\Desktop\\simulator\\images\\ZoloDora.jpg"
       if os.path.exists(dorazolo):
        with open(dorazolo, "rb") as f:
          bot.send_photo(user_id, f)
    def get_user_artifacts(self, user_id):
     with self.conn:
        cur = self.conn.cursor()
     
        cur.execute("""
            SELECT a.name 
            FROM artifacts a
            JOIN user_artifacts ua ON a.id = ua.artifact_id
            WHERE ua.user_id = ?
        """, (user_id,))
        owned = [row[0] for row in cur.fetchall()]

        cur.execute("""
            SELECT a.name 
            FROM artifacts a
            JOIN users u ON u.user_id = ?
            WHERE a.house_level_required <= u.house_lvl
            AND a.id NOT IN (
                SELECT artifact_id 
                FROM user_artifacts 
                WHERE user_id = ?
            )
        """, (user_id, user_id))
        available = [row[0] for row in cur.fetchall()]

     
        result = "📜 *Ваши артефакты:*\n"
        if owned:
            result += "\n".join(owned) 
        else:
            result += "У тебя пока нет артефактов."

        result += "\n\n🧿 *Доступные артефакты для твоего уровня:*\n"
        if available:
            result += "\n".join(available)  
        else:
            result += "Нет новых артефактов для твоего уровня."

        bot.send_message(user_id, result, parse_mode="Markdown")

    def population(self, message):
       user_id = message.chat.id
       bot.send_message(user_id, "Bababoy")
