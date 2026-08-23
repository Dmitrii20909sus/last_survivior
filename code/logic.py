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
        
        self.weapon_stickers = {
            'Оружие для охоты': {
                0: 'CAACAgIAAxkBAi1RkWiaN3PmM9SxMcWjKmGHO0-rqC_mAAIoigACVLS4SEqXoH2cx2MINgQ',
                1: 'CAACAgIAAxkBAi3semibfH5inepIyf67OjnsHsZjsSVFAAJwfwACLau4SM6_x5pNdb_uNgQ',
                2: 'CAACAgIAAxkBAi3snGibfRdrmgSpFFpwd19D6hAVFUs8AALjdAACy_TASNyQyVGbz17ENgQ',
                3: 'CAACAgIAAxkBAi3srmibfTmgOdVL9nwEFm6hYWowUaM_AAIreAACvb7ASFWz34GW9W9_NgQ',
                4: 'CAACAgIAAxkBAi3stmibfUrGXazQnDwVNTfMmQzrSkZVAAKzigAC8AzASBk5L2N1XHKqNgQ',
            },
            'Кирка': {
                0: 'CAACAgIAAxkBAi3ucWibghl7UaXvaPNjpGL6eeDTHG06AAL9fQACWQbBSFedBLsBSs_4NgQ',
                1: 'CAACAgIAAxkBAi3uf2ibgjZgH7LNVDVgOjKdFlYrTCeDAAJQgQAC4erBSKjgIXibPnZfNgQ',
                2: 'CAACAgIAAxkBAi3uimibgk35QxZaS_sSlBV7xojKEcFJAAIefgACWRnBSJWm3yQ2M_dHNgQ',
                3: 'CAACAgIAAxkBAi3ulWibgl1JX8Gm_CEWDRwzRT2nMyTmAAJOhgAC6t3ASJ-buaw31tDwNgQ',
                4: 'CAACAgIAAxkBAi3umWibgmtmt7Cd4SoJtCbFSfdlFJSgAAL9fAACm5nBSJxJ6rmNfL6GNgQ',
            },
            'Топор': {
                0: 'CAACAgIAAxkBAi3uqGibgoWjc9EGjfjJdRYYTvizxok-AAKbcgAC7CDBSFX03mU1Ita6NgQ',
                1: 'CAACAgIAAxkBAi3usmibgpbtGXteRj3DO1ErQA8rn081AAKhdQAC5BjASCxk0dFQugaRNgQ',
                2: 'CAACAgIAAxkBAi3uumibgqkRdydCw-ZIZcydOdKOq0eGAAL9hgACzH65SJbIh7Q_idavNgQ',
                3: 'CAACAgIAAxkBAi3uwWibgrpDbaUSfopELidOgnmU2NwBAAJyiAACSi_BSLADf4_7zGsxNgQ',
                4: 'CAACAgIAAxkBAi3uxGibgsbw_HjJeq_IqEJdk-DxeccLAAL7gQACc9bBSCtqLwQibUVuNgQ',
            },
            'Оружие для защиты от зомби': {
                0: 'CAACAgIAAxkBAi3vJWibg_K6dNyCDlcgE3N6Wx4G88V1AALXewACrDfBSFhNO521JpVgNgQ',
                1: 'CAACAgIAAxkBAi3vK2ibhAWe_JD3B1Y1FedvLhpmmjfpAAIicAACu5fBSOuP9tbo_QABezYE',
                2: 'CAACAgIAAxkBAi3vOmibhBU62GNGYVXdQZS7-7H0AAHWWgACWnYAAtxbwUjAM0zgQDMPszYE',
                3: 'CAACAgIAAxkBAi3vQ2ibhCLcD7hXO58lZ6UcQ8Pvf8eAAAIshAACpmu5SC6vsUr0znaLNgQ',
                4: 'CAACAgIAAxkBAi3vV2ibhEZprMpaZ2zeRvVSSU5VT3gQAAKOgQACv6fBSNECFt1ed9TcNgQ',
            },
        }
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
                             house_lvl INTEGER DEFAULT 0,
                             weak_spot TEXT,
                             call_data TEXT,
                             food_for_kids INTEGER DEFAULT 0,
                             interaction BOOLEAN DEFAULT false,
                             total_people INTEGER DEFAULT 0,
                             avaible_people_for_improvement DEFAULT 0,
                             lvlfood INTEGER DEFAULT 0,
                             lvlstone INTEGER DEFAULT 0,
                             lvlwood INTEGER DEFAULT 0,
                             lvlgold INTEGER DEFAULT 0,
                             understand INTEGER DEFAULT 0
                             )""")
        self.conn.execute("""CREATE TABLE IF NOT EXISTS house(
                              id INTEGER PRIMARY KEY,
                              level INTEGER,
                              gold_cost INTEGER,
                              wood_cost INTEGER,
                              stone_cost INTEGER)""")
        self.conn.execute("""CREATE TABLE IF NOT EXISTS artifacts (
                              id INTEGER PRIMARY KEY AUTOINCREMENT,
                              name TEXT UNIQUE,
                              house_level_required INTEGER)""") 
        self.conn.execute("""CREATE TABLE IF NOT EXISTS user_artifacts (
                              user_id INTEGER,
                              artifact_id INTEGER,
                              FOREIGN KEY (artifact_id) REFERENCES artifacts(id))""")
        self.conn.execute("""CREATE TABLE IF NOT EXISTS population_boosts (
                              boost TEXT UNIQUE, 
                              lvl0boost REAL,
                              lvl1boost REAL,
                              lvl2boost REAL,
                              lvl3boost REAL,
                              lvl4boost REAL,
                              lvl1cost INTEGER,
                              lvl2cost INTEGER,
                              lvl3cost INTEGER,
                              lvl4cost INTEGER
                               )""")
    def insert_houses(self):
       houses = [
          (1, 1, 8, 15, 13),
          (2, 2, 12, 30, 29),
          (3, 3, 20, 50, 52),
          (4, 4, 50, 80, 85),
          (5, 5, 80, 130, 130)]
       with self.conn:
          cur = self.conn.cursor()
          cur.executemany("""INSERT OR IGNORE INTO house (id, level, gold_cost, wood_cost, stone_cost) VALUES (?, ?, ?, ?, ?)""", houses)
   
    def insert_population_boosts(self):
       pop_boosts = [("Оружие для охоты", 1.5, 2, 3, 4, 3, 6, 10, 16),
                     ("Кирка", 1.8, 2.5, 3.5, 5, 4, 6, 12, 20),
                     ("Топор", 1.8, 2.5, 3.5, 5, 4, 6, 12, 20),
                     ("Оружие для защиты от зомби", 2, 3, 4, 5, 4, 8, 14, 20)]
       with self.conn:
          cur = self.conn.cursor()
          cur.executemany("""INSERT OR IGNORE INTO population_boosts (boost, lvl1boost, lvl2boost,
                           lvl3boost, lvl4boost, lvl1cost, lvl2cost, lvl3cost, lvl4cost) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""", pop_boosts)

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
    
    def lvl_weapons(self, user):
        firearms_lvl = user[16]
        pickaxe_lvl = user[17]
        axe_lvl = user[18]
        knight_lvl = user[19]

        firearms = [
            "Лук",
            "Арбалет",
            "Пистолет Glock-17",
            "AK-47",
            "M134 Миниган"
        ][firearms_lvl]

        pickaxe = [
            "Каменная кирка",
            "Железная кирка Еффективность(I) Удача(I)",
            "Алмазная кирка Еффективность(III) Удача(II)",
            "Незеритовая кирка Еффективность(V) Удача(III)",
            "Бедроковая кирка Еффективность(X) Удача(X)"
        ][pickaxe_lvl]

        axe = [
            "Каменный топор",
            "Железный топор Еффективность(I) Острота(I)",
            "Алмазный топор Еффективность(III) Острота(III)",
            "Незеритовый топор Еффективность(V) Острота(VI)",
            "Бедроковый топор Еффективность(X) Острота(X)"
        ][axe_lvl]

        knight = [
            "Кинжал",
            "Меч",
            "Катана",
            "Кусаригама",
            "Опустошитель титана"
        ][knight_lvl]

        return firearms, pickaxe, axe, knight
    
    def select_user(self, message):
        if hasattr(message, 'chat') and message.chat: 
         user_id = message.chat.id
        elif hasattr(message, 'message') and hasattr(message.message, 'chat'): 
         user_id = message.message.chat.id
        else:
         raise ValueError("Unknown message type!!!!")
  
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        return cur.fetchone()
        
    def select_user_by_id(self, user_id):
        with self.conn:
            cur = self.conn.cursor()
            cur.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
            return cur.fetchone()
    
        
    def start(self, message):
        user_id = message.chat.id
        username = message.from_user.username or "Anonymous"
        with self.conn:
           cur = self.conn.cursor()
           cur.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
           user = cur.fetchone()
           if user and user[13]:  
                return
           
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
           
    def return_sticker_g(self, call):
       user_id = call.message.chat.id
       user = self.select_user(call)
       if user is None:
                bot.send_message(user_id, "Вы не зарегистрированы, напишите /start")
                return

       if user[13]:
         return
       if user[9] >= 3:
               sticker_gun = self.weapon_stickers.get('Оружие для охоты', {}).get(user[16])
               if sticker_gun:
                 bot.send_sticker(user_id, sticker_gun)


    def return_sticker_p(self, call):
       user_id = call.message.chat.id
       user = self.select_user(call)
       if user is None:
                bot.send_message(user_id, "Вы не зарегистрированы, напишите /start")
                return

       if user[13]:
         return
       if user[9] >= 3:
               sticker_pickaxe = self.weapon_stickers.get('Кирка', {}).get(user[17])
               if sticker_pickaxe:
                 bot.send_sticker(user_id, sticker_pickaxe)

    def return_sticker_a(self, call):
       user_id = call.message.chat.id
       user = self.select_user(call)
       if user is None:
                bot.send_message(user_id, "Вы не зарегистрированы, напишите /start")
                return

       if user[13]:
         return
       if user[9] >= 3:
               sticker_axe = self.weapon_stickers.get('Топор', {}).get(user[18])
               if sticker_axe:
                 bot.send_sticker(user_id, sticker_axe)

    def return_sticker_k(self, call):
       user_id = call.message.chat.id
       user = self.select_user(call)
       if user is None:
                bot.send_message(user_id, "Вы не зарегистрированы, напишите /start")
                return

       if user[13]:
         return
       if user[9] >= 3:
               sticker_knight = self.weapon_stickers.get('Оружие для защиты от зомби', {}).get(user[19])
               if sticker_knight:
                 bot.send_sticker(user_id, sticker_knight)

    def profile(self, message):
        with self.conn:
            cur = self.conn.cursor()
            user_id = message.chat.id
            user = self.select_user(message)

            if user is None:
                bot.send_message(user_id, "Вы не зарегистрированы, напишите /start")
                return

            if user[13]:
                return

            house = user[9]
            house_str = f"{house}" if house > 0 else "Нету дома"

            profile_text = (
                f"👤* Твой профиль: *\n\n"
                f"🏅 Золото: {user[4]}\n"
                f"🪵 Дерево: {user[5]}\n"
                f"🪨 Камень: {user[6]}\n"
                f"🍗 Еда: {user[3]}\n"
                f"🏠 Уровень дома: {house_str}"
            )
            result = ""
            if house > 0:
                cur.execute("""
                    SELECT a.name 
                    FROM artifacts a
                    JOIN user_artifacts ua ON a.id = ua.artifact_id
                    WHERE ua.user_id = ?
                """, (user_id,))
                owned = [row[0] for row in cur.fetchall()]
                result = "\n".join(owned) if owned else "У тебя пока нет артефактов."
                profile_text += f"\n🧿* Артефакты:*\n{result}"
           
            if house >= 3:
                firearms, pickaxe, axe, knight = self.lvl_weapons(user)
                profile_text += (
                f"\n🏠 Поселение: {user[15]}\n"
                f"🔫 Огнестрел: {firearms} (ур. {user[16]})\n"
                f"⛏️ Кирка: {pickaxe} (ур. {user[17]})\n"
                f"🪓 Топор: {axe} (ур. {user[18]})\n"
                f"🗡 Холодное оружие: {knight} (ур. {user[19]})\n"
                )
  
                markup = types.InlineKeyboardMarkup(row_width=4)
                weapons = {
                "Огнестрел": ("🔫", "g"),
                "Кирка": ("⛏", "p"),
                "Топор": ("🪓", "a"),
                "Холодное оружие": ("🗡", "k")
                }
                buttons = []
                for name, (emoji, letter) in weapons.items():
                    buttons.append(types.InlineKeyboardButton(
                    text=f"{emoji}",
                    callback_data=f"send_sticker_profile_{letter}"
                    ))
                markup.add(*buttons)

        bot.send_message(user_id, profile_text, parse_mode="Markdown")
                     

        if isinstance(house, int) and house > 0:
            house_photo = f"C:\\Users\\Admin\\OneDrive\\Desktop\\simulator\\images\\lvl{house}.jpg"
            try:
                with open(house_photo, "rb") as f:
                    bot.send_photo(user_id, f, reply_markup=markup)
            except FileNotFoundError:
                bot.send_message(user_id, "🏠 Картинка дома не найдена.", reply_markup=markup)
            
                    
    def story_0(self, message):
     with self.conn: 
       user_id = message.chat.id
       user = self.select_user(message)    
       if user:      
        if user[7] == 0:
         if user[13]:
          return
         
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        cur = self.conn.cursor()
        cur.execute("UPDATE users SET interaction = true  WHERE user_id = ?", (user_id,))
        markup.add("Профиль", "Охота")
        bot.send_message(user_id, """*Бог:* Здравствуй, сын мой божий. Ты один из единственных, кому удалось пережить это несчастье.""", parse_mode="Markdown")
        time.sleep(2.5)
        bot.send_message(user_id,"""*Бог:* Ну что-же, для начала награжу ка я тебя как избранного ресурсами, в которых ты сейчас очень нуждаешься, держи 10 кусочков золота🏅, 20 кусков дерева🪵 и 20 камней🪨, с ними ты сможешь построить свой первый дом""", parse_mode="Markdown") 
        time.sleep(2)
        cur.execute("""
            UPDATE users SET gold = gold + 10, wood = wood + 20, stone = stone + 20, story = 1 
            WHERE user_id = ?
        """, (user_id,))    
        bot.send_message(user_id, "<i>Вам зачисленно: </i> +10🏅, +20🪵, +20🪨", parse_mode="HTML")  
      
        bot.send_message(user_id, """*Бог:* Скоро ты построишь себе новый дом, но сначала, иди ка ты на охоту, ты очень голодный, тебе стоило бы поесть, поэтому нажми в меню на кнопку *Охота*, чтобы добыть еды""", parse_mode="Markdown", reply_markup=markup)
        with self.conn:
         cur.execute("UPDATE users SET interaction = false WHERE user_id = ?", (user_id,))
        god = f"C:\\Users\\Admin\\OneDrive\\Desktop\\simulator\\images\\god.jpg"
        if os.path.exists(god):
         with open(god, "rb") as f:
          bot.send_photo(user_id, f)

    def get_user_weapon(self, user_id):
        cur = self.conn.cursor()
        cur.execute("""
            SELECT users.*, 
                COALESCE(
                    CASE users.lvlfood
                        WHEN 0 THEN population_boosts.lvl0boost
                        WHEN 1 THEN population_boosts.lvl1boost
                        WHEN 2 THEN population_boosts.lvl2boost
                        WHEN 3 THEN population_boosts.lvl3boost
                        WHEN 4 THEN population_boosts.lvl4boost
                    END, 1
                ) as weapon_multiplier
            FROM users 
            LEFT JOIN population_boosts 
                ON population_boosts.boost = 'Оружие для охоты'
            WHERE users.user_id = ?;
        """, (user_id,))
        weapon_multiplier = cur.fetchone()
        return weapon_multiplier 

    def hunt(self, message):
      with self.conn:  
        user = self.select_user(message)
        user_id = message.chat.id
        killed_zombies = 0
        player_hp = 6
        extracted_gold = 0
        now = time.time()
        cur = self.conn.cursor()
        user = self.select_user(message)
        if user:
         if user[13]:  
            return

        cooldown = 40
        cur.execute("UPDATE users SET interaction = true WHERE user_id = ?", (user_id,))

        try:
            cur.execute("SELECT last_hunt_time FROM users WHERE user_id = ?", (user_id,))
            result = cur.fetchone()
            last_hunt = result[0] if result else 0

            if now - last_hunt < cooldown:
                remaining = int(cooldown - (now - last_hunt))
                bot.send_message(user_id, f"🕑 Подожди ещё {remaining} сек. перед следующей охотой.")
                return

            bot.send_message(user_id, "🏹 Вы отправились на охоту...")

            self.results = {animal: 0 for animal in self.animals}
            total_points = 0

            for i in range(5):
                time.sleep(1)
                if random.random() < 0.27:
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
            zombie_random = random.randint(1, 4)
            if zombie_random != 1:
               pass
            elif zombie_random == 1:  
                zombie_hp = random.randint(2, 6)
                zombie_hp_start = zombie_hp
                weak_spots = ["Голова", "Печень", "Грудь", "Нога"]
                target_weak_spot = ""    
                markup = types.InlineKeyboardMarkup(row_width=2)
                buttons = [
                        types.InlineKeyboardButton("Голова", callback_data="head"),
                        types.InlineKeyboardButton("Грудь", callback_data="chest"),
                        types.InlineKeyboardButton("Печень", callback_data="liver"),
                        types.InlineKeyboardButton("Нога", callback_data="leg")
                        ]
                bot.send_message(user_id, "На вас напал зомби🧟‍♂, защишайтесь!")
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
                      cur.execute("UPDATE users SET weak_spot = ? WHERE user_id = ?", (target_weak_spot, user_id))
                      time.sleep(3)
                 if zombie_hp == 0:
                    gold = zombie_hp_start // 2
                    if gold == 0 or gold >= 5:
                      kusok = 'кусочков'
                    if gold == 1:
                       kusok = 'кусочек'
                    else:
                      kusok = 'кусочка'
                    bot.send_message(user_id, f"🏆 Победа! Ты получил {gold} {kusok} золота.")
                    sus = None
                    cur.execute("UPDATE users SET weak_spot = ?, call_data = ? WHERE user_id = ?", (sus, sus, user_id))
                    extracted_gold += gold
                    killed_zombies += 1 
                    break
                 elif player_hp == 0:
                    sus = None
                    bot.send_message(user_id, "💀 Ты проиграл! Зомби прокусил твои доспехи, ты не получаешь заработанные награды.")

                    cur.execute("UPDATE users SET weak_spot = ?, call_data = ? WHERE user_id = ?", (sus, sus, user_id))
                    time.sleep(2)
                    cur.execute("""UPDATE users
                      SET food = food - 20
                      WHERE user_id = ?
                      """, (user_id,))
                    return
                        
            msg = "<i>📊 Ваша добыча:</i>\n"
            for animal, count in self.results.items():
                if count > 0:
                    msg += f"{animal}: {count} шт.\n"

            if user[7] < 7:
                msg += f"\n<i>Всего очков:</i> {total_points} 🏆 "
                msg += f"\n🧟 Убито зомби: {killed_zombies}"
                msg += f"\n🏅 Найдено золота: {extracted_gold}"
                self.conn.execute("UPDATE users SET food = food + ?, last_hunt_time = ?, gold = gold + ? WHERE user_id = ?", (total_points, now, extracted_gold, user_id))

            else:                
                user_mult = self.get_user_weapon(user_id)
                weapon_multiplier = user_mult[-1] or 1

                user_mult_k = self.get_user_knight(user_id)
                knight_multiplier = user_mult_k[-1] or 1
                total_gold_noInt = extracted_gold * knight_multiplier
                total_gold = int(total_gold_noInt)

                total_points_mult = total_points * weapon_multiplier
                total_points_mult_int = int(total_points_mult)

                food_for_you = int(total_points_mult_int * 0.7)
                food_for_kids = total_points_mult_int - food_for_you

                msg += f"\n<i>Всего очков:</i> {total_points} × {weapon_multiplier} = {total_points_mult} 🏆 "
                msg += f"\n🧟 Убито зомби: {killed_zombies}"
                msg += f"\n🏅 Найдено золота: {extracted_gold} × {knight_multiplier} = {total_gold}"
                msg += f"\n<i>🥩Твоя еда:</i> {food_for_you} "
                msg += f"\n<i>🥩Еда для детей:</i> {food_for_kids} 🏆"

                self.conn.execute(
                    "UPDATE users SET food = food + ?, food_for_kids = food_for_kids + ?, last_hunt_time = ?, gold = gold + ? WHERE user_id = ?",
                    (food_for_you, food_for_kids, now, total_gold, user_id)
                )
            bot.send_message(user_id, msg, parse_mode="HTML")

            if user[7] == 1:
                time.sleep(2)
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                markup.add("Профиль", "Охота", "Построить дом")

                if total_points < 20:
                    bot.send_message(user_id, """*Бог:* Мда... Не очень конечно сегодня охота вышла, но ничего, Ещё научишся. Теперь тебе стоит подумать о строительстве твоего дома.""", parse_mode="Markdown")
                else:
                    bot.send_message(user_id, """*Бог:* Хорошая охота, сын мой. Ты показал, что способен выжить. Теперь тебе стоит подумать о строительстве твоего дома.""", parse_mode="Markdown")

                time.sleep(2)
                self.conn.execute("UPDATE users SET story = 2 WHERE user_id = ?", (user_id,))
                bot.send_message(user_id, """*Бог:* Построй себе дом. Для этого тебе понадобятся 8🏅 15🪵 и 13🪨. Нажми на кнопку *Построить дом* в меню""", parse_mode="Markdown", reply_markup=markup)

        finally:
            self.conn.execute("UPDATE users SET interaction = false WHERE user_id = ?", (user_id,))

       
    def house(self, message): 
     user_id = message.chat.id
     user = self.select_user(message)
     if user:
        if user[13]:  
            return
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
                bot.send_message(user_id, f"🏠 *Дом *\n\n Следующий уровень: *{house_lvl + 1}*\n 💰 Золото: {gold_cost} (у вас: {gold})\n 🌲 Дерево: {wood_cost} (у вас: {wood})\n🪨 Камень: {stone_cost} (у вас: {stone})\n\n ❌ Не хватает ресурсов", parse_mode="Markdown")
             
                return
            else:
                bot.send_message(user_id, f"🏠 *Дом*\n\n Следующий уровень: *{house_lvl + 1}*\n 💰 Золото: {gold_cost} (у вас: {gold})\n 🌲 Дерево: {wood_cost} (у вас: {wood})\n🪨 Камень: {stone_cost} (у вас: {stone})\n\n", parse_mode="Markdown", reply_markup=markupp)
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
        user = self.select_user(call)
        if user:
         if user[13]:  
            return
        cur.execute('''SELECT u.gold, u.wood, u.stone, u.house_lvl, u.story,
                        h.gold_cost, h.wood_cost, h.stone_cost FROM users u
                        INNER JOIN house h ON u.house_lvl + 1 = h.level
                        WHERE u.user_id = ?''', (user_id,))
        data = cur.fetchone()

        if data:
            gold, wood, stone, house_lvl, story, gold_cost, wood_cost, stone_cost = data

            if gold < gold_cost or wood < wood_cost or stone < stone_cost:
                bot.send_message(user_id, "❌ У тебя недостаточно ресурсов!")
                return

            cur.execute("""
                UPDATE users
                SET gold = gold - ?, wood = wood - ?, stone = stone - ?, house_lvl = house_lvl + 1
                WHERE user_id = ?
            """, (gold_cost, wood_cost, stone_cost, user_id))
            self.conn.commit()

            bot.send_message(user_id, f"🎉 Вы построили дом уровня {house_lvl + 1}!\nВаш баланс: 🏅 {gold - gold_cost}, 🪵 {wood - wood_cost}, 🪨 {stone - stone_cost}")
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
                markup.add("Профиль", "Охота", "Улучшить дом", "Путешествие", "Артефакты", "Поселение", "Продолжить сюжет")
                cur.execute("UPDATE users SET story = 9 WHERE user_id = ?", (user_id,))
                bot.send_message(user_id, "Вы можете продолжить сюжет (нажмите в меню)", reply_markup=markup)
            elif house_lvl + 1 == 5:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                markup.add("Профиль", "Охота", "Улучшить дом", "Путешествие", "Артефакты", "Поселение", "Продолжить сюжет")
                cur.execute("UPDATE users SET story = 11 WHERE user_id = ?", (user_id,))
                bot.send_message(user_id, "Вы можете продолжить сюжет (нажмите в меню)", reply_markup=markup)

    def handle_zombie(self, message):
       user = self.select_user(message)
       if user[10] == user[11]:
           return True
       else:
          return False
    
    def understand(self,call):
       if hasattr(call, "message"):
        user_id = call.message.chat.id
       else: 
        user_id = call.chat.id

       with self.conn:
          cur = self.conn.cursor()
          cur.execute("UPDATE users SET understand = 1 WHERE user_id = ?", (user_id,))
    
    def understand2(self,call):
       if hasattr(call, "message"):
        user_id = call.message.chat.id
       else:  
        user_id = call.chat.id
     
       with self.conn:
          cur = self.conn.cursor()
          cur.execute("UPDATE users SET understand = 2 WHERE user_id = ?", (user_id,))

    def get_user_pickaxe(self, user_id):
        cur = self.conn.cursor()
        cur.execute("""
            SELECT users.*, 
                COALESCE(
                    CASE users.lvlstone
                        WHEN 0 THEN population_boosts.lvl0boost
                        WHEN 1 THEN population_boosts.lvl1boost
                        WHEN 2 THEN population_boosts.lvl2boost
                        WHEN 3 THEN population_boosts.lvl3boost
                        WHEN 4 THEN population_boosts.lvl4boost
                    END, 1
                ) as stone_multiplier
            FROM users 
            LEFT JOIN population_boosts 
                ON population_boosts.boost = 'Кирка'
            WHERE users.user_id = ?;
        """, (user_id,))
        stone_multiplier = cur.fetchone()
        return stone_multiplier 
    
    def get_user_axe(self, user_id):
        cur = self.conn.cursor()
        cur.execute("""
            SELECT users.*, 
                COALESCE(
                    CASE users.lvlwood
                        WHEN 0 THEN population_boosts.lvl0boost
                        WHEN 1 THEN population_boosts.lvl1boost
                        WHEN 2 THEN population_boosts.lvl2boost
                        WHEN 3 THEN population_boosts.lvl3boost
                        WHEN 4 THEN population_boosts.lvl4boost
                    END, 1
                ) as wood_multiplier
            FROM users 
            LEFT JOIN population_boosts 
                ON population_boosts.boost = 'Топор'
            WHERE users.user_id = ?;
        """, (user_id,))
        wood_multiplier = cur.fetchone()
        return wood_multiplier 
    
    def get_user_knight(self, user_id):
        cur = self.conn.cursor()
        cur.execute("""
            SELECT users.*, 
                COALESCE(
                    CASE users.lvlgold
                        WHEN 0 THEN population_boosts.lvl0boost
                        WHEN 1 THEN population_boosts.lvl1boost
                        WHEN 2 THEN population_boosts.lvl2boost
                        WHEN 3 THEN population_boosts.lvl3boost
                        WHEN 4 THEN population_boosts.lvl4boost
                    END, 1
                ) as gold_multiplier
            FROM users 
            LEFT JOIN population_boosts 
                ON population_boosts.boost = 'Оружие для защиты от зомби'
            WHERE users.user_id = ?;
        """, (user_id,))
        gold_multiplier = cur.fetchone()
        return gold_multiplier 
    
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
        chance = 4
     elif house_level == 5:
        chance = 5
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
        if user:
            if user[13]:
             return
        cur.execute("UPDATE users SET interaction = true WHERE user_id = ?", (user_id,))

        if user[7] < 3:
            bot.send_message(user_id, "Ты ещё не можешь путешествовать.")
            cur.execute("UPDATE users SET interaction = false WHERE user_id = ?", (user_id,))
            return

        if user[3] < 20:
            bot.send_message(user_id, f"Ты голодный, нужно минимум 20 единиц 🍖, а у тебя их {user[3]}")
            cur.execute("UPDATE users SET interaction = false WHERE user_id = ?", (user_id,))
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

        if user[7] == 3:
            markup = types.InlineKeyboardMarkup()
            _understand = types.InlineKeyboardButton("Понятно", callback_data="understand")
            markup.add(_understand)
            rule = bot.send_message(user_id, "Каждый раз у зомби открытое место. Нажми на правильную кнопку. Если нажмёшь правильно — урон зомби, иначе — урон тебе. Каждый раз у тебя есть 3 секунды на раздумку", reply_markup=markup, parse_mode="Markdown")
            rule_id = rule.message_id
            for i in range(15):
                time.sleep(1)
                user = self.select_user(message)

                if user[20] == 1:
                    cur.execute("UPDATE users SET understand = 0 WHERE user_id = ?", (user_id,))
                    break
                if i == 14:
                    bot.send_message(user_id, "Ладно, я надеюсь ты понял")
                    time.sleep(1)

            try:
                bot.edit_message_reply_markup(chat_id=user_id, message_id=rule_id, reply_markup=None)  
            except Exception:
                pass
                
            bot.send_message(user_id, "Итак, начнём:")
            
        for event in event_list:

            if event == "Zombie":
                zombie_hp = random.randint(2, 6)
                zombie_hp_start = zombie_hp
                weak_spots = ["Голова", "Печень", "Грудь", "Нога"]
                target_weak_spot = ""
                bot.send_message(user_id, "На вас напал зомби🧟‍♂, защишайтесь!")

                markup = types.InlineKeyboardMarkup(row_width=2)
                buttons = [
                        types.InlineKeyboardButton("Голова", callback_data="head"),
                        types.InlineKeyboardButton("Грудь", callback_data="chest"),
                        types.InlineKeyboardButton("Печень", callback_data="liver"),
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
                      cur.execute("UPDATE users SET weak_spot = ? WHERE user_id = ?", (target_weak_spot, user_id))
                      time.sleep(3)
                 if zombie_hp == 0:
                    gold = zombie_hp_start // 2
                    if gold == 0 or gold >= 5:
                      kusok = 'кусочков'
                    if gold == 1:
                       kusok = 'кусочек'
                    else:
                      kusok = 'кусочка'
                    bot.send_message(user_id, f"🏆 Победа! Ты получил {gold} {kusok} золота.")
                    sus = None
                    cur.execute("UPDATE users SET weak_spot = ?, call_data = ? WHERE user_id = ?", (sus, sus, user_id))
                    extracted_gold += gold
                    killed_zombies += 1 
                    break
                 elif player_hp == 0:
                    sus = None
                    bot.send_message(user_id, "💀 Ты проиграл! Зомби прокусил твои доспехи, ты не получаешь заработанные награды.")

                    cur.execute("UPDATE users SET weak_spot = ?, call_data = ? WHERE user_id = ?", (sus, sus, user_id))
                    time.sleep(2)
                    cur.execute("""UPDATE users
                      SET food = food - 20
                      WHERE user_id = ?
                      """, (user_id,))
                
            
                markup = types.InlineKeyboardMarkup(row_width=2)
                buttons = [
                        types.InlineKeyboardButton("Голова", callback_data="head"),
                        types.InlineKeyboardButton("Грудь", callback_data="chest"),
                        types.InlineKeyboardButton("Печень", callback_data="liver"),
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
                      cur.execute("UPDATE users SET weak_spot = ? WHERE user_id = ?", (target_weak_spot, user_id))
                      time.sleep(3)
                 if zombie_hp == 0:
                    gold = zombie_hp_start // 2
                    if gold == 0 or gold >= 5:
                      kusok = 'кусочков'
                    if gold == 1:
                       kusok = 'кусочек'
                    else:
                      kusok = 'кусочка'
                    bot.send_message(user_id, f"🏆 Победа! Ты получил {gold} {kusok} золота.")
                    sus = None
                    cur.execute("UPDATE users SET weak_spot = ?, call_data = ? WHERE user_id = ?", (sus, sus, user_id))
                    extracted_gold += gold
                    killed_zombies += 1 
                    break
                 elif player_hp == 0:
                    sus = None
                    bot.send_message(user_id, "💀 Ты проиграл! Зомби прокусил твои доспехи, ты не получаешь заработанные награды.")

                    cur.execute("UPDATE users SET weak_spot = ?, call_data = ? WHERE user_id = ?", (sus, sus, user_id))
                    time.sleep(2)
                    cur.execute("""UPDATE users
                      SET food = food - 20
                      WHERE user_id = ?
                      """, (user_id,))
                    if user[7] == 3:
                     cur.execute(""" UPDATE users SET story = 4, understand = 0 WHERE user_id = ? """,(user_id,))
                     bot.send_message(user_id, "*Бог: * К сожалению, ты не победил зомби. Но не переживай, это только начало...", parse_mode="Markdown")
                    cur.execute("UPDATE users SET interaction = false WHERE user_id = ?", (user_id,))
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
      
        if user[9] <= 2:
            summary = (
                f"🌍 Приключение окончено!\n"
                f"🧟 Убито зомби: {killed_zombies}\n"
                f"🏅 Найдено золота: {extracted_gold} \n"
                f"🌲 Найдено дерева: {extracted_wood}\n"
                f"🪨 Найдено камня: {extracted_stone}\n"
                f"🍖 -20 еды"
            )
            cur.execute("""
                UPDATE users
                SET gold = gold + ?, wood = wood + ?, stone = stone + ?, food = food - 20
                WHERE user_id = ?
            """, (extracted_gold, extracted_wood, extracted_stone, user_id))
        elif user[9] >= 3:
           user_mult_k = self.get_user_knight(user_id)
           knight_multiplier = user_mult_k[-1] or 1
           total_gold_noInt = extracted_gold * knight_multiplier
           total_gold = int(total_gold_noInt)
           
           user_mult_a = self.get_user_axe(user_id)
           axe_multiplier = user_mult_a[-1] or 1
           total_wood_noInt = extracted_wood * axe_multiplier
           total_wood = int(total_wood_noInt)

           user_mult_p = self.get_user_pickaxe(user_id)
           pickaxe_multiplier = user_mult_p[-1] or 1
           total_stone_noInt = extracted_stone * pickaxe_multiplier
           total_stone = int(total_stone_noInt)

           summary = (          
                f"🌍 Приключение окончено!\n"
                f"🧟 Убито зомби: {killed_zombies}\n"
                f"🏅 Найдено золота: {extracted_gold} × {knight_multiplier} = {total_gold} \n"
                f"🌲 Найдено дерева: {extracted_wood} × {axe_multiplier} = {total_wood}\n"
                f"🪨 Найдено камня: {extracted_stone} × {pickaxe_multiplier} = {total_stone}\n"
                f"🍖 -20 еды"
            )
           cur.execute("""
                UPDATE users
                SET gold = gold + ?, wood = wood + ?, stone = stone + ?, food = food - 20
                WHERE user_id = ?
            """, (total_gold, total_wood, total_stone, user_id))
                     
        bot.send_message(user_id, summary)
        cur.execute("UPDATE users SET interaction = false, call_data = NULL, weak_spot = NULL WHERE user_id = ?", (user_id,))
        if user[7] == 3:
           time.sleep(2)
           cur.execute("""
            UPDATE users
            SET story = 4
            WHERE user_id = ?
        """, (user_id,))
           bot.send_message(user_id, "*Бог: * Хорошее было сегодня приключение, воин! Ты сражался достойно и вернулся с добычей. Я оставлю тебя на время, иди на охоту, строй дома и развивайся, потом увидишь как судьба с тобой поиграет...", parse_mode="Markdown")    
      

    def story_lvl2(self, message):
       user_id = message.chat.id
       user = self.select_user(message)
       if user:
        if user[13] == True:
            return
       with self.conn:
          cur = self.conn.cursor()
          cur.execute("UPDATE users SET story = 5, understand = 0, interaction = true WHERE user_id = ?", (user_id,))
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
             bot.send_message(user_id, "*Проф. Иван Золо: * Дорогой человек, от всего серда благодарю тебя за спасение моей жизни! Меня зовут профессор иван золо, я учённый в области биологии и я очень хочу поставить точку над этим вирусом, но для этого мне нужны определённые артефакты. Впусти меня в свой дом, у меня собой гостинцы есть.", parse_mode="Markdown", reply_markup=markup)
    def story_ivan_let_in(self, message):
             user_id = message.chat.id        
             bot.send_message(user_id, "<i>Вам зачисленно: </i> +15🍖", parse_mode="HTML")
             time.sleep(2)
             markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
             markup.add("Профиль", "Охота", "Улучшить дом", "Путешествие", "Артефакты")
             bot.send_message(user_id, "*Проф. Иван Золо: * Вобщем, чтобы помочь мне, ты когда путешествовать будешь, передавай артефакты мне, кстати список артефактов ты можешь найти в меню, в каталоге артефакты.", parse_mode="Markdown", reply_markup=markup)
             with self.conn:
              cur = self.conn.cursor()
              cur.execute("UPDATE users SET story = 6, interaction = false WHERE user_id = ?", (user_id,))             
              Zolik = f"C:\\Users\\Admin\\OneDrive\\Desktop\\simulator\\images\\mrZolo.jpg"
              if os.path.exists(Zolik):
                with open(Zolik, "rb") as f:
                    bot.send_photo(user_id, f)

    def story_lvl3(self, message):        
       user_id = message.chat.id
       user = self.select_user(message)
       if user:
        if user[13]:
            return
       with self.conn:
        cur = self.conn.cursor()
        cur.execute("UPDATE users SET interaction = true, understand = 0 WHERE user_id = ?", (user_id,))
        bot.send_message(user_id, "*Проф. Иван Золо: * Поздравлю тебя с нашим новым тобой постройленным домом. Соответственно я расширил мои исследования и я понял какие нам артефакты ещё нуж... Погоди, ты это слышишь?", parse_mode="Markdown")
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
       bot.send_message(user_id, "*Мария Ивановна: *Здраствуйте, меня зовут Мария Ивановна, раньше я была учительницой математики, но из-за зомби апокалипсиса я потеряла всё что у меня есть включая мою семью. Впустите меня пожалуйста в дом.", parse_mode="Markdown")
       matematichka = f"C:\\Users\\Admin\\OneDrive\\Desktop\\simulator\\images\\matematichka.jpg"
       if os.path.exists(matematichka):
        with open(matematichka, "rb") as f:
          bot.send_photo(user_id, f, reply_markup=markup)

    def Ivan_Dora_plan(self, message):
       user_id = message.chat.id 
       markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
       markup.add("Профиль", "Охота", "Улучшить дом", "Путешествие", "Артефакты", "Поселение")
       bot.send_message(user_id, "*Проф. Иван Золо:* Здравствуйте, я очень рад за вас что вы выжили, вы нам как раз очень нужны.",parse_mode="Markdown")
       time.sleep(3)
       bot.send_message(user_id, """*Проф. Иван Золо к тебе:* Так, коллега у меня есть план: Нам нужно развить цивилизацию людей чтобы побороть этот вирус усилиями наших потомков. Поэтому ты должен каждый раз после охоты делиться с нами 30% едой,а мы в это время с Дорой будет продуцировать новый людей. Они тем временем будут становиться всё умнее и будут развиваться и ты можешь будешь с ихней помощью улучшать своё оружие которое поможет тебе добывать больше ресурсов. А за поселением ты можешь следить спомощью кнопки *поселение*. Я надесь ты всё понял, а теперь иди на охоту, не терпится когда ты уже уйдёшь)""", parse_mode="Markdown", reply_markup=markup)
       with self.conn:
        cur = self.conn.cursor()
        cur.execute("UPDATE users SET story = 8, interaction = false WHERE user_id = ?", (user_id,))
       dorazolo = f"C:\\Users\\Admin\\OneDrive\\Desktop\\simulator\\images\\ZoloDora.jpg"
       if os.path.exists(dorazolo):
        with open(dorazolo, "rb") as f:
          bot.send_photo(user_id, f)
    
    def story_lvl4(self, message):      
       user_id = message.chat.id
       user = self.select_user(message)
       if user:
        if user[13]:
            return
       markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
       markup.add("Профиль", "Охота", "Улучшить дом", "Путешествие", "Артефакты", "Поселение")
       bot.send_message(user_id, "*Проф. Иван Золо: * Молодец что смог улучшить дом, благодаря тебе я продвинул свои иследования ещё дальше. Кстати, тебе открылись ещё по 2 уровня на каждом уровне прокачки твоего оружия. Поверь мне, нам осталось ещё немного", parse_mode="Markdown", reply_markup=markup)
       Zolik4 = f"C:\\Users\\Admin\\OneDrive\\Desktop\\simulator\\images\\zolik4lvl.jpg"
       if os.path.exists(Zolik4):
        with open(Zolik4, "rb") as f:
          bot.send_photo(user_id, f)
        
       with self.conn:
        cur = self.conn.cursor()
        cur.execute("UPDATE users SET story = 10 WHERE user_id = ?", (user_id,))

    def story_lvl5(self, message):
       user_id = message.chat.id
       user = self.select_user(message)
       if user:
        if user[13]:
            return
        with self.conn:
           cur = self.conn.cursor()
           cur.execute("UPDATE users SET interaction = true  WHERE user_id = ?", (user_id,))
       markup = types.InlineKeyboardMarkup()
       ok = types.InlineKeyboardButton("Выйти на охоту", callback_data="HuntWithZolo")
       markup.add(ok)
       population = user[14]
       Zolik5 = f"C:\\Users\\Admin\\OneDrive\\Desktop\\simulator\\images\\zolikAndDora5lvl.jpg"
       if os.path.exists(Zolik5):
        with open(Zolik5, "rb") as f:
          bot.send_photo(user_id, f)
       if population >= 8:
        bot.send_message(user_id, f"*Проф. Золо:* Эх, друг мой, смотри как жизнь налаживается, осталось буквально найти последний артефакт, который поможет восстановаить цивилизацию и вылечить всех людей на этой земле, да и с Дорой у нас дела хорошо идут, посмотри как мы развили наше поселение, аж {population} человек! Я тут заметил, уж что то слишком долго меня на свежем воздухе не было, уж сликом я работал много, давай ка по братский пойдем все вместе на охоту? ",reply_markup=markup, parse_mode="Markdown")
       else:
        bot.send_message(user_id,  f"*Проф. Золо:* Эх, друг мой, смотри как жизнь налаживается, осталось буквально найти последний артефакт, который поможет восстановаить цивилизацию и вылечить всех людей на этой земле! Я тут заметил, уж что то слишком долго меня на свежем воздухе не было, уж сликом я работал много, давай ка по братский пойдем все вместе на охоту?", reply_markup=markup, parse_mode="Markdown")

    def hunt_with_zolik(self, message):
       user_id = message.chat.id
       user = self.select_user(message)
       with self.conn:
         cur = self.conn.cursor()
         cur.execute("UPDATE users SET understand = 0 WHERE user_id = ?", (user_id,))
         bot.send_message(user_id, "🏹 Вы отправились на охоту с профессором Золо и Дорой...")
         time.sleep(1.5)
         bot.send_message(user_id, "*Проф. Золо:* Ты слышишь этот звук? Это помоему слишком слишком сильное рычание для обычного зверя!", parse_mode="Markdown")
         time.sleep(3)
         bot.send_message(user_id, "_Зомби выходит из деревьев и рычит:_", parse_mode="MarkdownV2")
         time.sleep(1.5)
         bot.send_message(user_id, "*АААААААРГХХХХХХ!*", parse_mode="Markdown")
         zombie = f"C:\\Users\\Admin\\OneDrive\\Desktop\\simulator\\images\\zombiemutant.jpg"
         if os.path.exists(zombie):
          with open(zombie, "rb") as f:
           bot.send_photo(user_id, f)
         time.sleep(3)
         bot.send_message(user_id, "*Дора:* АААААААА УЛЕТАЕМ НА ГАИТИ", parse_mode="Markdown")
         doragaity = f"C:\\Users\\Admin\\OneDrive\\Desktop\\simulator\\images\\doragaity.mp4"
         if os.path.exists(doragaity):
            try:
                with open(doragaity, "rb") as f:
                    bot.send_video(user_id, f, timeout=90) 
            except Exception as e:
                print(f"Error: {e}")
                bot.send_message(user_id, "(Не получается скинуть видео изза нестабильного интернета)")
         time.sleep(3)
         markup = types.InlineKeyboardMarkup()
         no_blyat = types.InlineKeyboardButton("Без матов🤫", callback_data="WithoutBadWords")
         blyat = types.InlineKeyboardButton("С матами🤬", callback_data="WithBadWords")
         markup.add(no_blyat, blyat)
         attention = bot.send_message(user_id, "*Внимание:* Ты можешь выбрать продолжение без матов и с матами (*НЕ* влияет на сюжет)!", parse_mode="Markdown", reply_markup=markup)
         attention_id = attention.message_id
         godrock = f"C:\\Users\\Admin\\OneDrive\\Desktop\\simulator\\images\\godrock.jpg"
         if os.path.exists(godrock):
          with open(godrock, "rb") as f:
           bot.send_photo(user_id, f)
         bl = 0
         for i in range(120):
            time.sleep(1)
            
            user = self.select_user(message)
            if user[20] in (1, 2):
                bl = user[20]
                try:
                    bot.edit_message_reply_markup(chat_id=user_id, message_id=attention_id, reply_markup=None)
                except Exception:
                    pass  
                time.sleep(1)
                break
            if i == 119:
          
                cur.execute("UPDATE users SET understand = 1 WHERE user_id = ?", (user_id,))
                bl = user[20]
                bot.send_message(user_id, "На всякий случай поставлю без матов чтобы грех не совершать☝️")
                try:
                    bot.edit_message_reply_markup(chat_id=user_id, message_id=attention_id, reply_markup=None)
                except Exception:
                    pass  
                time.sleep(1)
            
         if bl == 1:
           time.sleep(2)
           bot.send_message(user_id, "*Ты в мыслях:* Почему она улетела сама а нас оставила здесь, это же предательство!", parse_mode="Markdown")
         elif bl == 2:
             Jesus = f"C:\\Users\\Admin\\OneDrive\\Desktop\\simulator\\images\\Jesus.jpg" 
             if os.path.exists(Jesus):
              with open(Jesus, "rb") as f:
               bot.send_photo(user_id, f)

             time.sleep(2)

             bot.send_message(user_id, "*Ты в мыслях:* БЛЯТЬ СУКА ЕБАННАЯ! Почему блять она улетела сама а нас нахуй здесь оставила! Предательница!", parse_mode="Markdown")
         
         time.sleep(4)    
         
         bot.send_message(user_id, "*Проф. Золо:* Дора, любимая я спасу тебя!", parse_mode="Markdown")
         
         time.sleep(3)

         bot.send_message(user_id, "_Зомби кусает Ивана:_", parse_mode="Markdown")

         time.sleep(2)
         
         match bl: 
             case 1:
                 bot.send_message(user_id, "*Проф. Золо:* АЙ БОЛЬНО!", parse_mode="Markdown")
             case 2:
                 bot.send_message(user_id, "*Проф. Золо:* АЙ БЛЯТЬ СУКА!!!", parse_mode="Markdown")
         
         time.sleep(3)

         bot.send_message(user_id, "_Проф. Золо превращается в зомби_", parse_mode="Markdown")

         time.sleep(3)
         markup = types.InlineKeyboardMarkup()
         weapon = types.InlineKeyboardButton("Достать оружие", callback_data="take_weapon")
         markup.add(weapon)
         match bl: 
             case 1:
                 bot.send_message(user_id, "*Ты:* Идиот! У меня оружие было! Зачем ты полез к нему?! Ай дурак!", parse_mode="Markdown", reply_markup=markup)
             case 2:
                 bot.send_message(user_id, "*Ты:* ДАУН КОЧЕННЫЙ! У меня оружие было! Нахуя ты блять полез к нему?! Не профессор а долбоёб какой то!", parse_mode="Markdown", reply_markup=markup)
            
    def zolo_is_dead(self, message):
       user_id = message.chat.id
       user = self.select_user(message)
       bl = user[20]

       match bl: 
             case 1:
                 bot.send_message(user_id, "*Ты:* Получай зомби мутант!", parse_mode="Markdown")
             case 2:
                 bot.send_message(user_id, "*Ты:* На нахуй зомби мутант ебанный!!!", parse_mode="Markdown")
         
       mutant = f"C:\\Users\\Admin\\OneDrive\\Desktop\\simulator\\images\\mutantDead.jpg" 
       if os.path.exists(mutant):
          with open(mutant, "rb") as f:
            bot.send_photo(user_id, f)
        
       time.sleep(2)

       bot.send_message(user_id, "_Ты связываешь Ивана Золо и забираешь его на базу_ ", parse_mode="Markdown")

       zoloZombie = f"C:\\Users\\Admin\\OneDrive\\Desktop\\simulator\\images\\ZoloDead.jpg" 
       if os.path.exists(zoloZombie):
          with open(zoloZombie, "rb") as f:
            bot.send_photo(user_id, f)
       
       time.sleep(2)
       bot.send_message(user_id, "_Ты возвращаешься домой_ ", parse_mode="Markdown")

       house = f"C:\\Users\\Admin\\OneDrive\\Desktop\\simulator\\images\\lvl5.jpg" 
       try:
            if os.path.exists(house):
                with open(house, "rb") as f:
                 bot.send_photo(user_id, f)
            else:
                print(f"Картинка не найдена: {house}")
       except Exception as e:
         print(f"Error: {e}")
       
       time.sleep(2.5)
       bot.send_message(user_id, "_Дора находится уже на базе_", parse_mode="Markdown")
       time.sleep(2)
       bot.send_message(user_id, "*Дора:* Ну наконец то он умер! А то я уже устала от этого карлика с карликом", parse_mode="Markdown")
       time.sleep(2)
       bot.send_message(user_id, "_Дора плавно лезит к тебе вниз_", parse_mode="Markdown")
       time.sleep(2)
       bot.send_message(user_id, "*Дора:* А теперь мы проверим, карлик ли у тебя или нет😈", parse_mode="Markdown")
       dora_horny = f"C:\\Users\\Admin\\OneDrive\\Desktop\\simulator\\images\\doraHorny.jpg"
       if os.path.exists(dora_horny):
          with open(dora_horny, "rb") as f:
            markup = types.InlineKeyboardMarkup()
            stop_mne_nepriatno = types.InlineKeyboardButton("✋ Остановить Дору", callback_data="stop_dora")
            markup.add(stop_mne_nepriatno)
            bot.send_photo(user_id, f, reply_markup=markup)

    def stop_dora(self, message):
        user_id = message.chat.id
        user = self.select_user(message)
        bot.send_message(user_id, "*Ты:* Стоп, мне неприятно! Я всегда был лоялен к Ване и останусь лояльным, даже если он сейчас зомби!", parse_mode="Markdown") 
        time.sleep(3)
        bot.send_message(user_id, "*Ты:* Ты доигралась Дора! Я выкину тебя из этого дома, и тебя съедят зомби", parse_mode="Markdown")       
        time.sleep(2)
        bot.send_message(user_id, "*Дора:* НЕТ! Ты не можешь выкинуть меня просто, если ты убьёшь меня, то ты не узнаешь что тебе нужно будет сделать, чтобы спасти мир!", parse_mode="Markdown") 
        time.sleep(4)   
        bot.send_message(user_id, "*Ты:* И что же мне нужно будет сделать?", parse_mode="Markdown")
        time.sleep(2)  
        markup = types.InlineKeyboardMarkup()
        listen_dora = types.InlineKeyboardButton("Выслушать Дору", callback_data="listen_dora")  
        markup.add(listen_dora)
        bot.send_message(user_id, "*Дора:* Перед тем, как кидать меня на произвол судьбы, выслушай меня  внимательно, Иванушка разказал мне всё, что он планировал сделать:", parse_mode="Markdown", reply_markup=markup)

    def dora_in_prison(self, message):
        user_id = message.chat.id
        user = self.select_user(message)
        bot.send_message(user_id, "*Дора:* И так, чтобы сделать сыворотку от вируса, нам осталось собрать только 2 артефакта, а именно иголку Лирили Ларила и бомбу Бомбардиро крокодило, дальше нам нужно будет смешать все артефакты в лабаратории профессора Ивана Золо, дальше Профессор золо скопирует сыворотку до поизводственного количества и сбросит её по всему миру, так мы сможем спасти весь мир, только пожалуйста не бросай меня к зомби", parse_mode="Markdown")
        time.sleep(10)
        bot.send_message(user_id, "*Дора:* Теперь делай со мной что хочешь", parse_mode="Markdown")
        time.sleep(3)
        bot.send_message(user_id, "*Ты:* Значит так, за предательство Ивана Золо, мне придётся принять меры, и моё решение кинуть тебя в подвал и будешь ты жить рядом с клеткой Ивана, пока я не найду последний артефакт, а дальше уже сам Ваня решит, по каким рельсам пойдёт твоя судьба дальше", parse_mode="Markdown")
        time.sleep(8)
        prison = "C:\\Users\\Admin\\OneDrive\\Desktop\\simulator\\images\\prison.png"
        if os.path.exists(prison):
                with open(prison, "rb") as f:
                  bot.send_photo(user_id, f)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("Профиль", "Охота", "Путешествие", "Артефакты", "Концовка")
        bot.send_message(user_id, "_Когда ты соберерёшь все артефакты нажми в меню на «Смешать артефакты» чтобы спасти Ивана Золо_", parse_mode="Markdown", reply_markup=markup)

        with self.conn:
                cur = self.conn.cursor()
                cur.execute("UPDATE users SET story = 12, interaction = 0 WHERE user_id = ?", (user_id,))

        # продолжение следует


  
        
    def get_user_artifacts(self, user_id):
     with self.conn:
        user = self.select_user_by_id(user_id) 
        if user:   
         if user[13]:
          return
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

        cur.execute("SELECT house_lvl FROM users WHERE user_id = ?", (user_id,))
        row = cur.fetchone()
        house_level = row[0] if row else 1

        if house_level == 2:
            chance_text = "1 из 2 (50%)"
        elif house_level == 3:
            chance_text = "1 из 3 (~33%)"
        elif house_level == 4:
            chance_text = "1 из 4 (25%)"
        elif house_level >= 5:
            chance_text = "1 из 5 (20%)"
        else:
            chance_text = "Нет шанса (нужен дом выше)"
        
        result = "*🗿 Ваши артефакты:*\n"
        if owned:
            result += "\n".join([f"• {item}" for item in owned])
        else:
            result += "У тебя пока нет артефактов."

        result += f"\n\n*🎯 Шанс найти новый артефакт:* {chance_text}\n"

        result += "\n\n*Доступные артефакты для твоего уровня:*\n"
        if available:
                result += "\n".join([f"• {item}" for item in available])  
        else:
            result += "🎉 Ты уже собрал все доступные артефакты для своего уровня!"

        bot.send_message(user_id, result, parse_mode="Markdown")
    
    def population(self, message):
        user_id = message.chat.id
        user = self.select_user(message)
        if user[13]:
            return

        firearms, pickaxe, axe, knight = self.lvl_weapons(user)

        with self.conn:
            cur = self.conn.cursor()
            markup = types.InlineKeyboardMarkup()
            make_incest = types.InlineKeyboardButton("Увеличить поселение", callback_data="incest")
            boost_level = types.InlineKeyboardButton("Улучшить оружие", callback_data="boost_lvl")
            markup.add(make_incest, boost_level)
            
            food_for_kids = user[12]
            kids = user[14]
            for_improvement = user[15]

            bot.send_message(
                user_id,
                f"*👥Твоё поселение: {kids}  *\n\n"
                f"*🥩Еда для поселения: {food_for_kids} * \n"
                f"*❌️Безработные: {for_improvement} *\n\n"

                f"🏹Для охоты: *{firearms}* (ур. *{user[16]}*) \n"
                f"⛏️Для камня: *{pickaxe}* (ур. *{user[17]}*) \n"
                f"🪓Для дерева: *{axe}* (ур. *{user[18]}*) \n"
                f"🗡От зомби: *{knight}* (ур. *{user[19]}*)",
                reply_markup=markup, parse_mode="Markdown"
            )

    def incest(self, call):
       user_id = call.chat.id
       user = self.select_user(call)
       if user:
        if user[13]:
         return
        
       with self.conn:
          cur = self.conn.cursor()
          food = user[12]
          people = food // 5 
          rest_food = food % 5

          if food < 5:
            bot.send_message(user_id, "❌ Недостаточно еды для создания новых людей (нужно минимум 5).")
            return
          
          new_people_for_improvement = user[15] + people
          total_people = user[14] + people

          cur.execute("""
            UPDATE users 
            SET food_for_kids = ?, 
                avaible_people_for_improvement = ?, 
                total_people = ? 
            WHERE user_id = ?
            """, (rest_food, new_people_for_improvement, total_people, user_id))
          bot.send_message(user_id, f"🍗 Использовано {food - rest_food} еды.\n👶 Получено {people} новых поселенцев.\n ❌️Всего безработных: {new_people_for_improvement} \n🍗 Остаток еды: {rest_food}.")
    
    def shop(self, call):
        user_id = call.chat.id
        user = self.select_user(call)
        if not user:
            bot.send_message(user_id, "Вы не зарегистрированы, напишите /start")
            return
        
        if user[13]:
            return
        
        with self.conn:
            cur = self.conn.cursor()
            if user[9] >= 3:
                firearms, pickaxe, axe, knight = self.lvl_weapons(user)

                weapon_mapping = {
                    'lvlfood': (16, 'Оружие для охоты', firearms),
                    'lvlstone': (17, 'Кирка', pickaxe),
                    'lvlwood': (18, 'Топор', axe),
                    'lvlgold': (19, 'Оружие для защиты от зомби', knight)
                }

                shop_text = "🛒 <b>Улучшения</b>\n\n"
                markup = types.InlineKeyboardMarkup()

                for boost_code, (user_index, boost_id, current_weapon) in weapon_mapping.items():
                    current_level = user[user_index]
                    next_level = current_level + 1
                    max_level = 2 if user[9] == 3 else 4

                    if next_level > max_level:
                        shop_text += f"✅ <b>{boost_id}</b> уже на максимальном уровне.\n\n"
                        continue

                    boost_col = f"lvl{next_level}boost"
                    cost_col = f"lvl{next_level}cost"

                    row = cur.execute(f"""
                        SELECT boost, {boost_col}, {cost_col}
                        FROM population_boosts
                        WHERE boost = ?
                    """, (boost_id,)).fetchone()

                    if not row:
                        continue

                    boost_name, boost_value, cost_value = row
                    weapon_lists = {
                            'lvlfood': [
                                "Лук",
                                "Арбалет",
                                "Пистолет Glock-17",
                                "AK-47",
                                "M134 Миниган"
                            ],
                            'lvlstone': [
                                "Каменная кирка",
                                "Железная кирка Еффективность(I) Удача(I)",
                                "Алмазная кирка Еффективность(III) Удача(II)",
                                "Незеритовая кирка Еффективность(V) Удача(III)",
                                "Бедроковая кирка Еффективность(X) Удача(X)"
                            ],
                            'lvlwood': [
                                "Каменный топор",
                                "Железный топор Еффективность(I) Острота(I)",
                                "Алмазный топор Еффективность(III) Острота(III)",
                                "Незеритовый топор Еффективность(V) Острота(VI)",
                                "Бедроковый топор Еффективность(X) Острота(X)"
                            ],
                            'lvlgold': [
                                "Кинжал",
                                "Меч",
                                "Катана",
                                "Кусаригама",
                                "Опустошитель титана"
                            ]
                        }
                    if next_level < len(weapon_lists[boost_code]):
                        next_weapon_name = weapon_lists[boost_code][next_level]
                    else:
                        next_weapon_name = weapon_lists[boost_code][-1]

                    shop_text += (
                        f"🔹<b>{boost_name}</b>\n"
                        f"🧱 Сейчас у тебя: <i>{current_weapon}</i>\n"
                        f"➡️ Следующее оружие: <b>{next_weapon_name}</b> — Уровень {next_level}\n"                  
                        f"💥 Бонус: <i>{boost_value}</i>\n"
                        f"👤 Нужно людей: <i>{cost_value}</i>\n"
                    )

                    

                    if user[15] >= cost_value:
                        if boost_name == "Оружие для охоты":
                            product = "Огнестрел 🔫"
                        elif boost_name == "Кирка":
                            product = "кирку ⛏️"
                        elif boost_name == "Топор":
                            product = "топор 🪓"
                        elif boost_name == "Оружие для защиты от зомби":
                            product = "холодное оружие 🗡"
                        

                        shop_text += "\n"
                        markup.add(types.InlineKeyboardButton(
                            f"Купить {product}",
                            callback_data=f"buy_{boost_code}"
                        ))
                    else:
                        shop_text += "❌ Недостаточно людей для покупки.\n\n"

                bot.send_message(user_id, shop_text, parse_mode="HTML", reply_markup=markup)
           
 
    def buy_item(self, call):
        boost_code = call.data[4:]
        user_id = call.message.chat.id
        user = self.select_user(call)

        if not user:
            bot.send_message(user_id, "Вы не зарегистрированы, напишите /start")
            return
        
        if user[13]:
            return

        weapon_mapping = {
            'lvlfood': (16, 'Оружие для охоты'),
            'lvlstone': (17, 'Кирка'),
            'lvlwood': (18, 'Топор'),
            'lvlgold': (19, 'Оружие для защиты от зомби')
        }

        if boost_code not in weapon_mapping:
            bot.answer_callback_query(call.id, "Ошибка покупки.")
            return

        user_index, boost_name = weapon_mapping[boost_code]
        current_level = user[user_index]
        next_level = current_level + 1
        max_level = 2 if user[9] == 3 else 4  
        if next_level > max_level:
            bot.answer_callback_query(call.id, f"{boost_name} уже на максимальном уровне!")
            return

        with self.conn:
            cur = self.conn.cursor()
            boost_col = f"lvl{next_level}boost"
            cost_col = f"lvl{next_level}cost"

            row = cur.execute(f"""
                SELECT {boost_col}, {cost_col}
                FROM population_boosts
                WHERE boost = ?
            """, (boost_name,)).fetchone()

            if not row:
                bot.answer_callback_query(call.id, "Ошибка покупки.")
                return

            boost_value, cost_value = row


            if user[15] < cost_value:
                bot.answer_callback_query(call.id, "Недостаточно людей для покупки!")
                return

            new_people = user[15] - cost_value

            cur.execute(f"""
                UPDATE users
                SET {boost_code} = {boost_code} + 1,
                    avaible_people_for_improvement = avaible_people_for_improvement - ?
                WHERE user_id = ?
            """, (cost_value, user[2]))
        if boost_name == "Оружие для охоты":
            product = "Огнестрел 🔫"
        elif boost_name == "Кирка":
            product = "кирку ⛏️"
        elif boost_name == "Топор":
            product = "топор 🪓"
        elif boost_name == "Оружие для защиты от зомби":
            product = "холодное оружие 🗡"
        bot.answer_callback_query(call.id, f"Ты купил {product}!")
        bot.send_message(user_id, f"✅ {boost_name} улучшен до уровня {next_level}!\n👤 Осталось нерабочих: {new_people}")
        sticker_id = self.weapon_stickers.get(boost_name, {}).get(next_level)
        if sticker_id:
         bot.send_sticker(user_id, sticker_id)


                
            
            
        
        
        
