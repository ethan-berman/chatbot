from textgenrnn import textgenrnn

MODEL_NAME = 'berman'

model = textgenrnn(MODEL_NAME + '.hdf5')

def generate(num, temperature):
    generated = model.generate(num, return_as_list=True, temperature=temperature)
    for message in generated:
        message = message.replace('%%', '\n')
        print(message)
        print()
        print('-'*100)

generate(1, 0.8)
