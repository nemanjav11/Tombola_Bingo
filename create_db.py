import sqlite3
import random
import os
from tiket import get_sha1


#DATABASE_NAME= os.path.abspath("Tombola_Bingo/game.db")
DATABASE_NAME= 'game.db'
def connect_Sqlite():
    global conn,c
    conn = sqlite3.connect('game.db')
    c = conn.cursor()



def create_table_numbers_played():
    connect_Sqlite()
    c.execute("CREATE TABLE IF NOT EXISTS numbers_played (id INTEGER PRIMARY KEY,serial TEXT, numbers TEXT, date TEXT, stars TEXT)")
    conn.commit()
    conn.close()



def insert_empty_row():
    connect_Sqlite()
    c.execute("INSERT INTO numbers_played (serial,numbers, date) VALUES (NULL, NULL, NULL)")
    conn.commit()
    conn.close()




def create_database():
    connect_Sqlite()
    c.execute("""CREATE TABLE numbers_played (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    serial INTEGER,
                    numbers TEXT,
                    date TEXT
                )""")
    conn.commit()
    conn.close()

def create_tickets_table():
    connect_Sqlite()
    c.execute("""CREATE TABLE IF NOT EXISTS tickets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    serialId TEXT NOT NULL,
                    gameId TEXT NOT NULL,
                    numbers TEXT NOT NULL,
                    money INTEGER NOT NULL,
                    money_won INTEGER,
                    is_winner BOOLEAN NOT NULL,
                    date TEXT NOT NULL)""")
    conn.commit()
    conn.close()

def drop_all_tickets():
    connect_Sqlite()
    c.execute("DROP TABLE tickets")
    conn.close()
    return "Succeeded"


def read_all_tickets():
    connect_Sqlite()
    c.execute("SELECT * FROM tickets")
    tickets = c.fetchall()
    conn.close()
    return tickets


def insert_empty_ticket():
    connect_Sqlite()
    c.execute("INSERT INTO tickets (serial_Id, game_Id, numbers, money) VALUES (?,?,?,?)", (None, None, None, None))
    conn.commit()
    conn.close()



def add_is_winner_column():
    connect_Sqlite()
    c.execute("ALTER TABLE tickets ADD COLUMN serial INTEGER DEFAULT NULL")
    conn.commit()
    conn.close()

def update_serial_id(table_name, lambda_func):
    connect_Sqlite()
    c.execute(f'UPDATE {table_name} SET serialId = ?(serialId)', (lambda_func,))
    conn.commit()
    conn.close()


#changes all the values in the certain columns to some function
#Currently for encryption purposes 
def apply_changes_to_rows_in_column():
    connect_Sqlite()
    c.execute("SELECT id, gameId FROM tickets")
    rows = c.fetchall()
    for row in rows:
        rowId, gameId = row
        new_x = get_sha1(str(gameId + str(get_sha1('SECRET_KEY')+ str(rowId))))
        print(f"THIS IS new_x {new_x} and gameId {gameId} and id {rowId}")
        c.execute(f"UPDATE tickets SET serialId = ? WHERE id = ?", (new_x, rowId))
    conn.commit()
    conn.close()

# Example usage
#apply_lambda_to_serial_id(database_name, "tickets")

def add_stars_column():
    connect_Sqlite()
    c.execute("ALTER TABLE numbers_played ADD COLUMN stars TEXT DEFAULT NULL")
    conn.commit()
    conn.close()

def add_date_column():
    connect_Sqlite()
    c.execute("ALTER TABLE tickets ADD COLUMN date TEXT DEFAULT NULL")
    conn.commit()
    conn.close()
    print('Successfully added date column')


create_tickets_table()
create_table_numbers_played()

