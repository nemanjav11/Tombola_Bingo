import tkinter as tk
from tkinter import END,messagebox
from ticket import Ticket
import random


 # For executing the code that makes ticket with the entry

def button_clear(e):
    return e.delete(0,END)

def delete_all_command(entries):
    """Deletes all input information from the tkinter window"""
    money_Entry.delete(0,END)
    money_Entry.insert(0,'20')
    for i,j in enumerate(entries):
        j.delete(0,END)

def is_valid(number : int) -> bool:
    """This checks if the passed ticket information is valid for the game."""
    try: 
        num = int(number)
        if num > 48 or num < 0 or int(money_Entry.get())<0 or int(money_Entry.get())==ValueError:
            tk.messagebox.showinfo('Invalid Ticket', 'You entered invalid information.')
            return False
        return True
    except ValueError: 
        tk.messagebox.showinfo('Invalid Ticket', 'You entered invalid input for money or numbers')
        return False

def button_command(myList):
    """This function handles the main button command for making the ticket"""
    myList=[]
    for index in range(0,6):
        entries[index].focus_set()
        if is_valid(entries[index].get()):
            myList.append(entries[index].get())
        else: 
            break

    try: money= int(money_Entry.get())
    except ValueError: 
        money = 20
        
        
    else:
        a= Ticket(myList,money)
        tk.messagebox.showinfo('Ticket status',a.__str__()) 
    
    for i in entries:
        button_clear(i)
    money_Entry.insert(0,'20')
    
    entries[0].focus()
    

def random_command():
    """For picking random numbers\n
    and passing them inside the entries list"""
    randomList=[i for i in random.sample(range(1,49),6)]
    randomList.sort()
    entries = [child for child in mainframe.winfo_children() if isinstance(child, tk.Entry)]
    entries.pop(-1)
    for i,j in enumerate(entries):
        j.delete(0,END)
        j.insert(0,randomList[i])





 ## Creating a tkinter window application
root = tk.Tk()
root.resizable(height = None,width = None)
root.geometry("600x300")
root.configure(bg = '#006400')
root.title('Bingo Game')
mainframe= tk.Frame(root, relief='sunken',
                    padx = 10, pady = 10,
                    border = 2, height = 280)
mainframe.pack(fill ='both', padx = 20, pady = 20)
entries={1:"label1",
         2:"label2",
         3:"label3",
         4:"label4",
         5:"label5",
         6:"label6"}


for i in range (0,6):
    tk.Entry(mainframe,width = 10, highlightbackground = 'gray',selectbackground = 'blue').grid(row=0,column=i)
    
money_Entry=tk.Entry(mainframe, width = 8)
money_Entry.insert(0,20)
money_Entry.bind("<FocusIn>", lambda x: money_Entry.select_range(0,END))
money_Entry.grid(row = 3,column = 0, columnspan = 1)
 # For switching between Entry with <Return> button
 


def go_to_next_entry(event, entry_list, this_index):
    """This function is for changing through the list of entries
    using Enter button. """
    next_index = (this_index + 1) % len(entry_list)
    entry_list[next_index].focus_set()

    
money_Label=tk.Label(mainframe,text = 'Enter money amount')
money_Label.grid(row = 3,column = 1, columnspan = 3)
make_Ticket_Button=tk.Button(mainframe, 
                             text = 'Make an Ticket entry',
                             padx = 50, 
                             pady = 20,
                             borderwidth = 3,
                             command =lambda list=[]: button_command(list),)
make_Ticket_Button.grid(row = 5, column = 3, columnspan = 5, )
play_Round_Button=tk.Button(mainframe, text='Random numbers',padx = 50,pady = 20,
                            borderwidth=3, command=random_command, state='active')
play_Round_Button.grid(row = 5, column = 0, columnspan = 3,)
make_Empty_Space=tk.Label(mainframe, text = '', height = 3)
make_Empty_Space.grid(row = 4, column = 0, columnspan = 5, padx = 60, pady = 20)

entries = [child for child in mainframe.winfo_children() if isinstance(child, tk.Entry)]
entries[0].focus()
buttons= [child for child in mainframe.winfo_children() if isinstance(child, tk.Button)]

for idx, entry in enumerate(entries+buttons):
    entry.bind('<Return>', lambda e, idx = idx: go_to_next_entry(e, entries+buttons, idx))
    if entry==buttons[0]:
        list=[]
        entry.bind('<Return>', lambda list: button_command(list))
    entry.register(entry,'')
    entry.bind('')
     
    





root.mainloop()