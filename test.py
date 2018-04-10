import sqlite3

fd = sqlite3.connect("/Users/ethanberman/library/messages/chat.db")
c = fd.cursor()

num_user =  len(c.execute("select distinct associated_message_guid from message;").fetchall())

trial = c.execute('select text from chat inner join handle on chat.chat_identifier = handle.id inner join chat_handle_join on handle.rowid= chat_handle_join.handle_id inner join message on message.handle_id = chat_handle_join.handle_id where message.handle_id=422;')
print(trial.fetchall())
