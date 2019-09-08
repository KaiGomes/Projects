from sqlite3 import *

con = connect('database.db')

def logindata(con):
   cursorObj = con.cursor()
   cursorObj.execute("CREATE TABLE IF NOT EXISTS accounts(user text PRIMARY KEY, pass text, firstname text, lastname text, class integer, sportsid integer)")
   con.commit()

def insertdata(con, entities):
   cursorObj = con.cursor()
   #cursorObj.execute("INSERT INTO accounts VALUES('jcc5578', 'abrahamisuseless')")
   #con.commit()
   cursorObj.execute('INSERT OR IGNORE INTO accounts(user, pass, firstname, lastname, class, sportsid) VALUES(?, ?, ?, ?, ? ,?)', entities)
   con.commit()

def seeall(con):
   cursorObj = con.cursor()
   cursorObj.execute('SELECT * FROM accounts')
   rows = cursorObj.fetchall()
   for row in rows:
       print(row)




#def sportsid(con):
#    cursorObj = con.cursor()
#    cursorObj.execute("CREATE TABLE idaccounts(id integer PRIMARY KEY, class text)")
#    con.commit()

#def temptable(con):
#    cursorObj = con.cursor()
#    cursorObj.execute("CREATE TABLE temp(newid integer PRIMARY KEY, newclass text)")

#def inserttemp(con, temp):
#    cursorObj = con.cursor()
#    cursorObj.execute('In')
def deltable(con):
   cursorObj = con.cursor()
   cursorObj.execute('DROP TABLE if exists accounts')
   con.commit
