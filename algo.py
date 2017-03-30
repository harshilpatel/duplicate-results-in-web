from __future__ import division
import os, requests, sys 
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "beproject.settings")
django.setup()

# import requests as r
# import ujson
# from pprint import pprint

# api_key = '86522215796d407aafeab6a97f25fe02'
# query = "reddit-r-all"

# response = r.get('https://newsapi.org/v1/articles', params = {'apiKey':api_key, 'source' : query})
# pprint(ujson.loads(response.text))



import os, requests, sys 
from bs4 import BeautifulSoup
import newspaper
import nltk
import string
from nltk.corpus import stopwords
from nltk.stem.porter import *
stop = set(stopwords.words('english'))
from datetime import datetime
from app.models import *
from app.parse2 import *
from selenium import webdriver
from pprint import pprint

from nltk.tokenize import sent_tokenize, word_tokenize
stop = set(stopwords.words('english'))
stemmer = PorterStemmer()
punctuation = string.punctuation
from pattern.en import parse, Text, WORD, POS, CHUNK, PNP, REL, LEMMA
from pattern.vector import words, count, PORTER
from pattern.web import plaintext, collapse_spaces, collapse_tabs
from pattern.vector import Document, Model, TFIDF

items = webSearch.objects.all()

threshold = 0.1
if len(sys.argv) == 2:
    threshold = float(sys.argv[1]) 

def getWords(text):
    return words(text, stemmer = LEMMA,exclude = [],stopwords = False,language = 'en')  # seeing same results with stemmer.stem, LEMMA, PORTER

def cleanSring(text):
    # keywords = [j for j in count(words = words(text), stemmer = PORTER,exclude = [],stopwords = False,language = 'en')]
    # keywords = words(text, stemmer = PORTER,exclude = [],stopwords = False,language = 'en')
    # text = plaintext(text).lower()
    text = sent_tokenize(text.lower())

    # text = parse(text)
    # text = Text(text, token=[LEMMA])

    
    # pprint(keywords)
    
    for i,sentence in enumerate(text):
        words_in_sentence = getWords(sentence)
        # for j,item in enumerate(words_in_sentence):
        #     words_in_sentence[j] = stemmer.stem(item)
            # if item not in keywords:
                # words_in_sentence.remove(item)
        
        # words_in_sentence = collapse_spaces(" ".join(words_in_sentence), indentation = False, replace = " ")
        if len(words_in_sentence) > 0:
            text[i] = sorted(words_in_sentence)
            text[i] = " ".join(text[i])
        else:
            text[i] = ""
        # if "actions" in text[i]:
        #     print text[i]
    
    while "" in text:
        text.remove("")

    # for i,sentence in enumerate(text):
    #     for stops in [[''],['*']]:
    #         while stops in sentence:
    #             sentence.remove(stops)

    # pprint(text)
    # exit(0)
        
    return text

# file = open('news-api.txt','w')
# file2 = open('news-api2.txt','w')
# file.write("#######Start#########\n")
# file2.write("#######Start#########\n")
def calc():
    for item_count,item in enumerate(items):
        print "#"*20
        # file.write("#"*20 + '\n')
        # file2.write("#"*20 + '\n')
        query = item.queryText
        # file.write(query + "\n")
        # file2.write(query + "\n")
        results = item.results.all()
        print "Comparing {0} for {1}".format(len(results), query)

        sources = []
        all_results = [[cleanSring(r.text),r.url] for r in results]
        for r1_count,r1 in enumerate(all_results):
            source = r1
            source_text = r1[0]
            source_url = r1[1]
            # source_text = plaintext(source.text).replace("\n",".").replace('*','').lower()
            # sourceSentence = sent_tokenize(source_text)

            # for stops in ['','*']:
            #     while stops in sourceSentence:
            #         sourceSentence.remove(stops)
            # pprint(sourceSentence)
            # break
            # for i in sourceSentence: pprint(i)
            # sourceCountOfWords =  count(words = source_text,top = 5,stemmer = PORTER,exclude = [],stopwords = False,language = 'en',)

            # print "Source: {0} ".format(r1.url)

            sourceSentence = source_text
            for r_count,r in enumerate(all_results):
                target_text = r[0]
                target_url = r[1]
                if source_url == target_url:
                    continue
                # target_text = r.text
                # targetSentence = sent_tokenize(target_text)
                # w = words(target_text)
                # targetCounOfWords =  count(words = w,top = 5,stemmer = PORTER,exclude = [],stopwords = False,language = 'en',)

                # print len([c for c in count_of_words.keys() if c in source_text])
                # target_text = plaintext(r.text).replace("\n","").replace('*','').lower()
                # targetSentence = sent_tokenize(target_text)

                # targetSentence = cleanSring(r.text)
                targetSentence = target_text
                # similar = list(set(targetSentence).intersection(set(sourceSentence)))
                similar = []
                for SENT in targetSentence:
                    if SENT in sourceSentence and len(SENT) > 1 and SENT not in similar:
                        # print "*" +  SENT + "*"
                        # exit()
                        # print " ".join(SENT)
                        similar.append(SENT)
                        # similar.append("{0} - {1}".format(targetSentence.index(j), sourceSentence.index(j)))
                if len(targetSentence) > 0 and len(sourceSentence) > 0:
                    similarity = len(similar)/(len(set(targetSentence + sourceSentence)))
                    if similarity >= threshold and source_url not in sources and target_url not in sources:
                        sources.append(source_url)
                        pprint("Source: [{0}]{1} + Target: [{2}]{3} - SIM: {4}".format(r1_count,source_url[:40], r_count,target_url[:40], similarity, len(similar), len((sourceSentence))))
                        # file.write("Source: [{0}]{1} + Target: [{2}]{3} - similarity: {4}\n".format(r1_count,r1.url, r_count,r.url, similarity))
                        # file2.write("Source: [{0}]{1} + Target: [{2}]{3} - similarity: {4}\n".format(r1_count,r1.url[:20], r_count,r.url[:20], similarity))
                    
                # print r_count

# file.close()
# file2.close()

def analyse():
    for item_count,item in enumerate(items):
        print "^"*10
        print item.queryText
        result = get_results(item.queryText, 50)

        for i in result:
            if i.get('type')=='similar' and i.get('score')>threshold:
                print "{0} {1} {2}".format(i.get('source')[:20], i.get('dest')[:20], i.get('score'))

# calc()
analyse()