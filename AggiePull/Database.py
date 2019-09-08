import random
import datetime

from sqlite3 import *
from DataTable import logindata
from DataTable import insertdata
from DataTable import deltable
from DataTable import seeall
import csv
userClass = -99
create = 0
con = connect('database.db')
logindata(con)
#deltable(con)
repeat = True
while (repeat == True):
   create = int(input("Enter 1 if new account, otherwise enter 2: "))
   if create == 1:
       newuser = input("Enter the new username: ")
       newpass = input("Enter the new password: ")
       newfirst = input("Enter your first name: ")
       newlast = input("Enter your last name: ")
       newclass = input("Enter your classification: ")
       newid = input("Enter your sports id number: ")
       entities = (newuser, newpass, newfirst, newlast, newclass, newid)
       insertdata(con, entities)
   elif create == 2:
       user = input("Username: ")
       password = input("Password: ")
       break
cursorObj = con.cursor()
cursorObj.execute('SELECT * from accounts WHERE user=? AND pass=?', (user, password))
if (user == 'admin'):
   if (password == 'admin'):
       seeall(con)

if cursorObj.fetchall() :
   print ("Welcome to the website")
   print("Your information is formatted as 'First Name', 'Last Name', 'Classification', and 'Sports ID'")
   for row in cursorObj.execute('SELECT firstname, lastname, class, sportsid FROM accounts WHERE user=? AND pass =?', (user, password)):
       print(row)
       userClass = row[2]
else:
   if(user != "admin"):
       if(password != "admin"):
           print ("Your username or password is incorrect")

def getClass(con):
    l1 = []
    cursorObj = con.cursor()
    cursorObj.execute('SELECT * FROM accounts')
    rows = cursorObj.fetchall()
    for row in rows:
       l1.append(row[4])
    return l1

def getName(con):
    l1 = []
    cursorObj = con.cursor()
    cursorObj.execute('SELECT * FROM accounts')
    rows = cursorObj.fetchall()
    for row in rows:
       l1.append(row[2]+' '+row[3])
    return l1

def getSports(con):
    l1 = []
    cursorObj = con.cursor()
    cursorObj.execute('SELECT * FROM accounts')
    rows = cursorObj.fetchall()
    for row in rows:
       l1.append(row[5])
    return l1

availableTickets = []

class Ticket():
    def __init__(self, section, row, seat):
        self.section = section
        self.row = row
        self.seat = seat

    def printTicket(self):
        print("Section {}, Row {}, Seat {}".format(self.section, self.row, self.seat))


nullTicket = Ticket(720, 720, 720)


def loadTickets():
    # first deck student tickets
    for section in (123, 124, 127, 128):
        for row in range(1, 34 + 1):
            for seat in range(1, 60 + 1):
                studentTicket = Ticket(section, row, seat)
                availableTickets.append(studentTicket)

    # second deck student tickets
    for section in range(230, 238 + 1):
        for row in range(1, 38 + 1):
            for seat in range(1, 40 + 1):
                studentTicket = Ticket(section, row, seat)
                availableTickets.append(studentTicket)

    # third deck student tickets
    for section in range(330, 338 + 1):
        for row in range(1, 37 + 1):
            for seat in range(1, 40 + 1):
                studentTicket = Ticket(section, row, seat)
                availableTickets.append(studentTicket)


def getTickets(groupSize):
    tickets = []
    if groupSize > 12:
        tickets = getGroupTickets(groupSize)
    else:
        tickets = getRandomTickets(groupSize)
    return tickets


