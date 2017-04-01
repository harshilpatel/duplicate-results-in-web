from __future__ import division
import math
import os, requests, sys, string
from bs4 import BeautifulSoup
import newspaper
import nltk
import numpy as np
from nltk.corpus import stopwords
from nltk.stem.porter import *
from datetime import datetime
from app.models import *
from selenium import webdriver
from pprint import pprint

from django.core.exceptions import MultipleObjectsReturned

stop = set(stopwords.words('english'))
stemmer = PorterStemmer()
punctuation = string.punctuation
from pattern.en import parse, wordnet
from pattern.vector import words, count, PORTER, Document, Model, KMEANS, LEMMA, TFIDF, HIERARCHICAL
from pattern.web import plaintext, find_urls, strip_between

# driver = webdriver.Chrome()
# driver.set_window_size(0,0)

def parseURL(url, force = False):
	try:
		wr, created = WebResource.objects.get_or_create(url = url)
	except MultipleObjectsReturned:
		WebResource.objects.filter(url = url).delete()

	wr, created = WebResource.objects.get_or_create(url = url)
	if created or force:
		print "Parsing and Caching {0}".format(url)
		a = newspaper.Article(url)
		try:
			a.download()
			a.parse()
			text = a.text
			title = a.title

			if 'books.google' in url:
				text = ''

			wr.text = str(text.encode('utf-8', 'replace').lower())
			wr.title = a.title
			wr.urls = ",".join(find_urls(strip_between("<body*>","</body", text)))
			wr.save()	
		except:
			print "Failed"
	return wr

def getGoogleResults(query, quantity, news = False, force = False):
	all_results = []
	query = query.replace('_','%20')
	breakdown = 50

	if breakdown > quantity:
		breakdown = quantity

	newsParams = ''
	if news:
		newsParams = '&tbm=nws'

	for i in range(0, int(quantity), breakdown):
		if i == 0:
			url = 'https://www.google.com/search?q={0}&num={1}{2}'.format(query, breakdown, newsParams)
		else:
			url = 'https://www.google.com/search?q={0}&num={1}&start={2}{3}'.format(query, breakdown, i, newsParams)
			
		if os.environ.get('heroku'):
			soup = BeautifulSoup(requests.get(url).text, 'lxml')
			for link in soup.find_all('a'):
				href = link.get('href')
				if '/url?q=' in href and 'webcache' not in href:
					href = href.replace('/url?q=', '')
					href = href[:href.index('&sa')]
					all_results.append(href)

		else:
			driver = webdriver.Chrome(os.getcwd()+'/chromedriver')
			driver.set_window_size(0,0)
			driver.get(url)
			if news:
				for result in driver.find_elements_by_css_selector('div.g'):
					for css in ['a.l', 'a.top']:
						try:
							url = result.find_element_by_css_selector('a.l').get_attribute('href')
							if url:
								all_results.add(url)
						except: pass
			else:
				for result in driver.find_elements_by_css_selector('.rc'):
					url = result.find_element_by_css_selector('a').get_attribute('href')
					if "youtube.co" not in url:
						if url in all_results:
							print "Duplicate Results"
						else:
							all_results.append(url)
			driver.close()

	for i in all_results:
		parseURL(i, force)


	return all_results


