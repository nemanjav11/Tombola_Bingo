import json
import ast
from databaseMGT import connect_Sqlite


def Check_Connection(conn):
    try:
        conn.cursor()
        return True
    except Exception:
        return False


def Ticket_Check(TicketNo):
    query = f"SELECT * FROM tickets  WHERE id='{TicketNo}'"
    conn,c = connect_Sqlite()
    c.execute(query)
    
    _,_,gameId,numbers_list,money,money_won,is_winner,_= c.fetchall()[0]
    ##numbers_list = json.loads(numbers_list)
    numbers_list = ast.literal_eval(numbers_list)
    numbers_list= [int(num) for num in numbers_list]


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
        multipliers_valid = []
                
        for i in multipliers:
            try :
                multipliers_valid.append(int(i))
            except (NameError,ValueError): pass
            finally: pass
        multipliers = multipliers_valid
        money_won=min(multipliers)* money
        money_won= money_won * mainWin
        #if mainWin>1:
            #print(f"ticket is winner with multiplier id {TicketNo} you won multiplier on {stars}") 
        #else: print(f"WINNING TICKET :  id {TicketNo} you won : {money_won}")
        is_winner=True

    else: 
         #print(f"Loss - {TicketNo} : Ticket No.")
         is_winner = False   
    #try:
    c.execute("UPDATE tickets SET money_won=?,is_winner=? WHERE id=?", (money_won, is_winner,TicketNo))
    #except: pass
    conn.commit()
    conn.close()

def Payout_Round(gameId):
    conn,c = connect_Sqlite()
    c.execute("SELECT serialId FROM tickets WHERE gameId='{}'".format(gameId))
    ticket_winnings = c.fetchall()
    conn.close()
    for i in range(0, len(ticket_winnings)):
        Ticket_Check(ticket_winnings[i][0])

 #time_start=time.time()

#time_stop=time.time()
#print(time_stop - time_start)


if __name__ == '__main__':
    for i in range(1,27075):
        Ticket_Check(i) 
    Ticket_Check(input("Insert a ticket number"))