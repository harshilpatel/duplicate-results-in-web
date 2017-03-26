import os, requests, sys 
from bs4 import BeautifulSoup
import newspaper
import nltk
import string
from nltk.corpus import stopwords
from nltk.stem.porter import *
from datetime import datetime
from selenium import webdriver
from pprint import pprint

from nltk.tokenize import sent_tokenize, word_tokenize
from pattern.en import parse, Text, WORD, POS, CHUNK, PNP, REL, LEMMA
from pattern.vector import words, count, PORTER
from pattern.web import plaintext, collapse_spaces, collapse_tabs
from pattern.vector import Document, Model, TFIDF


stop = set(stopwords.words('english'))
stemmer = PorterStemmer()
punctuation = string.punctuation

d1 = "Sevaral cats attacked the master to grab food. It was hell."
d2 = "Several dogs attacked the master to grab food. It was cruel."
d3 = "Several animals attacked the master to grab food. It was ruined."


documents = [d1, d2, d3]

def hash_text(text):
  text = text.split()
  

for iIndex, i in enumerate(documents):
  iArray = []


  for jIndex, j in enumerate(documents[iIndex:]):
    print j