def get_results(query, quantity, force = False, news = False, analysis = True):
	query = query.lower()
	start = datetime.now()

	query = query.replace('_','%20')
	breakdown = 50

	if breakdown > quantity:
		breakdown = quantity

	data_to_be_written = []
	knowledgeKeywords = []	
	duplicates = []
	results, created =  webSearch.objects.get_or_create(queryText = query.strip())
	if created or force:
		all_results = getGoogleResults(query, quantity, news, force)
	else:
		all_results = []

	if len(all_results) == 0 and not created:
		all_results = [r.url for r in results.results.all()]

	all_results = all_results[:quantity]

	for index, i in enumerate(all_results):
		try:
			wr = parseURL(i, force)

			data = {'url' : i}

			keywords = [w for w in count(wr.text, top = 10, stemmer = LEMMA) if w not in stop]

			if 'books.google' in i:
				text = ''
			else:
				text = wr.text

			data.update({
				'keywords' : keywords,
				'text' : text,
				'title' : wr.title,
				'urls' : wr.urls,
				'type' : 'result',
				'index' : index+1,
				'similar' : [],
				'duplicates' : [],
				'category' : 0,
				})

			if wr not in results.results.all():
				results.results.add(wr)

			data['plaintext'] = data['text'].split('\n')

			while "" in data['plaintext']:
				data['plaintext'].remove('')

			knowledgeKeywords.extend(data['keywords'])

			data_to_be_written.append(data)
		except Exception as e:
			print "ERROR"
			print e

	if not analysis:
		return data_to_be_written


	# knowledgeKeywords = [w for w in count(knowledgeKeywords, top=20, stemmer = LEMMA)]
	# knowledgeKeywords.sort()

	# clustering
	items = []
	for i in data_to_be_written:
		items.append(Document(i.get('text'), name=i.get('url'), description=i.get('index')+1, stemmer = LEMMA))

	m = Model(items, weight=TFIDF)
	k = 10
	c = m.cluster(method=KMEANS, k=k)

	####### BEGIN Experimental Setup ##########

	# Calulation custom modal
	y = len(m.documents)
	# x = len(m.vector)
	v = m.features
	x = len(v)
	d = m.documents
	
	model = np.zeros((y,x))

	for i in range(y):
		for j in range(x):
			if v[j] in d[i].words:
				model[i][j] = 1


	def find_match(model, words = None, d = None):
		y,x = model.shape
		for i in range(y):
			for j in range(i+1,y):
				a = np.copy(model[i])
				b = np.copy(model[j])

				a_ones = np.count_nonzero(a)
				b_ones = np.count_nonzero(b)

				comparison = (a==b)

				score = a*b
				score = np.count_nonzero(score)

				if a_ones+b_ones>0 and a_ones+b_ones-score > 0:
					score = (score)/(a_ones+b_ones-score)
				else:
					score = 0 

				if model[i].any() and model[j].any() and comparison.any() and score > 0.2:
					print "Match [{0}] {1}:[{2}] - [{3}] {4}:[{5}] : {6} words".format(d[i].description,d[i].name[:30], np.count_nonzero(a), d[j].description,d[j].name[:30], np.count_nonzero(b), score, math.fabs(d[i].description - d[j].description))
					similar = {
						'type' : 'similar',
						'source' : d[i].name,
						'dest' : d[j].name,
						'score' : score,
					}
					data_to_be_written.append(similar)

				if score >= 0.9:
					for res in data_to_be_written:
						if res['type'] in ['result','duplicate'] and res['url'] == d[j].name and len(res['text'])>0:
							print "Duplicate {0}.{1}".format(i,j)
							res['type'] = 'duplicate'
		return model

	def idf(model, words = None, documents = None, threshold1 = 0, threshold2 = 0, transpose = False):
		# if transpose:
		# 	model = model.transpose()
		y,x = model.shape
		data = {}

		for i in range(x):
			count = np.count_nonzero(model[:,i])/y
			if count >= threshold1 and count <= threshold2:
				if words:
					data[words[i]] = count
				else:
					data[i] = count
		return data

	def df(text, threshold = 0):
		data = {}
		doc = Document(text, stemmer=PORTER, threshold = threshold)

		return doc.words

	model = find_match(model, v, d)

	knowledgeKeywords = [w for w in idf(model, v,d,0.4,0.7)]

	####### END Experimental Setup ##########

	# for i in c:
	# 	cluster = []
	# 	k = []
	# 	contains_text = False

	# 	for item in i:
	# 		for data in data_to_be_written:
	# 			if data.get('type') == 'result' and data.get('url')==item.name:
	# 				cluster.append({
	# 					'url' : data.get('url'),
	# 					'index' : item.description,
	# 					})
	# 				if data.get('text'):
	# 					k.extend([w for w in count(words(data.get('text')), top=50, stemmer = PORTER, exclude=[], stopwords=False, language='en')])
	# 					contains_text=True
	# 	cluster = {
	# 		'type' : 'cluster',
	# 		'data' : cluster,
	# 		'index' : min([c.get('index') for c in cluster] + [0]),
	# 		'keywords' : [w for w in count(k, top=10, stemmer = PORTER, exclude=[], stopwords=False, language='en')]
	# 	}
		
	# 	cluster['contains_text'] = contains_text

	# 	data_to_be_written.append(cluster)


	print "{0} results".format(len(data_to_be_written))
	data_to_be_written.append({
		'type' : 'meta',
		'keywords' : knowledgeKeywords,
		})
		

	# print "Time Taken to get results [Cached/new] {0} minutes".format((datetime.now() - start).seconds/60)
	# driver.close()


	return data_to_be_written