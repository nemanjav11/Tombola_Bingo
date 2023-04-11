import sqlite3
import hashlib
import random
import datetime
import json
import os





DATABASE_NAME= "game.db"

# DATABASE_NAME= os.path.abspath("Tombola_Bingo/game.db")

# Connects to a database and creates a cursor object
    
def connect_Sqlite():
    global conn,c
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    

        

### RETURNS SHA1 hash of the string ###


def get_sha1(input_string):
    sha1 = hashlib.sha1()
    sha1.update(input_string.encode('utf-8'))
    return sha1.hexdigest()
    
class Game():
    
    
    
    
    
    ## Method for inserting a new game object into the database
    
    def insert_row(self):
        SQL_INSERT_QUERY = "INSERT INTO numbers_played (serial, numbers, date, stars) VALUES (?, ?, ?, ?)"
        connect_Sqlite()
        
    # Convert the dictionary to a JSON string for database compatibility

        dict_As_Json = json.dumps(self.numbers)
        self.date= json.dumps(datetime.datetime.now().timestamp())
        c.execute(SQL_INSERT_QUERY, (self.Serial, dict_As_Json, self.date, self.starsArray))
        
        conn.commit()
        conn.close()
    
    ## Reads the database to see the last number and encrypts the input data
   
    def add_id(self):
        GET_ID_QUERY = "SELECT id FROM numbers_played ORDER BY id DESC LIMIT 1"
        connect_Sqlite()
        c.execute(GET_ID_QUERY)
        try: max_Id = c.fetchone()[0]
        except TypeError: max_Id= 0 #Because we need this for the first time initialization
        
        if max_Id:
            self.id = max_Id + 1
            new_Id = max_Id + 1
            new_Id = get_sha1(str(new_Id)+get_sha1("SECRET_KEY"))
        
        else:
            self.id = 0
            new_Id = 0
            new_Id = get_sha1(str(new_Id)+get_sha1("SECRET_KEY"))
        
        self.Serial = new_Id
        print(self.Serial)
        conn.close()

    ## Generates the game numbers in a dictionary with multipliers
    
    def generate_numbers(self):
        numbers = list(range(1, 49))
        random.shuffle(numbers)
        arrayWinnings=["First","Second","Third","Forth","Fifth",10000,7500,5000,2500,1000,500,300,200,150,100,90,80,70,60,50,40,30,25,20,15,10,9,8,7,6,5,4,3,2,1]
        numbersRandom= numbers[:35]
        dictionary = dict(zip(arrayWinnings, numbersRandom))
        self.numbers= dictionary

  
    ## Method for generating star multipliers
    
    def generate_stars(self):
        arrayMultipliers=[i for i in range(7,36)]
        starsArray=[]
        while len(starsArray) < 2:
            i= random.choice(arrayMultipliers)
            if i in starsArray: pass
            else: starsArray.append(i)
        self.starsArray= json.dumps(starsArray)
        


    def __init__(self):
        connect_Sqlite()
        self.generate_numbers()
        self.generate_stars()
        self.add_id()
        self.insert_row()
        #print("Success!")

    def __str__(self):
        return f"Game object with id {self.id} and numbers {self.numbers}"    