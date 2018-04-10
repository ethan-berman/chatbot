import numpy as np
import sqlite3
from pathlib import Path
#trademark Ethan Berman
#add functionality to predict reply that program will receive, and then train on loss to the actual reply it receives, so that through continued talking the program gets closer and closer to saying what I would actually say
#use dsouzarc imessage parsing to get messages that are not part of groupchats.  Link to his repo in readme.

running = True
known_words = []
home  = str(Path.home())
fd = sqlite3.connect(home + "/Library/Messages/chat.db")
c = fd.cursor()

num_user = max(c.execute("select ROWID from handle;"))
print(num_user[0])
conv = []
for i in range(1,num_user[0]):
    received = c.execute("SELECT text, date FROM chat INNER JOIN handle ON chat.chat_identifier = handle.id INNER JOIN chat_handle_join ON  handle.ROWID= chat_handle_join.handle_id INNER JOIN message ON message.handle_id = chat_handle_join.handle_id where message.handle_id=" +str(i) +" and message.is_from_me=0;")
    income = received.fetchall()
    sent = c.execute("SELECT text, date FROM chat INNER JOIN handle ON chat.chat_identifier = handle.id INNER JOIN chat_handle_join ON  handle.ROWID= chat_handle_join.handle_id INNER JOIN message ON message.handle_id = chat_handle_join.handle_id where message.handle_id=" +str(i) +" and message.is_from_me=1;")
    outgo = sent.fetchall()
    entry = (income,outgo)
    conv.append(entry)
text_words = c.execute("select text from message;")
print(conv)
#print(conv[420][1])
#flatten lists of received and sent messages in tuple form, make new list from recieved that has all received texts, dates, and sender info in individual tuples.  Then concatenate the lists and sort by date.
def flatten(thread):
    flat = []
    for i in range(len(thread)):
        for item in thread[i]:
            flat.append([item[0],item[1], i])
    flat.sort(key=lambda x: x[1])
    return(flat)
#print(flatten(conv[420]))
inputs = []
for entry in conv:
    inputs.append(flatten(entry))
#print(inputs)
conv_list = []
inputs = list(filter(None,inputs))
clean_inputs = []
for item in inputs:
    if item == []:
        pass
    else:
        starter = item[0][2]
        cindex = []
        for i in range(1, len(item)):
            if(item[i][2] == starter):
                if(len(item[i-1]) != 0 and type(item[i][0]) == str and type(item[i-1][0]) == str):
                    #print(item[i-1])
                    #print(item[i-1][0])
                    item[i-1][0] = item[i-1][0] + " " + item[i][0]
                    item[i] = []
            else:
                starter = item[i][2]
    for thread in item:
        for value in range(len(thread)):
            if(value==None):
                thread.remove(None)
    item = list(filter(None,item))
    dict_entry = {}
    if(item[0][2] == 0):
        for i in range(0,(len(item)-1),2):
            dict_entry[item[i][0]] = item[i+1][0]
    else:
        for i in range(1,(len(item)-1),2):
            dict_entry[item[i][0]] = item[i+1][0]
    '''
    for i in range(0,len(item), 2):
        if(item[i][2] == 0):
            #if message is from other person, my reply is output
            dict_entry[item[i][0]] = item[i+1][0]
        else:
            pass
    '''
    clean_inputs.append(item)
    conv_list.append(dict_entry)
#print(conv_list)
new_attempt = []
for item in clean_inputs:
    dict_entry = {}
    for i in range(0,len(item)-2,2):
        if(item[0][2] == 0):
            #if first message is incoming
            dict_entry[item[i][0]] = item[i+1][0]
        else:
            #if first message is outgoing
            dict_entry[item[i+1][0]] = item[i+2][0]

    '''
    if(item[0][2] == 0):
        for i in range(0,len(item)-1,2):
            dict_entry[item[i][0]] = item[i+1][0]
    else:
        for i in range(1,len(item)-1,2):
            dict_entry[item[i][0]] = item[i+1][0]
    '''
    new_attempt.append(dict_entry)
while(running == True):
    text = input("")
    words = text.split(' ')
    for w in words:
        if w not in known_words:
            known_words.append(w)
    print(known_words)
    if(int(text) < len(new_attempt)):
        print(new_attempt[int(text)])

    if(text == ".quit"):
        running =  False

