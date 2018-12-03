#!/Library/Frameworks/Python.framework/Versions/3.5/bin/python3
#Import decklist downloaded from tapped out into card collection SQL table

#the SQLite shell CSV importer can't handle more complicated CSV files,
#like ones with embeded quotes or commas, so to import the deck lists
#we are going through python

import csv
import sqlite3

#csv file for deck being importated
deck_list_csv="Collection.csv"
#location of cards to be entered into the database
location="collection binder"

cards=[]
with open(deck_list_csv, newline='') as deck_list:
    reader = csv.reader(deck_list)
    for row in reader:
        cards.append(row)

#connect to the SQL database
#the table we are working with called "collection"        
#Collums: card_name, qty, location, date_mod

conn = sqlite3.connect('MTGmodern.db')
c = conn.cursor()
for x in range(1,len(cards)):
    card_name=cards[x][2]
    qty=int(cards[x][1])
    c.execute("INSERT INTO collection (card_name, qty, location, date_mod) VALUES (?, ?, ?, DateTime('now'));",
             (card_name, qty, location))
              
    
conn.commit() #save
conn.close() #quit

print('done')
