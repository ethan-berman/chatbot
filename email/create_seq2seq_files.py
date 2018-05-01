import pickle
import re

mail = pickle.load(open('messages.pickle', 'rb'))

mail = sorted(mail, key=lambda x: x[2])

in_messages = []
out_messages = []
vocab = set()

for message in mail:
    message_text = message[1]

    # Replace Return Characters with <ret>
    message_text = message_text.replace(b'\r\n', b'<ret>')
    message_text = message_text.replace(b'\n', b'<ret>')

    # Check for incoming message
    reply_start = message_text.find(b'<ret>>')
    if reply_start == -1:
        continue

    # Cut off more than one reply
    second_reply_start = message_text.find(b'<ret>>>')
    if second_reply_start != -1:
        message_text = message_text[:second_reply_start]
    
    incoming = message_text[reply_start:].replace(b'<ret>>', b'<ret>')
    response = message_text[:reply_start]

    # Pad returns to count as separate words
    incoming = incoming.replace(b'<ret>', b' <ret> ')
    response = response.replace(b'<ret>', b' <ret> ')

    # Remove double spaces
    while incoming.find(b'  ') != -1 or response.find(b'  ') != -1:
        incoming = incoming.replace(b'  ', b' ')
        response = response.replace(b'  ', b' ')
    incoming = incoming.strip()
    response = response.strip()

    # Remove response prefixes

    incoming = re.sub(r'On (?:Mon|Tue|Wed|Thu|Fri|Sat|Sun), (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec).+wrote', '', incoming.decode())
    response = re.sub(r'On (?:Mon|Tue|Wed|Thu|Fri|Sat|Sun), (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec).+wrote', '', response.decode())
    incoming = re.sub(r'On (?:Mon|Tue|Wed|Thu|Fri|Sat|Sun), (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec).+\@[a-zA-Z]+\.[a-zA-Z]+', '', incoming)
    response = re.sub(r'On (?:Mon|Tue|Wed|Thu|Fri|Sat|Sun), (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec).+\@[a-zA-Z]+\.[a-zA-Z]+', '', response)

    # Remove punctuation
    punctuation = '.,()!?/\\:\'"*[]@#$%^&-+_=;'
    incoming = ''.join([ch for ch in incoming if ch not in punctuation])
    response = ''.join([ch for ch in response if ch not in punctuation])

    print(incoming)
    print('-'*50)
    print(response)
    print('-'*200)

    in_messages.append(incoming)
    out_messages.append(response)

    vocab |= set(incoming.split(' '))
    vocab |= set(response.split(' '))


vocab_file = open('vocab', 'wb')
vocab_text = '\n'.join(list(vocab))
vocab_file.write(vocab_text.encode())

in_file = open('email.in', 'wb')
in_file.write('\n'.join(in_messages).encode())

out_file = open('email.out', 'wb')
out_file.write('\n'.join(out_messages).encode())
