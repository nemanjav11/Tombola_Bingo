import tkinter as tk
from PIL import ImageTk, Image
from tkinter import messagebox
from drafting import Game
import sqlite3
import pandas as pd
import json
import os




DATABASE_NAME= os.path.abspath("game.db")
# DATABASE_NAME= 'game.db'

def connect_Sqlite():
    global conn,c
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
# gets the latest version of the game object from the database
def get_last_id():
    connect_Sqlite()
    c.execute("SELECT MAX(id) FROM numbers_played")
    last_id = c.fetchone()[0]
    return last_id

 # transforming json string numbers from database into dictionary

def get_number_dictionary(id):
    QUERY = "SELECT * FROM numbers_played"
    with sqlite3.connect(DATABASE_NAME) as conn:
        df_Game = pd.read_sql_query(QUERY,conn)
    my_Game_Dict= dict(df_Game['numbers'][df_Game['id']==id])
    for i in my_Game_Dict.values():
        global my_Game_Dicts
        my_Game_Numbers = json.loads(i)
    return my_Game_Numbers



 # For executing the code that initializes the newest game object
last_Id= get_last_id() #For the initialization of the game, might change this later

root= tk.Tk()
root.title="Bingo"
root.geometry="1000x1600"
root.configure(bg='#006400')
root.resizable(False,False)

main_frame= tk.Frame(root, relief='sunken',border=5,padx=10,pady=10, height=600, width=800)
main_frame.grid(column=0, row=0, sticky='nswe', padx= 10, pady=30)

main_frame_balls= tk.Frame(main_frame, relief='sunken',border=2,padx=10,pady=10,)
main_frame_balls.grid(column=2, row=0)
### for displaying the numbers ###
numbers_frame=tk.Frame(main_frame,width=1000, height=20, borderwidth=3, border=3, relief='sunken')
numbers_frame.configure(height=500,width=650)
numbers_frame.grid_propagate(0)
numbers_frame.grid(column=1,row=0)
coordinates=[]
for i in range(7):
     for j in range(5):
          coordinates.append((i,j))

images=[]
for i in range(1,49):
     path = f"Images\image{i}_little.png"
     img_load=Image.open(path)
     img_load= ImageTk.PhotoImage(img_load)
     images.append(img_load)
images_Big=[]
for i in range(1,49):
     path = f"Images\image{i}_little.png"
     img_load=Image.open(path)
     img_load= img_load.resize((150,150),Image.LANCZOS)
     img_load= ImageTk.PhotoImage(img_load)
     images_Big.append(img_load)


counter=0
myList=[]
panels=[]
texts_Labels=[]
for c in coordinates:
     global img
     numbers_place=tk.Frame(numbers_frame,width=50, height=60)
     numbers_place.grid(column=c[0],row=c[1])
     numbers_text=tk.Label(numbers_place, font=('helvetica',10,'bold'),)
     numbers_text.grid(column=0,row=1)
     myList.append(numbers_place)
    
     paneli = tk.Label(numbers_place, image = images[counter], relief='raised',anchor='n')
     paneli.grid(column=0,row=0,sticky='nswe',padx=15,pady=10)
     panels.append(paneli)
     counter+=1





     


countdown_frame= tk.Frame(root, relief='groove')
countdown_frame.grid(column=0,row=1, sticky='we', padx=20, pady=5 )
countdown_label= tk.Label(root,text='0',anchor='center',background='#006400',font=('helvetica',12))
countdown_label.grid(column=0,row=2,)
countdown_line1= tk.Canvas(countdown_frame, height=20, width=1000)
countdown_line1.create_rectangle(0,0,0,20 ,fill='blue',outline='white')
countdown_line1.grid(column=0,row=0, sticky='we')
countdown_label2=tk.Label(root, text='Game with ID : '+ str(last_Id+1) + ' next',background='#006400',font=('helvetica',12))
countdown_label2.grid(column=0,row=3)


### THIS SECTION FOR IMAGE HANDLING ###

main_Img=Image.open('Images\image2_little.png')
main_Img= main_Img.resize((150,150),Image.LANCZOS)
main_Img = ImageTk.PhotoImage(main_Img)
panel = tk.Label(main_frame_balls, image = main_Img)
panel.pack(anchor='n')

my_Countdown = list(range(0,1000,2))
my_Time = list(map(lambda x: x/(10/3),my_Countdown))

# print(my_Time)
# print(my_Countdown)
my_Index = 480 #timer counter

def destroy_countdown():
    global countdown_label,countdown_line1,my_Index,last_Id
    countdown_line1.destroy()
    countdown_label.destroy()
    countdown_line1 = tk.Canvas(countdown_frame, height=20, width=1000, )
    countdown_label = tk.Label(root,text=str(round(my_Time[my_Index])),background='#006400',font=('helvetica',12,'bold'))
    countdown_label.grid(column=0,row=2,)
    countdown_label2=tk.Label(root,text='Game with ID : '+ str(last_Id+1) +' is next',background='#006400',font=('helvetica',12,'bold'))
    countdown_label2.grid(column=0,row=3)
    countdown_line1.create_rectangle(0,0,my_Countdown[my_Index],20 ,fill='blue',outline='white',disabledfill='gray')
    countdown_line1.grid(column=0,row=0, sticky='we')
    my_Index += 1
    if my_Index>=500:
        global my_dict, my_Game,my_Index_Draft
        my_dict=dict()
        for i in panels : i.destroy()
        for i in texts_Labels:  i.destroy()
        my_Game=Game()
        last_Id= get_last_id() 
        my_Index=0
        my_Index_Draft=0
        draft_numbers()
    countdown_frame.after(500, destroy_countdown)



def draft_numbers():
     global last_Id,images,my_Index_Draft,panel
     
     my_dict=get_number_dictionary(last_Id)
     my_Mults =[i for i in my_dict.keys()]
     numbers_place=tk.Frame(numbers_frame,width=50, height=60)
     numbers_place.grid(column=coordinates[my_Index_Draft][0],row=coordinates[my_Index_Draft][1])
     numbers_text=tk.Label(numbers_place, font=('helvetica',10,'bold'),text= my_Mults[my_Index_Draft])
     texts_Labels.append(numbers_text)
     numbers_text.grid(column=0,row=1)
     myList.append(numbers_place)
     panel.destroy()
     panel = tk.Label(main_frame_balls, image = images_Big[my_dict.get(my_Mults[my_Index_Draft])-1])
     panel.pack(anchor='n')
     paneli = tk.Label(numbers_place, image = images[my_dict.get(my_Mults[my_Index_Draft])-1], relief='raised',anchor='n')
     paneli.grid(column=0,row=0,sticky='nswe',padx=15,pady=10)
     panels.append(paneli)
     numbers_frame.after(3300, draft_numbers)
     my_Index_Draft+=1
     

# w = tk.Canvas(root, width=250, height=200)
# w.create_rectangle(0, 0, 100, 100, fill="blue", outline = 'blue')
# w.grid(row=0,)
destroy_countdown()
root.mainloop()


