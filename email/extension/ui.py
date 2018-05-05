from textgenrnn import textgenrnn
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk
import tkinter as tk
import subprocess
import threading
import mailbox
import shlex
import time
import re

email_pattern = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

model = None
mbox_filename = None
messages = []
extracting = False
training = False

# Displays tk alert
def alert(title, text):
    messagebox.showinfo(title, text)

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

# Gets unix timestamp from mail date
def get_timestamp(mail_date):
    timestamp = time.mktime(time.strptime(mail_date, '%a, %d %b %Y %H:%M:%S %z'))
    return timestamp

# Opens file dialog to select mbox
def select_mbox():
    global mbox_filename
    mbox_filename = filedialog.askopenfilename()

    if not mbox_filename:
        mbox_filename = None

    mbox_label.config(text='File Selected: %s' % mbox_filename)

def extract_emails():
    global extracting
    global messages
    global mbox_filename

    # Acquire lock
    if extracting:
        alert('Mbox Error', 'Already busy extracting an mbox file.')
        return
    extracting = True

    target_email=target_email_entry.get().strip()
    if not email_pattern.match(target_email):
        alert('Email Address Error', 'Please enter a valid email address.')
        extracting = False
        return

    try:
        mail = mailbox.mbox(mbox_filename)
    except:
        alert('Mbox Error', 'Please select a valid mbox file.')
        extracting = False
        return

    def func():
        global extracting
        global messages

        # Set small progress to indicate that mail is extracting
        progressbar.config(value=1, maximum=100)

        total = len(mail)        

        # Extract and filter all mail
        for i, mail_item in enumerate(mail):
            progressbar.config(value=i, maximum=total)

            info = mail_item.items()

            # Extract needed values from info
            correct_sender = False
            received_time = None
            date = None
            for info_item in info:
                # Check if message was sent by target_email
                if info_item[0] == "From":
                    if target_email in info_item[1]:
                        correct_sender = True
                # Get message timestamp
                if info_item[0] == "Date":
                    date = info_item[1]

            if not correct_sender:
                continue

            timestamp = get_timestamp(date)

            messages.append([mail_item, get_message_body(mail_item), timestamp])
    
        # Sort by timestamp
        messages = sorted(messages, key=lambda x: x[2])

        # Generate text file for training
        out_file = open('mail.txt', 'wb+')
        for message in messages:
            message_text = message[1]

            # Replace Return Characters with <ret> for returns
            message_text = message_text.replace(b'\r\n', b'<ret>')
            message_text = message_text.replace(b'\n', b'<ret>')

            out_file.write(message_text + b'\n')

        out_file.close()

        progressbar.config(value=0, maximum=1)

        extracting = False
    
    threading.Thread(target=func).start()

# stdout callback function for lines read from external process
def stdout_callback(stdout_line):
    print(stdout_line)
    train_output_text.config(state='normal')
    train_output_text.delete('1.0', tk.END)
    train_output_text.insert('1.0', stdout_line)
    train_output_text.config(state='disabled')

# Run command externally - used to train model
def run_command(command):
    process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE)
    while True:
        output = process.stdout.readline().decode()
        if output == '' and process.poll() is not None:
            break
        if output:
            stdout_callback(output)
    rc = process.poll()
    return rc

def train():
    global training
    if training:
        alert('Training Error', 'Already busy training.')
        return
    training = True

    def func():
        global training
        num_epochs = num_epochs_scale.get()
        run_command('./dist/model.exe --model_name=mail --input_file=mail.txt --num_epochs=%s' % num_epochs)
        training = False

    threading.Thread(target=func).start()

def load_model():
    global model
    if model is not None:
        return
    model = textgenrnn('mail.hdf5')

def generate():
    load_model()
    generated = model.generate(5, return_as_list=True, temperature=temperature_scale.get())


    train_output_text.config(state='normal')
    train_output_text.delete('1.0', tk.END)

    for message in generated:
        message = message.replace('<ret>', '\n')
        train_output_text.insert('1.0', message)
        train_output_text.insert('1.0', '\n')
        train_output_text.insert('1.0', '-'*100)
        train_output_text.insert('1.0', '\n')
        
    train_output_text.config(state='disabled')

root = tk.Tk()
root.rowconfigure(0, weight=1)
root.columnconfigure(1, weight=1)

# Controls Frame
controls_frame = tk.Frame(root)
controls_frame.grid(row=0, column=0, sticky='new')

help_button = ttk.Button(controls_frame, text='Help')
help_button.grid(row=0, column=0, columnspan=2, sticky='ew')

select_mbox_button = ttk.Button(controls_frame, text='Select Mbox File', command=lambda:select_mbox())
select_mbox_button.grid(row=1, column=0, sticky='w')

mbox_label = ttk.Label(controls_frame, text='File Selected: %s' % mbox_filename, wraplength=120, justify=tk.LEFT)
mbox_label.grid(row=1, column=1, sticky='ew')

target_email_label = ttk.Label(controls_frame, text='Target Email: ')
target_email_label.grid(row=2, column=0, sticky='w')

target_email_entry = ttk.Entry(controls_frame)
target_email_entry.grid(row=2, column=1, sticky='ew')

load_emails_button = ttk.Button(controls_frame, text='Extract Emails', command=lambda:extract_emails())
load_emails_button.grid(row=3, column=0, columnspan=2, sticky='ew')

progressbar = ttk.Progressbar(controls_frame)
progressbar.grid(row=4, column=0, columnspan=2, sticky='ew')

num_epochs_label = ttk.Label(controls_frame, text='Num Epochs: ')
num_epochs_label.grid(row=5, column=0, sticky='w')

num_epochs_scale = tk.Scale(controls_frame, from_=1, to=25, resolution=1, orient=tk.HORIZONTAL)
num_epochs_scale.grid(row=5, column=1, sticky='ew')

train_button = ttk.Button(controls_frame, text='Train Model', command=lambda: train())
train_button.grid(row=6, column=0, columnspan=2, sticky='ew')

temperature_label = tk.Label(controls_frame, text='Temperature: ')
temperature_label.grid(row=7, column=0, sticky='w')

temperature_scale = tk.Scale(controls_frame, from_=0, to=2, resolution=0.01, orient=tk.HORIZONTAL)
temperature_scale.grid(row=7, column=1, sticky='ew')

generate_button = ttk.Button(controls_frame, text='Generate', command=generate)
generate_button.grid(row=8, column=0, columnspan=2, sticky='ew')

# Log Frame
log_frame = tk.Frame(root)
log_frame.grid(row=0, column=1, sticky='nsew')
log_frame.rowconfigure(1, weight=1)
log_frame.columnconfigure(0, weight=1)

train_output_label = tk.Label(log_frame, text='Log')
train_output_label.grid(row=0, column=0, sticky='w')

train_output_text = tk.Text(log_frame, width=50, height=20, state='disabled')
train_output_text.grid(row=1, column=0, sticky='nsew')

root.mainloop()
