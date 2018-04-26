from textgenrnn import textgenrnn

MODEL_NAME = 'peter_emails'
NUM = 10
TEMPERATURE = 0.6

model = textgenrnn(MODEL_NAME + '.hdf5')

generated = model.generate(NUM, return_as_list=True, temperature=TEMPERATURE)

for message in generated:
    message = message.replace('%%', '\n')
    print(message)
    print()
    print('-'*100)
