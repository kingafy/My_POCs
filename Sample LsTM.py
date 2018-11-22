# -*- coding: utf-8 -*-
"""
Created on Tue Jul  3 14:52:15 2018

@author: Anshuman_Mahapatra
"""

##Small LSTM Recurrent Neural Network

import numpy
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.callbacks import ModelCheckpoint
from keras.utils import np_utils

# load ascii text and covert to lowercase
filename = "D:\Data Science\Data\wonderland.txt"
raw_text = open(filename).read()
raw_text = raw_text.lower()
print(raw_text)

# create mapping of unique chars to integers
chars = sorted(list(set(raw_text)))
char_to_int = dict((c, i) for i, c in enumerate(chars))
print(char_to_int)

n_chars = len(raw_text)
print(raw_text[:20])
n_vocab = len(chars)
print ("Total Characters: ", n_chars)
print ("Total Vocab: ", n_vocab)