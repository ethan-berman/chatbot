import numpy as np
import sqlite3
#trademark Ethan Berman
#add functionality to predict reply that program will receive, and then train on loss to the actual reply it receives, so that through continued talking the program gets closer and closer to saying what I would actually say
running = True
known_words = []

fd = sqlite3.connect("/Users/ethanberman/Library/Messages/chat.db")
c = fd.cursor()

num_user = max(c.execute("select ROWID from handle;"))
print(num_user[0])
conv = []
for i in range(1,num_user[0]):
    received = c.execute("select text, date from message where handle_id="+str(i)+" and is_from_me=0;")
    sent = c.execute("select text, date from message where handle_id="+str(i)+" and is_from_me=1;")
    conv.append((received.fetchall(),sent.fetchall()))
text_words = c.execute("select text from message;")


#flatten lists of received and sent messages in tuple form, make new list from recieved that has all received texts, dates, and sender info in individual tuples.  Then concatenate the lists and sort by date.
for c in conv:
    for m in c:
        print(m)

for w in text_words:
    if w is not None:
        #print(w)
        pass

while(running == True):
    text = input("")
    words = text.split(' ')
    for w in words:
        if w not in known_words:
            known_words.append(w)
    print(known_words)

    if(text == ".quit"):
        running =  False

