import random
import os

os.environ['NLTK_DATA'] = os.getcwd() + '/nltk_data'

import nltk
from nltk.tokenize import word_tokenize
from textblob import TextBlob
from nltk.corpus import wordnet
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import stopwords
#nltk.download('stopwords')
import re

from nltk.classify.util import accuracy




##MarkovTextGenerator
from essential_generators import *


class friendlybot:
    user_string = ""
    words = []
    classifier = None

    def feat(self, words):
        stopset = list(set(stopwords.words('english')))
        return dict([(word, True) for word in words.split() if word not in stopset])

    def build_model(self):

        with open("data/pos_tweets.txt") as f:
            nice_list = list(f)

        with open("data/commets.txt") as f:
            not_nice_list = list(f)

        nice = [(self.feat(f), 'positive') for f in nice_list]
        not_nice = [(self.feat(f), 'negative') for f in not_nice_list]
        training = nice +not_nice
        self.classifier = NaiveBayesClassifier.train(training)

    def generate_positive_comments(self):
        comments_list =[]
        return comments_list

    def formatsent(self, sentence):
        return ({word: True for word in word_tokenize(sentence)})

    def __init__(self, user_string):
        self.words, self.user_string = self.data_cleaning(user_string)

    def data_cleaning(self, sentence):
        cleaned = []
        space_tokenizer = nltk.tokenize.SpaceTokenizer()
        word_list = space_tokenizer.tokenize(sentence)

        ## I is not recognized as pronoun if not capital
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

    def sentiment(self, sentence):
        pos = []

    def generate_random_response(self):
        # use default generators
        gen = DocumentGenerator(text_generator=MarkovTextGenerator(), word_generator=MarkovWordGenerator())
        sentence = gen.gen_sentence()
        return sentence

    def classify_comment(self, sentence):
        return self.classifier.classify(self.feat(sentence))



if __name__ == '__main__':

    saying = input()
    chatbot = friendlybot(saying)
    print(chatbot.generate_random_response())
    print(chatbot.antonyms("happy"))
    chatbot.build_model()
    print(chatbot.classify_comment("I will kill you"))





