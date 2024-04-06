from DataBaseMGT import connect_Sqlite
import json
import time


def read_all_rows():
    conn,c = connect_Sqlite()
    c.execute("SELECT * FROM numbers_played")
    rows = c.fetchall()
    for row in rows:
        print(row)
    conn.close()



def read_specific_row():
    conn,c = connect_Sqlite()
    c.execute("SELECT * FROM numbers_played WHERE id='1'")
    rows = c.fetchall()
    for row in rows:
        print(row)
    conn.close()





def get_dict_from_database():
    conn,c = connect_Sqlite()
    c.execute("SELECT numbers FROM numbers_played")
    dict_as_json = c.fetchone()[0]

    # Convert the JSON string back into a dictionary
    dictionary = json.loads(dict_as_json)

    conn.close()
    return dictionary





def read_specific_winnings(id):
    conn,c = connect_Sqlite()

    c.execute("SELECT numbers FROM numbers_played WHERE id='{}'".format(id))
    dict_as_json = c.fetchone()[0]

    # Convert the JSON string back into a dictionary
    dictionary = json.loads(dict_as_json)

    conn.close()
    
    
    for key, value in dictionary.items():
        time.sleep(2)
        print(f"{key}: {value}")

        



def read_specific_ticket(id):
    conn,c = connect_Sqlite()
    c.execute("SELECT money_won FROM tickets where id ='{}'".format(id))
    tickets = c.fetchall()
    conn.close()
    return tickets


def read_all_winnings():
    conn,c = connect_Sqlite()
    c.execute("SELECT money_won FROM tickets where money_won ")
    tickets = c.fetchall()
    winnings = 0
    for i in tickets:
        if i[0] == None:
            pass
        else: winnings += i[0]
    conn.close()
    return(winnings)


def read_all_pays():
    conn,c = connect_Sqlite()
    c.execute("SELECT money FROM tickets ")
    tickets = c.fetchall()
    paying = 0
    for i in tickets:
        if i[0] == None:
            pass
        else: paying += i[0]
    conn.close()
    return(paying)
    


Cash_IN = int(read_all_pays())
Cash_OUT = int(read_all_winnings())
print(Cash_IN - Cash_OUT)
