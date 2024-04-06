from databaseMGT import *
conn,c = connect_Sqlite()
def MakeTables():
    create_numbers_table()
    create_tickets_table()

################################################################
#  These are codes for the database handling functions,        #
# used for first initialization and testing purposes           #
################################################################


def add_Text_column(TableName,ColumnName):
    
    c.execute(f"ALTER TABLE ? ADD COLUMN ? TEXT DEFAULT NULL", TableName, ColumnName)
    conn.commit()

def insert_empty_row():
    
    c.execute("INSERT INTO numbers_played (serial,numbers, date) VALUES (0, NULL, NULL)")
    conn.commit()


def create_numbers_table():
    
    c.execute("""CREATE TABLE IF NOT EXISTS numbers_played (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    serial INTEGER,
                    numbers TEXT,
                    date TEXT,
                    stars TEXT
                )""")
    conn.commit()

def create_tickets_table():
    
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





""" def drop_all_tickets():
    connect_Sqlite()
    c.execute("DROP TABLE tickets")
    conn.close()
    return "Succeeded"
 """

""" def read_all_tickets():
    connect_Sqlite()
    c.execute("SELECT * FROM tickets")
    tickets = c.fetchall()
    conn.close()
    return tickets """


#changes all the values in the certain columns to some function
""" #Currently for encryption purposes 
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
    conn.close() """

# Example usage
#apply_lambda_to_serial_id(database_name, "tickets")
if __name__ == "__main__":
    MakeTables()
    print('Success')