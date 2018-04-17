import random
import os

os.environ['NLTK_DATA'] = os.getcwd() + '/nltk_data'

import nltk
from nltk.tokenize import word_tokenize
from textblob import TextBlob
from nltk.corpus import wordnet
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import stopwords
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer


#nltk.download('stopwords')
import re
from nltk.classify.util import accuracy

##MarkovTextGenerator
from essential_generators import *


##implementation of a friendly bot
class friendlybot:

    POSITIVE_RESPONSES = "That sounds good, you should post it"
    NEGATIVE_RESPONE = " Are you sure you want to post that? "
    user_string = ""
    words = []
    classifier = None
    bot = None
    noun, verb, adjective = None, None, None

    #build naive_bayees classifier model and chat_bot
    def __init__(self):
        self.build_model()
        self.chat_bot()

    ##split user's sentence into part of speech
    def find_pos(self):
        text=TextBlob(self.user_string)
        for word, tag in text.pos_tags:
            if tag == 'NN':  # This is a noun
                self.noun = word
            elif tag == 'JJ':
                self.adjective = word
            elif tag.startswith('VB'):
                self.verb = word

    #construct a response to counteract the negative response
    def constructive_response(self):
        self.find_pos()
        noun, verb, adjective = self.noun, self.verb, self.adjective
        noun, verb, adjective = self.noun, self.verb, self.adjective
        if noun:
            if (TextBlob(noun).sentiment.polarity < -0.1):
                return "why is there {} why not there is no {}?".format(noun, self.antonyms(noun).pop(0))

        if verb:
            if (TextBlob(verb).sentiment.polarity < -0.1):
                return "why do you want to {} you should instead {}".format(verb, self.antonyms(verb).pop(0))

        if adjective:
            if (TextBlob(adjective).sentiment.polarity < -0.1):
                return "why {} ? why not {}?".format(adjective, self.antonyms(adjective).pop(0))
        else:
            return self.NEGATIVE_RESPONE

    #split words into tokens
    def feat(self, words):
        stopset = list(set(stopwords.words('english')))
        return dict([(word, True) for word in words.split() if word not in stopset])

    # build classification model
    def build_model(self):

        with open("data/pos_tweets.txt") as f:
            nice_list = list(f)

        #open negative comment data from Kaggle:
        with open("data/neg_comments.txt") as f:
            not_nice_list = list(f)

        nice = [(self.feat(f), 'positive') for f in nice_list]
        not_nice = [(self.feat(f), 'negative') for f in not_nice_list]
        training = nice +not_nice
        self.classifier = NaiveBayesClassifier.train(training)


    def generate_positive_comments(self):
        nice = []
        for word in self.words:
            s = TextBlob(word)
            if s.sentiment.polarity < -0.1:
                ant_list = self.antonyms(word)
                for i in ant_list:
                    s2 = TextBlob(i)
                    if s2.sentiment.polarity > 0.1:
                        nice.append(i)
                        break
            else:
                nice.append(word)

        return ' '.join(nice)

    def formatsent(self, sentence):
        return ({word: True for word in word_tokenize(sentence)})

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

    def chat_bot(self):
        self.bot = ChatBot("Chatterbot", storage_adapter="chatterbot.storage.SQLStorageAdapter")
        self.bot.set_trainer(ChatterBotCorpusTrainer)
        self.bot.train("chatterbot.corpus.english")

    def get_response(self, user_string):
        if "post this" in user_string.lower():

            user_string=re.findall(r'"([^"]*)"', user_string)
            self.words, self.user_string = self.data_cleaning(user_string[0])
            if(self.classify_comment(self.user_string)== 'negative'):
                return  self.constructive_response()
            else:
                 return self.POSITIVE_RESPONSES

        else:
            return str(self.bot.get_response(user_string))




if __name__ == '__main__':

    while True:
        saying = input()
        chatbot = friendlybot()
        print(chatbot.get_response(saying))

   # print(chatbot.generate_random_response())
    #print(chatbot.antonyms("happy"))
    #chatbot.build_model()
    #print(chatbot.classify_comment("I will kill you"))
    #test = TextBlob("kill")
    #print(test.sentiment.polarity)