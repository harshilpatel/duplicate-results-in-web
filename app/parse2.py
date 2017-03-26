import os, requests, sys, string
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
punctuation = string.punctuation
from pattern.en import parse
from pattern.vector import words, count, PORTER, Document, Model, KMEANS, LEMMA
from pattern.web import plaintext, find_urls, strip_between

# driver = webdriver.Chrome()
# driver.set_window_size(0,0)

def getGoogleResults(query, quantity, news = False):
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
			driver = webdriver.Chrome()
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

	# all_results = list(set(all_results))
	# print len(all_results)

	return all_results


def get_results(query, quantity, force = False, news = True):
	query = query.lower()
	# driver = webdriver.Chrome()
	# driver.set_window_size(0,0)
	start = datetime.now()

	query = query.replace('_','%20')
	breakdown = 50

	if breakdown > quantity:
		breakdown = quantity

	data_to_be_written = []
	knowledgeKeywords = []	
	results, created =  webSearch.objects.get_or_create(queryText = query.strip())
	all_results = getGoogleResults(query, quantity)

	if len(all_results) == 0:
  		all_results = [r.url for r in results.results.all()[:quantity] ]

	for i in all_results:
		try:
			# print "Analysing {0}".format(i)
			wr, created = WebResource.objects.get_or_create(url = i)
			data = {'url' : i}
			if created or force:
				a = newspaper.Article(i)
				try:
					a.download()
					a.parse()
					# a.nlp()
					# text = a.text
				except:
					print "Failed"
					# continue

				# print a.authors

				text = a.text
				if 'books.google' in data.get('url'):
					text = ''
				# w = words(text)
				c = count(words = words(text),top = 10,stemmer = LEMMA,exclude = [],stopwords = False,language = 'en') # need the count ?
				# w = words(text,top = 5,stemmer = LEMMA,exclude = [],stopwords = False,language = 'en')				
				
				keywords = ",".join([w for w in c])
				# print keywords
				# print keywords
				data.update({
					'keywords' : keywords,
					'text' : text.encode('utf-8'),
					'title' : a.title,
					'urls' : ",".join(find_urls(strip_between("<body*>","</body", text))),
					'type' : 'result',
					})

				# data_to_be_written.append(data)
				
				wr.keywords = data.get('keywords')
				wr.text = data.get('text')
				wr.title = data.get('title')
				wr.save()
			else:
				data.update({
					'keywords' : wr.keywords,
					'text' : wr.text,
					'title' : wr.title,
					'urls' : wr.urls,
					'type' : 'result',
					})

			if wr not in results.results.all():
				results.results.add(wr)

			data['plaintext'] = data['text'].split('\n') # sentence

			while "" in data['plaintext']:
				data['plaintext'].remove('')

			knowledgeKeywords.extend(data['keywords'].split(','))

			data_to_be_written.append(data)
		except Exception as e:
			print ""
			# print e


	# for i in data_to_be_written:
	# 	i['plaintext'] = i.get('text').split('\n') # sentence
	# 	while "" in i['plaintext']:
	# 		i['plaintext'].remove('')
		
	# 	knowledgeKeywords.extend(i.get('keywords').split(','))

		# structures = []
		# for j in i.get('text'):
			# structures.append(j.split())

		# i['text'] = structures
		# try:
			# import pdb; pdb.set_trace()
			# keywords = i.get('keywords').split(',')
			# for i in keywords:
				# knowledgeKeywords.add(i)
		# except Exception as e:
			# print "ERR - "
			# print e



	# knowledgeKeywords = list(set(knowledgeKeywords))
	knowledgeKeywords = count(knowledgeKeywords, top=20, stemmer = LEMMA, exclude=[], stopwords=False, language='en')
	# print knowledgeKeywords
	knowledgeKeywords = list(set([i for i in knowledgeKeywords]))
	knowledgeKeywords.sort()
	# print knowledgeKeywords

	# for j in range(len(knowledgeKeywords)):
	# 	if j >= len(knowledgeKeywords): continue
	# 	item = knowledgeKeywords[j]
	# 	if item in stop or len(item) <= 1:
	# 		knowledgeKeywords.remove(item)
		

	# knowledgeKeywords = list(set(knowledgeKeywords))



	# clustering
	items = []
	for i in data_to_be_written:
		items.append(Document(i.get('text'), name=i.get('url') ))

	m = Model(items)
	k = quantity/10
	c = m.cluster(method=KMEANS, k=k)

	print "{0} Clusters".format(len(c))
	for i in c:
		cluster = []
		k = []
		contains_text = False
		for item in i:
			for data in data_to_be_written:
				if data.get('type') == 'result' and data.get('url')==item.name:
					cluster.append(data.get('url'))
					if data.get('text'):
						k.extend([w for w in count(words(data.get('text')), top=20, stemmer = LEMMA, exclude=[], stopwords=False, language='en')])
						contains_text=True
		cluster = {
			'type' : 'cluster',
			'data' : cluster,
			'keywords' : [w for w in count(k, top=10, stemmer = LEMMA, exclude=[], stopwords=False, language='en')]
		}
		
		cluster['contains_text'] = contains_text

		data_to_be_written.append(cluster)

		if i:
			print "{0} in this cluster".format(len(i))
		# print "\n\n"


	print "{0} results".format(len(data_to_be_written))
	data_to_be_written.append({
		'type' : 'meta',
		'keywords' : knowledgeKeywords,
		})
		

	# print "Time Taken to get results [Cached/new] {0} minutes".format((datetime.now() - start).seconds/60)
	# driver.close()
	return data_to_be_written