import os, requests, sys 
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "beproject.settings")
django.setup()

# start parse and let this boy train
from bs4 import BeautifulSoup
import newspaper
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import *
from datetime import datetime
from app.models import *
from selenium import webdriver
from pprint import pprint
stop = set(stopwords.words('english'))
stemmer = PorterStemmer()

from selenium import webdriver
from app.parse2 import get_results

# sample = ['sasikala', 'modi', 'trump h1b', 'infosys', 'tcs', '']
sample = []
if os.environ.get('heroku'):
	url = "http://www.news.google.co.in"
	r = requests.get(url)
	soup = BeautifulSoup(requests.get(url).text, 'lxml')
	for link in soup.find_all('a'):
		for item in link.text.encode('utf-8', 'replace').split(" "):
			item = item.lower()
			item = item.replace("'","").replace('"','')
			if item not in stop and item != "" and len(item) > 3:
				sample.append(item)
else:
	driver = webdriver.Chrome(os.getcwd() + '/chromedriver')

	driver.get('http://news.google.com')

	sample = []

	for i in driver.find_elements_by_css_selector('a'):
		for item in i.text.encode('utf-8', 'replace').split(" "):
			item = item.lower()
			item = item.replace("'","").replace('"','')
			if item not in stop and item != "" and len(item) > 3:
				sample.append(item)

	driver.close()
sample = list(set(sample))

print(len(sample))

pprint(sample)

for i in sample:
	get_results(i, 50)