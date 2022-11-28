import re
import  nltk
from nltk.util import ngrams, everygrams, pad_sequence
from nltk.tokenize import word_tokenize
from nltk.lm import MLE, WittenBellInterpolated
from pprint import pprint
from const import SEARCH_TEXT
n = 4

input_text = SEARCH_TEXT.lower()
def tokenize(text, n):
    return list(pad_sequence(word_tokenize(text), n, pad_left=True, left_pad_symbol = "<s>"))

def get_grams(text, n):
    return list(everygrams(tokenized, max_len=n))

def create_model(tokenized, n):
    model = WittenBellInterpolated(n)
    model.fit([ngrams], vocabulary_text=tokenized)
    return model


