import sqlite3
import os

DATABASE_NAME= os.path.abspath(r'C:\Users\Kico-neco\Documents\Python\Tombola_Bingo\dist\game.db')
# DATABASE_NAME= 'game.db'
global conn,c
def connect_Sqlite():
    global conn,c
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    return conn,c