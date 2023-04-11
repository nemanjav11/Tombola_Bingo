import sqlite3
import json
import time

database_name = "game.db"
def read_all_rows(database_name):
    conn = sqlite3.connect(database_name)
    c = conn.cursor()
    c.execute("SELECT * FROM numbers_played")
    rows = c.fetchall()
    for row in rows:
        print(row)
    conn.close()



def read_specific_row(database_name):
    conn = sqlite3.connect(database_name)
    c = conn.cursor()
    c.execute("SELECT * FROM numbers_played WHERE id='1'")
    rows = c.fetchall()
    for row in rows:
        print(row)
    conn.close()





def get_dict_from_database(database_name):
    conn = sqlite3.connect(database_name)
    c = conn.cursor()

    c.execute("SELECT numbers FROM numbers_played")
    dict_as_json = c.fetchone()[0]

    # Convert the JSON string back into a dictionary
    dictionary = json.loads(dict_as_json)

    conn.close()
    return dictionary

##print(get_dict_from_database(database_name))




def read_specific_winnings(id):
    conn = sqlite3.connect(database_name)
    c = conn.cursor()

    c.execute("SELECT numbers FROM numbers_played WHERE id='{}'".format(id))
    dict_as_json = c.fetchone()[0]

    # Convert the JSON string back into a dictionary
    dictionary = json.loads(dict_as_json)

    conn.close()
    
    
    for key, value in dictionary.items():
        time.sleep(2)
        print(f"{key}: {value}")

        



def read_specific_ticket(id):
    conn = sqlite3.connect(database_name)
    c = conn.cursor()
    c.execute("SELECT money_won FROM tickets where id ='{}'".format(id))
    tickets = c.fetchall()
    conn.close()
    return tickets


def read_all_winnings():
    conn = sqlite3.connect(database_name)
    c = conn.cursor()
    c.execute("SELECT money_won FROM tickets where money_won ")
    tickets = c.fetchall()
    winnings = 0
    for i in tickets:
        if i[0] == None:
            pass
        else: winnings += i[0]
    print(winnings)   
    conn.close()


def read_all_pays():
    conn = sqlite3.connect(database_name)
    c = conn.cursor()
    c.execute("SELECT money FROM tickets ")
    tickets = c.fetchall()
    winnings = 0
    for i in tickets:
        if i[0] == None:
            pass
        else: winnings += i[0]
    print(winnings)   
    conn.close()
    








print(read_all_pays()- read_all_winnings())

