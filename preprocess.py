import nltk
from nltk.tokenize import word_tokenize
import string


def preprocess(text):

    tokens = word_tokenize(text)

    tokens = [word for word in tokens if word not in string.punctuation]

    return " ".join(tokens)
