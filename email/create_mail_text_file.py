import pickle

mail = pickle.load(open('messages.pickle', 'rb'))

mail = sorted(mail, key=lambda x: x[2])

out_file = open('mail.txt', 'wb+')

for message in mail:
    message_text = message[1]

    # Replace Return Characters with %% (a likely unused character combo)
    message_text = message_text.replace(b'\r\n', b'%%')
    message_text = message_text.replace(b'\n', b'%%')

    # Write each message on a new line
    out_file.write(message_text + b'\n')

out_file.close()
