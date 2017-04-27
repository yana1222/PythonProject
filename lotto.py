import csv


f=open('c:/Users/wilso/Desktop/prize.csv')
rows = csv.reader(f)
next(rows)

rows = [row for row in rows]



class Ticket:
    name = ''
    prizes =[]
    expected_value=0
    new_expected_value = 0 
    price = 0
    prob = 0
    N=0
    n=0
    def predcount(self):
        N = sum(prize['total_winners'] for prize in self.prizes)/sum(prize['probability'] for prize in self.prizes)
        n = sum(prize['available'] for prize in self.prizes)/sum(prize['probability'] for prize in self.prizes)
        self.n = n
        self.N = N
        return(self)

    def new_prizes(self):
        for prize in self.prizes:
            prize['new_probability'] = prize['available']/self.n
        return(self)

tickets = []
def info(data):
    names =[]
    for row in rows:
        names.append((row[0],row[6]))
    names = set(names)
    for name in names:
        t=Ticket()
        t.name = name[0]
        t.price = int(name[1])
        tickets.append(t)
    return(tickets)

def prizes(lst, data):
    tickets=[]
    for ticket in lst:
        ticketdata = list(filter(lambda x: x[0]==ticket.name,data))
        prizes=[]
        for row in ticketdata:
            try:
                prize = {'prize':int(row[1]),'probability':1/int(row[2]),'total_winners':int(row[3]),'claimed':int(row[4]), 'available':int(row[5])}
            except:
                prize = {'prize':row[1],'probability':1/int(row[2]),'total_winners':int(row[3]),'claimed':int(row[4]), 'available':int(row[5])}
            prizes.append(prize)
        ticket.prizes = prizes
        tickets.append(ticket)
    return(tickets)

def ev(item):
    prize_probs = []
    for prize in item.prizes:
        prize_prob = (prize['prize'],prize['probability'])
        prize_probs.append(prize_prob)
    initev = sum(i[0]*i[1] for i in prize_probs if i[0] != 'Ticket')
    if prize_probs[-1][0]=='Ticket':
        ticketprize = prize_probs[-1] 
        ticketprizevalue_wght = 1/(1/ticketprize[1]-1)
        item.expected_value= (initev+ticketprizevalue_wght*initev)/item.price
    else:
        item.expected_value = initev/item.price
    return(item)

def newev(item):
    prize_probs = []
    for prize in item.prizes:
        prize_prob = (prize['prize'],prize['new_probability'])
        prize_probs.append(prize_prob)
    initev = sum(i[0]*i[1] for i in prize_probs if i[0] != 'Ticket')
    if prize_probs[-1][0]=='Ticket':
        ticketprize = prize_probs[-1] 
        ticketprizevalue_wght = 1/(1/ticketprize[1]-1)
        item.new_expected_value= (initev+ticketprizevalue_wght*initev)/item.price
    else:
        item.new_expected_value = initev/item.price
    return(item)

ticketlists = info(rows)
ticketlists = prizes(ticketlists,rows)
ticketlists = [ev(ticket) for ticket in ticketlists]
ticketlists = [t.predcount() for t in ticketlists]
ticketlists = [t.new_prizes() for t in ticketlists]
ticketlists = [newev(ticket) for ticket in ticketlists]

for ticket in ticketlists:
    print (ticket.name, ticket.expected_value, ticket.new_expected_value)

