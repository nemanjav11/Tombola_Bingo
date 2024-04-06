import random
import datetime
from drafting import get_sha1, Game
from databaseMGT import connect_Sqlite


def is_Not_Int(integer):
        try: int(integer)
        except TypeError: return True

def check_i(i):
        if (i <= 0) or (i >= 49):
            return False 
        else : return True
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
        
        self.money = money
        self.RejectionReason = ''
        self.validate_numbers()
        self.nums.sort()
        self.lastId= self.get_last_id()
        self.gameId=int(self.get_game_id())
        self.serialId= get_sha1(str(self.gameId) + str(get_sha1('SECRET_KEY')+ str(self.lastId)))
        self.date= datetime.datetime.now().timestamp() ## WE SHOULD ADD THIS INTO THE DATABASE 
        self.insert_ticket()
        #print(self.ValidTicket)
        

        
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
        if self.ValidTicket:
            conn,c = connect_Sqlite()
            c.execute("INSERT INTO tickets (serialId, gameId, numbers, money, is_winner, date) VALUES (?,?,?,?,FALSE,?)", (self.serialId, self.gameId, str(self.nums),self.money, self.date))
            conn.commit()
            conn.close()
            return 'Success'
        

    def validate_numbers(self):
        if len(self.nums) >= 7:
            self.RejectReason('Number array is too long')
        if len(self.nums) > 0:
                try:
                    [int(i) for i in self.nums]
                except TypeError : 
                    self.RejectReason('Input not a number; ')
                finally : 
                    if len(self.nums) == 6 :
                        if True in list([(int(i)<=0 or int(i)>=49) for i in self.nums]):
                            self.RejectReason('Invalid number in numbers list')
                        else : 
                            if len(set(self.nums)) < 6:
                                self.RejectReason('Repeated number in numbers list')
                            self.ValidTicket = True
                        
        if self.nums==[]:
            while len(self.nums) < 6 :
                i = random.randint(1,49)
                if i not in self.nums :
                    self.nums.append(i)
            self.ValidTicket = True
            
        try:
            try:
                int(self.lastId)
            except AttributeError:
                self.lastId = 0
            finally : 
                int(self.gameId)
        except AttributeError: #for the first time
            self.gameId = 1
        if (self.money > 1000) or (self.money < 20) :
                self.RejectReason('Invalid money; ')

    def RejectReason(self,ReasonStr):
        self.RejectionReason = self.RejectionReason + ReasonStr
        self.ValidTicket = False
        exit()
        
""" money_players=[20,20,20,20,50,50,100,20,500,200]
for _ in range(1000):
    for _ in range(50):
        money_Sample=random.sample(money_players,1)
        a=Ticket([],money_Sample[0])
    b=Game() """

""" money_players=[20,20,20,20,50,50,100,20]
time_start=time.time()
for _ in range(1,20):
    for i in range (1,500):
        Ticket()
    Game()
time_stop= time.time()
print(time_stop-time_start) """
#Ticket([1,2,3,4,5,6],20)