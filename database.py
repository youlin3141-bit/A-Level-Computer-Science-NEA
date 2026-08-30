import sqlite3
def connect():
    return sqlite3.connect("game_storage.db")
def get_username(player_id):
    connection=connect()
    cursor=connection.cursor()
    cursor.execute("""SELECT username FROM players WHERE player_id=?""",(player_id,))
    data=cursor.fetchone()
    cursor.close()
    return data
def get_highest_level(player_id):
    connection=connect()
    cursor=connection.cursor()
    cursor.execute("""SELECT highest_level FROM players WHERE player_id=?""",(player_id,))
    data=cursor.fetchone()
    if not data:
        return 0
    cursor.close()
    connection.close()
    return data[0]
def create_database():
    connection=connect()
    cursor=connection.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS players(
                        player_id INTEGER PRIMARY KEY,
                        username TEXT UNIQUE,
                        highest_level INTEGER DEFAULT 0,
                        password TEXT

        )""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS worlds(
                    world_id INTEGER PRIMARY KEY,
                    player_id INTEGER,
                    
                    player_level INTEGER,
                    difficulty TEXT,
                    currency INTEGER,
                    experience INTEGER,
                    game_level INTEGER,
                    
                    speed FLOAT,
                    damage_upgrade INTEGER,
                    health INTEGER,
                    max_health INTEGER,
                    mace INTEGER,
                    spellbook INTEGER,
                    FOREIGN KEY (player_id) REFERENCES players(player_id)
    )""")

    # cursor.execute("PRAGMA table_info(players)")
    print(cursor.fetchall())
    connection.commit()
    connection.close()
def save_game(game):
    connection=connect()
    cursor=connection.cursor()
    cursor.execute("""UPDATE worlds SET player_level=?,
                    difficulty=?,
                    currency=?,
                    experience=?,
                    game_level=?,
                    speed=?,
                    damage_upgrade=?,
                    health=?,
                    max_health=?,
                    mace=?,
                    spellbook=? WHERE player_id=? AND world_id=?""",(
        game.player.progression.level,
        game.difficulty,
        game.player.progression.currency,
        game.player.progression.xp,
        game.level,
        game.player.speed,
        game.player.damage_upgrade,
        game.player.health,
        game.player.max_health,
        int(game.player_has_item("Mace")),
        int(game.player_has_item("SpellBook")),
        game.player_id,
        game.world_id
    ))
    connection.commit()
    connection.close()

def load_game(player_id,world_id):
    connection=connect()
    cursor=connection.cursor()
    cursor.execute("""SELECT player_level ,
                    difficulty,
                    currency ,
                    experience,
                    game_level,
                    speed,
                    damage_upgrade,
                    health,
                    max_health,
                    mace,
                    spellbook FROM worlds WHERE player_id=? AND world_id=?
                    """,(player_id,world_id))
    data=cursor.fetchone()
    cursor.close()
    return data
def load_all_games(player_id):
    connection=connect()
    cursor=connection.cursor()
    cursor.execute("""SELECT player_level ,
                    difficulty,
                    currency ,
                    experience,
                    game_level,
                    speed,
                    damage_upgrade,
                    health,
                    max_health,
                    mace,
                    spellbook FROM worlds WHERE player_id=?
                    """,(player_id,))
    data=cursor.fetchall()
    cursor.close()
    return data
def get_leaderboard():
    connection=connect()
    cursor=connection.cursor()
    cursor.execute("""SELECT username, highest_level FROM players ORDER BY highest_level DESC limit 50""")
    data=cursor.fetchall()
    cursor.close()
    return data

def count_games(player_id):
    connection=connect()
    cursor=connection.cursor()
    cursor.execute("""SELECT COUNT(*) FROM worlds WHERE player_id=?""", (player_id,))
    count=cursor.fetchone()[0]
    connection.close()
    return count
# def load_game_progress(player_id,world_id):
#     connection = connect()
#     cursor = connection.cursor()
#     cursor.execute("""SELECT difficulty,
#                         game_level,
#                         FROM worlds,
#                         WHERE player_id=? AND world_id?
#                         """, (player_id, world_id))
#     data = cursor.fetchone()
#     cursor.close()
#     return data

def login(username,password):
    connection=connect()
    cursor=connection.cursor()
    cursor.execute("""SELECT player_id
                FROM players
                WHERE username=? AND password=?""",
                   (username,password))
    data=cursor.fetchone()
    connection.close()
    if data:
        return data[0]
    else:
        return None

def create_player(username,password,confirm_password):
    # if not 8<=len(password)<=20:
    #     return False,"Password must be 8-20 characters long"
    if not any(char.isupper() for char in password):
        return False,"Password must contain an uppercase letter"
    if not any(char.isdigit() for char in password):
        return False,"Password must contain a number"
    if password!=confirm_password:
        return False,"Passwords do not match"
    connection=connect()
    cursor=connection.cursor()
    try:
        cursor.execute("""INSERT INTO players
                    (username,password) 
                    VALUES(?,?)""",
        (username,password))
        connection.commit()
        return True,"Account Created"
    except sqlite3.IntegrityError:
        return False,"Username already exists"
    finally:
        connection.close()

def display_players():
    connection=connect()
    cursor=connection.cursor()
    cursor.execute("""SELECT * FROM players""")
    data=cursor.fetchall()
    connection.close()
    return data
def display_game():
    connection=connect()
    cursor=connection.cursor()
    cursor.execute("""SELECT * FROM worlds""")
    data=cursor.fetchall()
    connection.close()
    return data
def create_world(player_id,):
    connection=connect()
    cursor=connection.cursor()
    cursor.execute("""INSERT INTO worlds
                    (player_id)
                   VALUES(?)""",
                   (player_id,))
    connection.commit()
    world_id=cursor.lastrowid
    connection.close()
    return world_id
def get_player_worlds(player_id):
    connection=connect()
    cursor=connection.cursor()
    cursor.execute("""SELECT world_id FROM worlds WHERE player_id=?""", (player_id,))
    data=cursor.fetchall()
    connection.close()
    ids=[]
    for world_id in data:
        ids.append(world_id[0])
    return ids
def delete_worlds(world_id):
    connection=connect()
    cursor=connection.cursor()
    cursor.execute("""DELETE FROM worlds WHERE world_id=?""", (world_id,))
    connection.commit()
    connection.close()
def highest_level(game):
    connection=connect()
    cursor=connection.cursor()
    cursor.execute("""UPDATE players
                    SET highest_level=?
                    WHERE player_id=? and highest_level<?""",(game.level,game.player_id,game.level))
    connection.commit()
    connection.close()
def test_leaderboard():
    connection=connect()
    cursor=connection.cursor()
    cursor.executemany("""
        INSERT INTO players (username, highest_level, password)
        VALUES (?, ?, ?)
    """, [
        ("Player1", 1, "password"),
        ("Player2", 5, "password"),
        ("Player3", 10, "password"),
        ("Player4", 3, "password"),
        ("Player5", 15, "password"),
        ("Player6", 8, "password"),
        ("Player7", 12, "password"),
        ("Player8", 2, "password"),
        ("Player9", 20, "password"),
        ("Player10", 7, "password"),
        ("Player11", 14, "password"),
        ("Player12", 6, "password"),
        ("Player13", 18, "password"),
        ("Player14", 4, "password"),
        ("Player15", 11, "password"),
        ("Player16", 9, "password"),
        ("Player17", 16, "password"),
        ("Player18", 13, "password"),
        ("Player19", 19, "password"),
        ("Player20", 17, "password")
    ])
    connection.commit()
    cursor.close()
