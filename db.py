import sqlite3
from contextlib import closing

def init_db():
    with closing(sqlite3.connect("main.db", check_same_thread=False)) as connection:
        with closing(connection.cursor()) as cursor:
            cursor.execute('CREATE TABLE IF NOT EXISTS players (player_id INTEGER PRIMARY KEY AUTOINCREMENT, player_name TEXT)')
            cursor.execute('CREATE TABLE IF NOT EXISTS matches (match_id INTEGER PRIMARY KEY AUTOINCREMENT, player1_id INTEGER, player2_id INTEGER, time DATETIME, FOREIGN KEY(player1_id) REFERENCES players (player_id),  FOREIGN KEY(player2_id) REFERENCES players (player_id))')
            cursor.execute('CREATE TABLE IF NOT EXISTS match_sets (match_id INTEGER, set_num INTEGER, set_p1 INTEGER, set_p2 INTEGER, FOREIGN KEY(match_id) REFERENCES matches (match_id), PRIMARY KEY(match_id, set_num))')
            connection.commit()


def insert_player(player_name):
    data = (player_name,)
    with closing(sqlite3.connect("main.db", check_same_thread=False)) as connection:
        with closing(connection.cursor()) as cursor:
            cursor.execute('INSERT INTO players (player_name) VALUES(?)', data)
            connection.commit()

def insert_match(player1_id, player2_id, time):
    data = (player1_id, player2_id, time,)
    with closing(sqlite3.connect("main.db", check_same_thread=False)) as connection:
        with closing(connection.cursor()) as cursor:
            cursor.execute('INSERT INTO matches (player1_id, player2_id, time) VALUES(?, ?, ?)', data)
            connection.commit()

def insert_match_set(match_id, set1_p1, set1_p2, set2_p1, set2_p2, set3_p1, set3_p2):
    data = [(match_id, 1, set1_p1, set1_p2),(match_id, 2, set2_p1, set2_p2), (match_id, 3, set3_p1, set3_p2)]
    with closing(sqlite3.connect("main.db", check_same_thread=False)) as connection:
        with closing(connection.cursor()) as cursor:    
            cursor.executemany('INSERT INTO match_sets (match_id, set_num, set_p1, set_p2) VALUES (?, ?, ?, ?)', data)
            connection.commit()

def get_uncompleted_matches():
    with closing(sqlite3.connect("main.db", check_same_thread=False)) as connection:
        with closing(connection.cursor()) as cursor:
            return cursor.execute("""SELECT match_id as Id, time as Tid, p1.player_name as Spelare_1, p2.player_name as Spelare_2 FROM matches
                                   LEFT JOIN players as p1 ON matches.player1_id = p1.player_id
                                   LEFT JOIN players as p2 ON matches.player2_id = p2.player_id
                                   WHERE NOT EXISTS (SELECT 1 FROM match_sets WHERE match_sets.match_id = matches.match_id)
                                  ORDER BY Tid ASC""").fetchall()

def get_completed_matches():
    with closing(sqlite3.connect("main.db", check_same_thread=False)) as connection:
        with closing(connection.cursor()) as cursor:
            return cursor.execute("""SELECT match_id as Id, time as Tid, p1.player_name as Spelare_1, p2.player_name as Spelare_2 FROM matches 
                                    LEFT JOIN players as p1 ON matches.player1_id = p1.player_id
                                    LEFT JOIN players as p2 ON matches.player2_id = p2.player_id
                                    WHERE EXISTS (SELECT 1 FROM match_sets WHERE match_sets.match_id = matches.match_id)
                                    ORDER BY Tid DESC""").fetchall()

def get_sets_for_match(match_id):
    data = (match_id,)
    with closing(sqlite3.connect("main.db", check_same_thread=False)) as connection:
        with closing(connection.cursor()) as cursor:
            return cursor.execute("SELECT set_num, set_p1, set_p2 FROM match_sets WHERE match_id = ?", data).fetchall()

def get_players():
    with closing(sqlite3.connect("main.db", check_same_thread=False)) as connection:
        with closing(connection.cursor()) as cursor:
            return cursor.execute("SELECT player_id as Id, player_name as Namn FROM players").fetchall()

def get_player_name_from_id(player_id):
    data = (player_id,)
    with closing(sqlite3.connect("main.db", check_same_thread=False)) as connection:
        with closing(connection.cursor()) as cursor:
            return cursor.execute("SELECT player_name FROM players WHERE player_id = ?", data).fetchall()