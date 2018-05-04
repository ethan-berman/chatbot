from textgenrnn import textgenrnn
import argparse
import sys

# Get model_name and input_file arguments
parser = argparse.ArgumentParser()
parser.add_argument('--model_name')
parser.add_argument('--input_file')
parser.add_argument('--num_epochs')
args = parser.parse_args()
model_name = args.model_name
input_file = args.input_file
num_epochs = int(args.num_epochs)

model = textgenrnn(vocab_path='textgenrnn_vocab.json', weights_path='textgenrnn_weights.hdf5')
model.train_from_file(input_file, num_epochs=num_epochs)
model.save(model_name + '.hdf5')
