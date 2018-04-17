
import random
import os
os.environ['NLTK_DATA'] = os.getcwd() + '/nltk_data'
import nltk
from textblob import TextBlob
from nltk.corpus import wordnet

class friendlybot:
    user_string = ""
    words = []

    def __init__(self, user_string):
        self.words, self.user_string = self.data_cleaning(user_string)

    def data_cleaning(self, sentence):
        cleaned = []
        space_tokenizer = nltk.tokenize.SpaceTokenizer()
        word_list = space_tokenizer.tokenize(sentence)
        for word in word_list:
            if word == 'i':
                word = 'I'
            if word == "i'm":
                word = "I'm"
            cleaned.append(word)
        return word_list, ' '.join(cleaned)

    def antonyms(self, word):
        antonyms = []
        for syn in wordnet.synsets(word):
            for a in syn.lemmas():
                if a.antonyms():
                    antonyms.append(a.antonyms()[0].name())
        return antonyms



