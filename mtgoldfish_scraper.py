#!/Library/Frameworks/Python.framework/Versions/3.5/bin/python3
import requests
from bs4 import BeautifulSoup
import sqlite3

#urls for creatuers, spells, and lands
mtggoldfish_modern_creatures="https://www.mtggoldfish.com/format-staples/modern/full/creatures"
mtggoldfish_modern_spells="https://www.mtggoldfish.com/format-staples/modern/full/spells"
mtggoldfish_modern_lands="https://www.mtggoldfish.com/format-staples/modern/full/lands"
all_mtggoldfish=[mtggoldfish_modern_creatures, mtggoldfish_modern_spells, mtggoldfish_modern_lands]

#get a list of the card names as strings
cards=[]
for card_type in all_mtggoldfish:
    page = requests.get(card_type)
    #print(page.status_code)
    soup = BeautifulSoup(page.content, 'html.parser')
    cards_messy = soup.find_all(class_='col-card') #look for col-card HTML tag
    for x in range(1,51): #The lists are 50 most pop cards of a type, but the first entry is the title
        cards.append(cards_messy[x].get_text())

#print(cards)

#connect to the SQL database
#the table we are working with called "modern_staples"        
#Collums: card_name, add_date, last_seen
#add_date = date added to db, last_seen=date last appered in top 50 lists

conn = sqlite3.connect('MTGmodern.db')
c = conn.cursor()
for z in range(0,len(cards)):
    c.execute('SELECT card_name FROM modern_staples WHERE card_name = ?;', [cards[z]])
    data=c.fetchone()
    #If the entry does not exist make it, if it does update last seen
    if data is None:
        c.execute("INSERT INTO modern_staples (card_name, add_date, last_seen) VALUES (?, DateTime('now'), DateTime('now'));",
              [cards[z]]) #need [] to make it so this returns the string of the card name, not each letter in the name
    else:
        c.execute("UPDATE modern_staples SET last_seen=DateTime('now') WHERE card_name = ?;", [cards[z]])
        
conn.commit() #save
conn.close() #quit
