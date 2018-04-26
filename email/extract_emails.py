from bs4 import BeautifulSoup
import mailbox
import pickle
import time
import re

FILE_NAME = "All mail Including Spam and Trash.mbox"
FROM_EMAIL = "warwick_marangos18@milton.edu"

mail = mailbox.mbox(FILE_NAME)

total = len(mail)

messages = []

# Gets plain text body of email
def get_message_body(message):
    body = None
    if message.is_multipart():
        for part in message.walk():
            if part.is_multipart():
                for subpart in part.walk():
                    if subpart.get_content_type() == 'text/plain':
                        body = subpart.get_payload(decode=True)
            elif part.get_content_type() == 'text/plain':
                body = part.get_payload(decode=True)
    elif message.get_content_type() == 'text/plain':
        body = message.get_payload(decode=True)
    return body

def get_timestamp(mail_date):
    timestamp = time.mktime(time.strptime(mail_date, '%a, %d %b %Y %H:%M:%S %z'))
    return timestamp

for i, mail_item in enumerate(mail):
    if i % 10 == 0:
        print ('%s of %s' % (i, total))

    info = mail_item.items()
    # info is in format [[name, value], [name, value]]
    # Potentially Useful Names:
    # "From"
    # "Date"
    # "Delivered-To"
    # "Received"
    # "Subject"
    # "Sender"
    # "X-Original-Sender"

    # Extract needed values from info
    correct_sender = False
    received_time = None
    date = None
    for info_item in info:
        # Check if message was sent by FROM_EMAIL
        if info_item[0] == "From":
            if FROM_EMAIL in info_item[1]:
                correct_sender = True
        # Get message timestamp
        if info_item[0] == "Date":
            date = info_item[1]

    if not correct_sender:
        continue

    timestamp = get_timestamp(date)

    messages.append([mail_item, get_message_body(mail_item), timestamp])

pickle.dump(messages, open('messages.pickle', 'wb+'))
