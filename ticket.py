import sqlite3
import os
import random
import json
#from drafting import Game
import time
import datetime
from drafting import get_sha1, Game

# DATABASE_NAME= os.path.abspath("Tombola_Bingo/game.db")
DATABASE_NAME= 'game.db'

def connect_Sqlite():
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    return conn,c

def is_Not_Int(integer):
        try: int(integer)
        except TypeError: return True


class Ticket:
    """ Creates an ticket object with tickets \n
    id, numbers, money played, gameId and date when ticket was created.\n
    without parameters nums ticket will get randomly generated numbers \n
    """
    def __init__(self, nums=[], money=20):
        if None not in nums:
            self.nums= nums
        else:
            raise ValueError("Invalid number for ticket")  
        
        self.validate_numbers()
        self.nums.sort()
        self.money = money
        self.lastId= self.get_last_id()
        self.gameId=int(self.get_game_id())
        self.serialId= get_sha1(str(self.gameId) + str(get_sha1('SECRET_KEY')+ str(self.lastId)))
        self.date= datetime.datetime.now().timestamp() ## WE SHOULD ADD THIS INTO THE DATABASE 
        self.insert_ticket()

        
        #print("Success!")
    
    def __str__(self):
        numbers_For_Display=''
        for i in self.nums:
            numbers_For_Display=numbers_For_Display+ str(i)+', '
        return f"You have created a ticket with numbers : {numbers_For_Display} for {self.money} coins, for Game no.{self.gameId}, ticket no.{self.lastId} ! Good Luck!"
        
    @classmethod
    def get_last_id(self):
        conn,c = connect_Sqlite()
        c.execute("SELECT MAX(id) FROM tickets")
        last_id = c.fetchone()[0]
        
        if last_id == 0:
            self.id = 0
        else:
            try: self.id = last_id + 1
            except TypeError: self.id= 0
        conn.close()
        return self.id
        



    def get_game_id(self):
        conn, c = connect_Sqlite()
        c.execute("SELECT MAX(id) FROM numbers_played")
        last_id = c.fetchone()[0]
        if last_id is None:
            self.gameId = 1
        else:
            self.gameId = last_id + 1
        conn.close()
        return self.gameId
     


    def insert_ticket(self):
        conn,c = connect_Sqlite()
        c.execute("INSERT INTO tickets (serialId, gameId, numbers, money, is_winner, date) VALUES (?,?,?,?,FALSE,?)", (self.serialId, self.gameId, str(self.nums),self.money, self.date))
        conn.commit()
        conn.close()

    def validate_numbers(self):
        if self.nums==[]:
            raise ValueError("You can't provide empty list")
#a=Ticket()

#nums= [7,1,5,9,20,15]
# nums=[]

## For testing purposes only

# money_players=[20,20,20,20,50,50,100,20]
# for _ in range(20):
#     for _ in range(100):
#         money_Sample=random.sample(money_players,1)
#         a=Ticket(money=money_Sample[0])
#     b=Game()
    



# money_players=[20,20,20,20,50,50,100,20]
# time_start=time.time()
# for _ in range(1,20):
#     for i in range (1,500):
#         Ticket()
#     Game()
# time_stop= time.time()
# print(time_stop-time_start)