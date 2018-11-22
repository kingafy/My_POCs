
from __future__ import print_function, division
from builtins import range, input
# Note: you may need to update your version of future
# sudo pip install -U future

import os
import sys
import string
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


from keras.models import Model
from keras.layers import Dense, Embedding, Input, LSTM
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.optimizers import Adam, SGD

import xlsxwriter

workbook = xlsxwriter.Workbook('arrays.xlsx')
worksheet = workbook.add_worksheet()


# some configuration
MAX_SEQUENCE_LENGTH = 100
MAX_VOCAB_SIZE = 3000
EMBEDDING_DIM = 50
VALIDATION_SPLIT = 0.2
BATCH_SIZE = 128
##EPOCHS = 2000
EPOCHS = 200
LATENT_DIM = 25

# load in the data
input_texts = []
target_texts = []
for line in open("D:/Data Science/Sample Codes/machine_learning_examples-master/machine_learning_examples-master/hmm_class/robert_frost.txt"):
  line = line.rstrip()
  if not line:
    continue

  input_line = '<sos> ' + line
  target_line = line + ' <eos>'

  input_texts.append(input_line)
  target_texts.append(target_line)


all_lines = input_texts + target_texts

print(all_lines[:10])

print(len(input_texts))
print(input_texts[:10])
print(target_texts[:10])

# convert the sentences (strings) into integers
##Tokenizer function of keras  to turn text into seq of integers
##num_words param keeps words based on freauency of words
tokenizer = Tokenizer(num_words=MAX_VOCAB_SIZE, filters='')
##change the above to have no limit on VOCAB_SIZE  


tokenizer.fit_on_texts(all_lines)
#print(tokenizer.fit_on_texts(all_lines[:10]))
input_sequences = tokenizer.texts_to_sequences(input_texts)
print(input_texts[:2])
#print(tokenizer.texts_to_sequences(input_texts[:2]))
print(input_sequences[:10])
print(input_texts[:10])
print(type(input_sequences))
target_sequences = tokenizer.texts_to_sequences(target_texts)
print(target_sequences[:10])

# find max seq length
max_sequence_length_from_data = max(len(s) for s in input_sequences)
print('Max sequence length:', max_sequence_length_from_data)


# get word -> integer mapping
word2idx = tokenizer.word_index
##print(type(word2idx))
print('Found %s unique tokens.' % len(word2idx))
## 3056 tokens

##assert('Anshuman' in word2idx)
assert('<eos>' in word2idx)


# pad sequences so that we get a N x T matrix
max_sequence_length = min(max_sequence_length_from_data, MAX_SEQUENCE_LENGTH)
print(max_sequence_length)
##Max Sequence length is 12
#PAd sequencing for ones which are less the max seq lenght of line
input_sequences = pad_sequences(input_sequences, maxlen=max_sequence_length, padding='post')
target_sequences = pad_sequences(target_sequences, maxlen=max_sequence_length, padding='post')
print('Shape of data tensor:', input_sequences.shape)
print(type(input_sequences))



# load in pre-trained word vectors
print('Loading word vectors...')
word2vec = {}
#with open(os.path.join('D:/Data Science/Data/glove/glove.6B" % EMBEDDING_DIM)) as f:
#with open("D:/Data Science/Data/glove.6B.50d.txt','rb') as f:
with open(f'D:/Data Science/Data/glove.6B/glove.6B.50d.txt', 'rb') as f:
  # is just a space-separated text file in the format:
  # word vec[0] vec[1] vec[2] ...
  for line in f:
    values = line.split()
    word = values[0]
    vec = np.asarray(values[1:], dtype='float32')
    word2vec[word] = vec
print('Found %s word vectors.' % len(word2vec))
print(type(word2vec))



# prepare embedding matrix
print('Filling pre-trained embeddings...')
num_words = min(MAX_VOCAB_SIZE, len(word2idx) + 1)
print(num_words)
print(len(word2idx))
print(EMBEDDING_DIM)
##First have the embedding matrix created to have all zeroes and then populate it.The embedding matrix will be vocab size and dimensions defined
embedding_matrix = np.zeros((num_words, EMBEDDING_DIM))
print(embedding_matrix)