def getGroupTickets(groupSize):
    groupTickets = []

    # find best available third deck seats
    for i in range(0, 8 + 1):

        # find section closest to 50 yard line
        if i % 2 == 0:
            section = 334 + (i / 2)
        else:
            section = 334 - ((i + 1) // 2)

        # find best row with enough available seats
        for row in range(1, 37 + 1):
            for ticket in availableTickets:
                if len(groupTickets) >= groupSize:
                    break
                if ticket.section == section:
                    if ticket.row == row:
                        if ((41 - ticket.seat) >= (groupSize - len(groupTickets))):
                            groupTickets.append(ticket)
                            availableTickets[availableTickets.index(ticket)] = nullTicket
    return groupTickets


def getRandomTickets(groupSize):
    randomTickets = []
    potentialRows = []

    # find first deck rows with enough seats
    for ticket in availableTickets:
        repeat = False
        if ticket.section < 200:
            if (61 - ticket.seat) >= (groupSize):
                for pTicket in potentialRows:
                    if (ticket.section == pTicket.section) and (ticket.row == pTicket.row):
                        repeat = True
                if not repeat:
                    potentialRows.append(ticket)

    # randomly select first deck row
    if len(potentialRows) > 0:
        sTicket = random.choice(potentialRows)
        for ticket in availableTickets:
            if (ticket.section == sTicket.section) and (ticket.row == sTicket.row) and (
                    ticket.seat < (sTicket.seat + groupSize)):
                randomTickets.append(ticket)
                availableTickets[availableTickets.index(ticket)] = nullTicket

    # find second deck rows with enough seats
    else:
        for ticket in availableTickets:
            repeat = False
            if ticket.section >= 200 and ticket.section < 300:
                if (61 - ticket.seat) >= (groupSize):
                    for pTicket in potentialRows:
                        if (ticket.section == pTicket.section) and (ticket.row == pTicket.row):
                            repeat = True
                    if not repeat:
                        potentialRows.append(ticket)

        if len(potentialRows) > 0:
            sTicket = random.choice(potentialRows)
            for ticket in availableTickets:
                if (ticket.section == sTicket.section) and (ticket.row == sTicket.row) and (
                        ticket.seat < (sTicket.seat + groupSize)):
                    randomTickets.append(ticket)
                    availableTickets[availableTickets.index(ticket)] = nullTicket

        # defer to third deck seats
        else:
            randomTickets = getGroupTickets(groupSize)

    return randomTickets


'''def test():
    loadTickets()
    for i in range (0, 1260):
        fillTickets = getTickets(12)
    myTickets = getTickets(12)
    for ticket in myTickets:
        ticket.printTicket()

test()'''

loadTickets()
print('Create Group')

dataClass = getClass(con)
dataName = getName(con)
dataSportsPass = getSports(con)
sportsPass = []
sizeClass = []
groupClass = [userClass]

while True:
    addMore = str(input('Click + to add more people and done when done: '))
    if addMore == '+':
        tempSportsPass = int(input('Enter sports pass number: '))
        if tempSportsPass in dataSportsPass:
            if tempSportsPass in sportsPass:
                print('Person already added to group.')
            else:
                nameTemp = dataName[dataSportsPass.index(tempSportsPass)]
                nameAsk = str(input('Add ' + str(nameTemp) + '? Type y or n: '))
                if (nameAsk == 'y') and (tempSportsPass not in sportsPass):
                    sportsPass.append(tempSportsPass)
                    groupClass.append(dataClass[dataSportsPass.index(tempSportsPass)])
                else:
                    print("Try another sports pass.")
        else:
            print("Error, invalid sports pass.")
    elif addMore == 'done':
        break
    else:
        print('Error')

if len(sportsPass) == 0:
    sizeClass = [(1, userClass)]
else:
    sizeClass.append((1 + len(sportsPass), max(groupClass)))

print(sizeClass)
size = sizeClass[0][0]
classification = sizeClass[0][1]
const_g_size = 12
#now = datetime.datetime.today().weekday()
now = 0
const_classification = 999
if now == 0:
    const_classification = 4
elif now == 1:
    const_classification = 3
elif now == 2:
    const_classification = 2\

elif now == 3:
    const_classification = 1

myTickets = []
if (size >= const_g_size) or (classification >= const_classification):
    myTickets = getTickets(size)
else:
    print("Invalid")
for ticket in myTickets:
    ticket.printTicket()