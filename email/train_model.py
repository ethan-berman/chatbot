from textgenrnn import textgenrnn

INPUT_FILE = 'mail.txt'
MODEL_NAME = 'peter_emails'

model = textgenrnn()
model.train_from_file(INPUT_FILE, num_epochs=25, batch_size=100)
model.save(MODEL_NAME + '.hdf5')
