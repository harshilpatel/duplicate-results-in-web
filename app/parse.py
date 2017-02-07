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

def parseResults(results):
	# print "Analysing %s articles" %str(len(results))
	returnData = []
	stop = set(stopwords.words('english'))
	stemmer = PorterStemmer()
	for i in results:
		# try:
		# if link.objects.filter(url = i).count() > 1:
		# 	# print link.objects.all().count()
		# 	print "Duplicates found, delete now"
		# 	return {}
		item = link.objects.filter(url = i)
		if item.count() == 1:
			item = item.first()
			# print "Link already exists"
			context = {'url' : item.url, 'text' : ''}
			for i in item.structuralCandidates.all():
				para = ''
				for j in i.contextualCandidates.all():
					para += ' '.join([k.text for k in j.wordCandidates.all()])
				if para:
					# para += '.'
					context['text'] += para + '. '
			# return context
			returnData.append(context)
			print "Found - {0}".format(context.get('url'))
			continue
		elif item.count() > 1:
			print "Skipping duplicate entrier. fix it"
			continue
		# except:
			# pass

		# print "Calculating NEW URL"
		print "New - {0}".format(i)
		data = {}
		if 'webcache' in i or (i.count('/') <= 3 and i[-1:] == '/'):
			# print "CachedGoogle link"
			continue
		article = Article(i)
		article.download()
		data['url'] = str('[' + i + ']')
		# try:

		article.parse()
		data['title'] = str('[' + article.title.encode('ascii', 'ignore') + ']')
		text = article.text.encode('ascii', 'ignore').lower()
		text = re.sub('&#?\w+;', fixup, text)

		structure = text.replace('\n\n','\n').split('\n')
		articleText = ''
		resultLink = link.objects.create(url = i)
		for count,para in enumerate(structure):

			text = para.split('.')
			paraText = ''
			# structuralC = structuralCandidates.objects.create(order = count)
			structures = []
			for sentence in text:
				tokens = nltk.word_tokenize(sentence)
				new_tokens = []

				# for review in tokens:
					# new_review = []
				for token in tokens: 
					new_token = regex.sub(u'', token)
					if not new_token == u'':
						new_tokens.append(new_token)
					
					# new_tokens.append(new_review)
				tagged = nltk.pos_tag(new_tokens)

				paraText += ' '.join([stemmer.stem(i[0]) for i in tagged if i[0] not in stop]) + '.'

				context = []
				for group in tagged:
					word, feature = group
					word = stemmer.stem(word)
					if word not in stop:
						# paraText += " " +  word
						# db connections
						wordC, created  = wordCandidate.objects.get_or_create(text = word, feature = feature)
						context.append(wordC)

				q_objects = []
				for c in context:
					q_objects.append(Q(wordCandidates = c))

				# print "CC {0}".format(len(q_objects))

				if len(q_objects) > 0:
					contextualCFilter = contextualCandidates.objects.filter(reduce(operator.and_, q_objects)) # look for matching sentence with same context
					# if contextualCFilter.count() > 0:
					for cc in contextualCFilter:
						if context == cc.wordCandidates.all():
							contextualC = cc
							print "Match found"
							break
					else:
						contextualC = contextualCandidates.objects.create()
						contextualC.wordCandidates.set(context)
					# else:
						# print "Possible duplicate contextual candidates in DB"

					# structuralC.contextualCandidates.add(contextualC)
					structures.append(contextualC)

			q_objects = []
			for s in structures:
				q_objects.append(Q(contextualCandidates = s))

			# print "SC {0}".format(len(q_objects))

			if len(q_objects) > 0:
				structuralCFilter = structuralCandidates.objects.filter(reduce(operator.and_, q_objects)) # look for existing structure

				# if structuralCFilter.count() > 0:
				for sc in structuralCFilter:
					if structures == sc.contextualCandidates.all():
						structuralC = sc
						print "Match Found"
						break
				else:
					structuralC =  structuralCandidates.objects.create()
					structuralC.contextualCandidates.set(structures)	

				# if structuralCFilter.count() == 0:
				# 	structuralC =  structuralCandidates.objects.create()
				# 	structuralC.contextualCandidates.set(structures)
				# elif structuralCFilter.count() == 1:
				# 	structuralC = structuralCFilter.first()
				# else:
				# 	print "Possible dupicates Structural candidates in DB"

				resultLink.structuralCandidates.add(structuralC)

				articleText += paraText


		data['text'] = articleText

		# data['text'] = str(article.text.encode('utf-8', 'replace').lower())
		# except Exception as e:
		# 	print e
		# 	data['text'] = str('FAILS')
		returnData.append(data)
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


def beginQuery(query, quantity = 30):
	start = datetime.now()


	query = query.replace('_','%20')
	breakdown = 50

	if breakdown > quantity:
		breakdown = quantity

	data_to_be_written = []
	for i in range(0, int(quantity), breakdown):
		# print i
		# headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

		if i == 0:
			url = 'https://www.google.com/search?q={0}&num={1}'.format(query, breakdown)
		else:
			url = 'https://www.google.com/search?q={0}&num={1}&start={2}'.format(query, breakdown, i)

		# r = requests.get(url, headers = headers)
		
		# if 'Our systems have detected unusual traffic from your computer network' in r.text:
			# print "Error"
		driver = webdriver.Chrome(os.getcwd() + '/chromedriver')
		# driver.set_window_size(1,1)
		driver.get(url)
		# text = driver.page_source
		all_results = []
		for result in driver.find_elements_by_css_selector('.rc'):
			all_results.append(result.find_element_by_css_selector('a').get_attribute('href'))

		driver.close()

		for i in parseResults(all_results):
			data_to_be_written.append(i)
		# print len(data_to_be_written)

	# f = open(query.replace('%20','_')+'.txt', 'w')
	# json.dump(data_to_be_written, f, indent = 4)
	# f.close()

	print "Time Taken to get results [Cached/new] {0} minutes".format((datetime.now() - start).seconds/60)
	return data_to_be_written

# start = datetime.now()

# query = sys.argv[1].replace('_','%20')
# quantity = int(sys.argv[2])

# beginQuery(query, quantity)

# print "Time Taken {0} minutes".format((datetime.now() - start).seconds/60)
