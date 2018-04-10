import sqlite3

fd = sqlite3.connect("/Users/ethanberman/library/messages/chat.db")
c = fd.cursor()

num_user =  len(c.execute("select distinct associated_message_guid from message;").fetchall())
print(num_user)
