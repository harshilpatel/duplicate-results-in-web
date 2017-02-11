import requests
from bs4 import BeautifulSoup
# import scrap
from pprint import pprint
import sys
import os
from newspaper import Article
import time
import json
from selenium import webdriver
from datetime import datetime
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import *
from app.models import link, wordCandidate, contextualCandidates, structuralCandidates
import operator
from django.db.models import Q
import re, string, htmlentitydefs
regex = re.compile('[%s]' % re.escape(string.punctuation))

if 'RDS_DB_NAME' in os.environ:
	from pyvirtualdisplay import Display
	display = Display(visible=0, size=(800, 600))
	display.start()


def fixup(m):
	text = m.group(0)
	if text[:2] == "&#":
		# character reference
		try:
			if text[:3] == "&#x":
				return unichr(int(text[3:-1], 16))
			else:
				return unichr(int(text[2:-1]))
		except ValueError:
			pass
	else:
		# named entity
		try:
			text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
		except KeyError:
			pass
	return text # leave as is

def parseResults(results, force = False):
	# print "Analysing %s articles" %str(len(results))
	# print results
	returnData = []
	stop = set(stopwords.words('english'))
	stemmer = PorterStemmer()
	for i in results:
		# print i
		if not force:
			try:
				item = link.objects.get(url = i)
				context = {'url' : item.url, 'title' : item.title, 'text' : item.text}
				returnData.append(context)
				# print "Found - {0} / skipped".format(context.get('url'))
				continue
			except:
				pass

		# print "Calculating NEW URL"
		# print "New - {0}".format(i)
		data = {}
		if 'webcache' in i or (i.count('/') <= 3 and i[-1:] == '/'):
			print "Err - Cached Google link / skipped"
			continue
		article = Article(i)
		article.download()
		# try:

		article.parse()
		text = article.text.encode('ascii', 'ignore').lower()
		text = re.sub('&#?\w+;:', fixup, text)
		data.update({
			'url' : i.encode('utf-8'),
			'title' : article.title.encode('ascii', 'ignore'),
			'text' : text,
		})

		structure = text.replace('\n\n','\n').split('\n')
		resultLinks, created = link.objects.get_or_create(url = i, title = data['title'])
		for count,para in enumerate(structure):

			text = para.split('.')
			structures = []
			for sentence in text:
				# print sentence
				# sentence = sentence.replace(",", " , ")
				tokens = nltk.word_tokenize(sentence)
				new_tokens = []

				for token in tokens: 
					new_token = regex.sub(u'', token)
					if not new_token == u'':
						new_tokens.append(new_token)
					
				tagged = nltk.pos_tag(new_tokens)

				context = []
				for group in tagged:
					word, feature = group
					word = stemmer.stem(word)
					word = word.strip()
					if word and word not in stop:
						wordC, created  = wordCandidate.objects.get_or_create(text = word, feature = feature)
						# if not created: print "Found exisiting word - {0}".format(word)
						context.append(wordC)

				q_objects = []
				for c in context:
					q_objects.append(Q(wordCandidates = c))

				if len(q_objects) > 0:
					contextualCFilter = contextualCandidates.objects.filter(reduce(operator.and_, q_objects)) # look for matching sentence with same context
					for cc in contextualCFilter:
						if context == list(cc.wordCandidates.all()):
							# print "Found existing Sentence - {0}".format(sentence)
							contextualC = cc
							# print "Match found"
							break
					else:
						contextualC = contextualCandidates.objects.create()
						contextualC.wordCandidates.set(context)
					structures.append(contextualC)

			q_objects = []
			for s in structures:
				q_objects.append(Q(contextualCandidates = s))

			if len(q_objects) > 0:
				structuralCFilter = structuralCandidates.objects.filter(reduce(operator.and_, q_objects)) # look for existing structure

				for sc in structuralCFilter:
					if structures == sc.contextualCandidates.all():
						structuralC = sc
						# print "Found existing Structure"
						break
				else:
					structuralC =  structuralCandidates.objects.create()
					structuralC.contextualCandidates.set(structures)	

				resultLinks.structuralCandidates.add(structuralC)

		# data['text'] = str(article.text.encode('utf-8', 'replace').lower())
		# except Exception as e:
		# 	print e
		# 	data['text'] = str('FAILS')
		returnData.append(data)
		# print "*"*10
	return returnData

# def getResults(html):
# 	soup = BeautifulSoup(html, 'lxml')
# 	for i in soup.find_all('a'):
# 		print i.get('href')
# 	# return []

# 	all_results = []

# 	for link in soup.find_all('a'):
# 		href = link.get('href')
# 		# if '/url?q=' in href and 'webcache' not in href:
# 			# href = href.replace('/url?q=', '')
# 		all_results.append(href)
# 	return parseResults(all_results)


def beginQuery(query, quantity = 30, force = False):
	start = datetime.now()

	query = query.replace('_','%20')
	breakdown = 50

	if breakdown > quantity:
		breakdown = quantity

	data_to_be_written = []
	for i in range(0, int(quantity), breakdown):
		if i == 0:
			url = 'https://www.google.com/search?q={0}&num={1}'.format(query, breakdown)
		else:
			url = 'https://www.google.com/search?q={0}&num={1}&start={2}'.format(query, breakdown, i)

		# driver = webdriver.Chrome(os.getcwd() + '/chromedriver')
		# driver.set_window_size(1,1)

		driver = webdriver.Chrome(os.getcwd() + '/chromedriver')
		driver.get(url)
		all_results = []

		# soup = BeautifulSoup(requests.get(url).text, 'lxml')

		# for link in soup.find_all('a'):
		# 	href = link.get('href')
		# 	if '/url?q=' in href and 'webcache' not in href:
		# 		href = href.replace('/url?q=', '')
		# 		href = href[:href.index('&sa')]
		# 		print href
		# 		all_results.append(href)

		for result in driver.find_elements_by_css_selector('.rc'):
			all_results.append(result.find_element_by_css_selector('a').get_attribute('href'))

		driver.close()

		for i in parseResults(all_results, force):
			data_to_be_written.append(i)
		

	print "Time Taken to get results [Cached/new] {0} minutes".format((datetime.now() - start).seconds/60)
	return data_to_be_written
