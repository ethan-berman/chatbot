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
    income = received.fetchall()
    sent = c.execute("select text, date from message where handle_id="+str(i)+" and is_from_me=1;")
    outgo = sent.fetchall()
    entry = (income,outgo)
    conv.append(entry)
text_words = c.execute("select text from message;")

#print(conv[420][1])
#flatten lists of received and sent messages in tuple form, make new list from recieved that has all received texts, dates, and sender info in individual tuples.  Then concatenate the lists and sort by date.
def flatten(thread):
    flat = []
    for i in range(len(thread)):
        for item in thread[i]:
            flat.append((item[0],item[1], i))
    flat.sort(key=lambda x: x[1])
    return(flat)
print(flatten(conv[420]))
inputs = []
for entry in conv:
    inputs.append(flatten(entry))
print(inputs)

for item in inputs:
    for i in range(len(item)):
        if(i
while(running == True):
    text = input("")
    words = text.split(' ')
    for w in words:
        if w not in known_words:
            known_words.append(w)
    print(known_words)

    if(text == ".quit"):
        running =  False

