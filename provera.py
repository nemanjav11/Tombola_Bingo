import sqlite3
import pandas as pd
import json
import time
import os
DATABASE_NAME = os.path.abspath(r'C:\Users\Kico-neco\Documents\Python\Tombola_Bingo\game.db')

def make_number_from_string(input_string):
    result = ""
    for char in input_string:
        if char.isdigit():
            result += char
    return int(result) if result else None

def provera_Tiketa(brojTiketa):
    conn = sqlite3.connect(DATABASE_NAME)
    query = f"SELECT * FROM tickets  WHERE id='{brojTiketa}'"
    df= pd.read_sql_query(query,conn)
    
    
   
    
    _,_,gameId,numbers_list,money,money_won,is_winner,_= c.fetchall()[0]
    numbers_list= json.loads(numbers_list)
   
    c.execute("SELECT numbers FROM numbers_played WHERE id='{}'".format(gameId))
    dict_as_json = c.fetchone()
    
    c.execute("SELECT stars FROM numbers_played WHERE id='{}'".format(gameId))
    stars_as_json = c.fetchone()

    # Convert the JSON string back into a dictionary
    dictionary = json.loads(dict_as_json[0])
    stars = json.loads(stars_as_json[0])

    winningArray=[]
    
    for key,value in dictionary.items():
        winningArray.append(value)

    count= 0
    mainWin= 1
    
    for i in winningArray:
        if i in numbers_list:
            count += 1
    for i in stars:
        if i in numbers_list:
            mainWin += 1
    
    multipliers= []

    if count == 6 :
        
        for key,value in dictionary.items():
            if value in numbers_list:
                multipliers.append(key)
                
        
        money_won=int(min(multipliers))* money
        money_won= money_won*mainWin
        # if mainWin>1:
            # print(f"ticket is winner with multiplier id {brojTiketa} you won multiplier on {stars}") 
        # else: print(f"WINNING TICKET :  id {brojTiketa} you won : {money_won}")
        is_winner=True

    else: 
        # print(f"nedobitan {brojTiketa} : broj tiketa")
        is_winner = False   
    try:
        c.execute("UPDATE tickets SET money_won=?,is_winner=? WHERE id=?", (money_won, is_winner, brojTiketa))
    except: pass
    conn.commit()
    conn.close()

#provera_Tiketa(1591)
#provera_Tiketa(1592)




def isplata(gameId):
    conn = sqlite3.connect(DATABASE_NAME)
    c=  conn.cursor()
    c.execute("SELECT serialId FROM tickets WHERE gameId='{}'".format(gameId))
    ticket_winnings = c.fetchall()

    for i in range(0, len(ticket_winnings)):
        provera_Tiketa(ticket_winnings[i][0])


def return_max_id_ticket():
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("SELECT MAX(id) FROM tickets")
    maxId = c.fetchone()[0]
    return maxId


time_start=time.time()
for i in range(0,2):
    provera_Tiketa(i)
time_stop=time.time()
print(time_stop - time_start)

# provera_Tiketa(input(f"Insert a ticket number: "))