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
conv = []
for i in range(1,num_user[0]):
    received = c.execute("SELECT distinct text, date FROM chat INNER JOIN handle ON chat.chat_identifier = handle.id INNER JOIN chat_handle_join ON  handle.ROWID= chat_handle_join.handle_id INNER JOIN message ON message.handle_id = chat_handle_join.handle_id where message.handle_id=" +str(i) +" and message.is_from_me=0;")
    income = received.fetchall()
    sent = c.execute("SELECT distinct text, date FROM chat INNER JOIN handle ON chat.chat_identifier = handle.id INNER JOIN chat_handle_join ON  handle.ROWID= chat_handle_join.handle_id INNER JOIN message ON message.handle_id = chat_handle_join.handle_id where message.handle_id=" +str(i) +" and message.is_from_me=1;")
    outgo = sent.fetchall()
    entry = (income,outgo)
    print(outgo)
    conv.append(entry)
def flatten(thread):
    flat = []
    for i in range(len(thread)):
        for item in thread[i]:
            flat.append([item[0],item[1], i])
    flat.sort(key=lambda x: x[1])
    return(flat)
inputs = []
for entry in conv:
    cleaned = flatten(entry)
    cleaned = list(filter(None,cleaned))
    inputs.append(cleaned)
#print(inputs)
conv_list = []
inputs = list(filter(None,inputs))
clean_inputs = []

def concat(message):
    #input  amessage and output
    outputs = []
    start = message[0][2]
    sample_entry = ["",0,start]
    for item in message:
        if(item[0] is not None):
            if(item[2] == start):
                sample_entry[0] = sample_entry[0] + " " + item[0]
                sample_entry[1] = item[1]
            else:
                start = item[2]
                outputs.append(sample_entry)
                sample_entry = [item[0], item[1], start]
    return(outputs)
'''
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
    for i in range(0,len(item), 2):
        if(item[i][2] == 0):
            #if message is from other person, my reply is output
            dict_entry[item[i][0]] = item[i+1][0]
        else:
            pass

    clean_inputs.append(item)
'''
#print(conv_list)
new_attempt = [] 
'''
fresh_inputs = []
for item in inputs:
    fresh_inputs.append(list(filter(None,item)))
'''
for item in inputs:
    item = concat(item)
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

print(new_attempt)
while(running == True):
    text = input("")
    words = text.split(' ')
    for w in words:
        if w not in known_words:
            known_words.append(w)
    print(known_words)
    if(text == ".quit"):
        running =  False

