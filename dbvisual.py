import sqlite3
import pandas as pd
import json

database_name="game.db" #connects to a database

query= "SELECT * FROM numbers_played" #query to be sent to a database

# #transforming json string numbers from database into dictionary
# with sqlite3.connect(database_name) as conn:
#     df_Game = pd.read_sql_query(query,conn)
# my_Game_Dict= dict(df_Game['numbers'][df_Game['id']==0])
# for i in my_Game_Dict.values():
#     global my_Game_Dicts
#     my_Game_Numbers= json.loads(i)
# for i,j in my_Game_Numbers.items():
#     print(f" {i} : {j}")







query= "SELECT * FROM tickets"
with sqlite3.connect(database_name) as conn:
    df = pd.read_sql_query(query,conn)




print(df[df['money_won']>100])