print("MAX VOCAB SIZE is %d" %MAX_VOCAB_SIZE)
for word, i in word2idx.items():
  if i < MAX_VOCAB_SIZE:
    embedding_vector = word2vec.get(word)
    if embedding_vector is not None:
      # words not found in embedding index will be all zeros.
      embedding_matrix[i] = embedding_vector

print(embedding_matrix)

print(embedding_matrix[:,1])
print(type(embedding_matrix))

print(embedding_matrix.shape)

np.savetxt("D:/Data Science/POC/matrix_embedding.csv", embedding_matrix, delimiter=",")

print(len(input_sequences))##1436
print(max_sequence_length) ###12
print(num_words)  ###3000
# one-hot the targets (can't use sparse cross-entropy)
one_hot_targets = np.zeros((len(input_sequences), max_sequence_length, num_words))
print(one_hot_targets.shape)
for i, target_sequence in enumerate(target_sequences):
  for t, word in enumerate(target_sequence):
    if word > 0:
      one_hot_targets[i, t, word] = 1


print(num_words)
print(EMBEDDING_DIM)

# load pre-trained word embeddings into an Embedding layer
embedding_layer = Embedding(
  num_words,
  EMBEDDING_DIM,
  weights=[embedding_matrix],
  # trainable=False
)



print('Building model...')

# create an LSTM network with a single LSTM
input_ = Input(shape=(max_sequence_length,))
initial_h = Input(shape=(LATENT_DIM,))
initial_c = Input(shape=(LATENT_DIM,))
x = embedding_layer(input_)
lstm = LSTM(LATENT_DIM, return_sequences=True, return_state=True)
x, _, _ = lstm(x, initial_state=[initial_h, initial_c]) # don't need the states here
dense = Dense(num_words, activation='softmax')
output = dense(x)

model = Model([input_, initial_h, initial_c], output)
model.compile(
  loss='categorical_crossentropy',
  # optimizer='rmsprop',
  optimizer=Adam(lr=0.01),
  # optimizer=SGD(lr=0.01, momentum=0.9),
  metrics=['accuracy']
)

print('Training model...')
z = np.zeros((len(input_sequences), LATENT_DIM))
r = model.fit(
  [input_sequences, z, z],
  one_hot_targets,
  batch_size=BATCH_SIZE,
  epochs=EPOCHS,
  validation_split=VALIDATION_SPLIT
)

# plot some data
plt.plot(r.history['loss'], label='loss')
plt.plot(r.history['val_loss'], label='val_loss')
plt.legend()
plt.show()

# accuracies
plt.plot(r.history['acc'], label='acc')
plt.plot(r.history['val_acc'], label='val_acc')
plt.legend()
plt.show()



# make a sampling model
input2 = Input(shape=(1,)) # we'll only input one word at a time
x = embedding_layer(input2)
x, h, c = lstm(x, initial_state=[initial_h, initial_c]) # now we need states to feed back in
output2 = dense(x)
sampling_model = Model([input2, initial_h, initial_c], [output2, h, c])


# reverse word2idx dictionary to get back words
# during prediction
idx2word = {v:k for k, v in word2idx.items()}


def sample_line():
  # initial inputs
  np_input = np.array([[ word2idx['<sos>'] ]])
  h = np.zeros((1, LATENT_DIM))
  c = np.zeros((1, LATENT_DIM))

  # so we know when to quit
  eos = word2idx['<eos>']

  # store the output here
  output_sentence = []

  for _ in range(max_sequence_length):
    o, h, c = sampling_model.predict([np_input, h, c])

    # print("o.shape:", o.shape, o[0,0,:10])
    # idx = np.argmax(o[0,0])
    probs = o[0,0]
    if np.argmax(probs) == 0:
      print("wtf")
    probs[0] = 0
    probs /= probs.sum()
    idx = np.random.choice(len(probs), p=probs)
    if idx == eos:
      break

    # accuulate output
    output_sentence.append(idx2word.get(idx, '<WTF %s>' % idx))

    # make the next input into model
    np_input[0,0] = idx

  return ' '.join(output_sentence)

# generate a 4 line poem
while True:
  for _ in range(4):
    print(sample_line())

  ans = input("---generate another? [Y/n]---")
  if ans and ans[0].lower().startswith('n'):
    break


