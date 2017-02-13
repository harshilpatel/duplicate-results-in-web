import os, requests, sys 
from bs4 import BeautifulSoup
import newspaper
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import *
from datetime import datetime
from app.models import *
from selenium import webdriver

stop = set(stopwords.words('english'))
stemmer = PorterStemmer()


def getGoogleResults(query, quantity, news = True):
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
			driver = webdriver.Chrome(os.getcwd() + '/chromedriver')
			driver.set_window_size(0,0)
			driver.get(url)
			if news:
				for result in driver.find_elements_by_css_selector('div.g'):
					for css in ['a.l', 'a.top']:
						try:
							url = result.find_element_by_css_selector('a.l').get_attribute('href')
							if url:
								print url
								all_results.add(url)
						except: pass
			else:
				for result in driver.find_elements_by_css_selector('.rc'):
					url = result.find_element_by_css_selector('a').get_attribute('href')
					if "youtube.co" not in url:
						print url
						all_results.add(url)
			driver.close()

	all_results = list(set(all_results))

	return all_results


def get_results(query, quantity, force = False, news = True):
	query = query.lower()
	# driver = webdriver.Chrome(os.getcwd() + '/chromedriver')
	# driver.set_window_size(0,0)
	start = datetime.now()

	query = query.replace('_','%20')
	breakdown = 50

	if breakdown > quantity:
		breakdown = quantity

	data_to_be_written = []
	results, created =  webSearch.objects.get_or_create(queryText = query.strip())
	all_results = getGoogleResults(query, quantity, news = True)

	for i in all_results:
		# print "Analysing {0} for keywords".format(i[:20])
		wr, created = WebResource.objects.get_or_create(url = i)
		data = {'url' : i}
		if created:
			a = newspaper.Article(i)
			a.download()
			a.parse()
			try:
				a.nlp()
				keywords = a.keywords
			except:
				keywords = ""
				pass
			if keywords:
				keywords = ",".join([i.encode('utf-8') for i in keywords if i and i in a.text])
			# else:
				# keywords = ""
			data.update({
				'keywords' : keywords,
				'text' : a.text.encode('utf-8'),
				'title' : a.title,
				})
			data_to_be_written.append(data)
			wr.keywords = data.get('keywords')
			wr.text = data.get('text')
			wr.title = data.get('title')
			wr.save()
		else:
			data.update({
				'keywords' : wr.keywords,
				'text' : wr.text,
				'title' : wr.title,
				})
		if wr not in results.results.all():
				results.results.add(wr)
		data_to_be_written.append(data)

	# knowledge = []
	knowledgeKeywords = set([])

	for i in data_to_be_written:
		i['plaintext'] = i.get('text').split('\n') # sentence
		while "" in i['plaintext']:
			i['plaintext'].remove('')

		# structures = []
		# for j in i.get('text'):
			# structures.append(j.split())

		# i['text'] = structures
		try:
			# import pdb; pdb.set_trace()
			keywords = i.get('keywords').split(',')
			for i in keywords:
				knowledgeKeywords.add(i)
		except Exception as e:
			print "ERR - "
			# print e



	knowledgeKeywords = list(knowledgeKeywords)
	knowledgeKeywords.sort()

	for j in range(len(knowledgeKeywords)):
		if j >= len(knowledgeKeywords): continue
		item = knowledgeKeywords[j]
		if item in stop or len(item) <= 1:
			knowledgeKeywords.remove(item)
		

	knowledgeKeywords = list(set(knowledgeKeywords))
	data_to_be_written.append({
		'type' : 'meta',
		'keywords' : list(knowledgeKeywords),
		})
		

	print "Time Taken to get results [Cached/new] {0} minutes".format((datetime.now() - start).seconds/60)
	# driver.close()
	return data_to_be_written