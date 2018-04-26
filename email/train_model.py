from textgenrnn import textgenrnn

MODEL_NAME = 'peter_emails'

model = textgenrnn()
model.train_from_file('mail.txt', num_epochs=25, batch_size=100)
model.save(MODEL_NAME + '.hdf5')
