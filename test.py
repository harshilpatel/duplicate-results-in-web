# from __future__ import division
# import os, requests, sys 
# import django
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "beproject.settings")
# django.setup()

# import pdb, os, string
# import selenium, requests
# from app.models import *
# from app.parse2 import *
# import nltk
# from nltk.corpus import stopwords
# from nltk.stem.porter import *
# from nltk.stem.snowball import *
# from pattern.en import parse


# stop = list(set(stopwords.words('english')))
# stemmer = PorterStemmer()
# # stemmer2 = SnowballStemmer()
# def analyseSource(query = "", url = ""):

# 	if query == "":
# 		all = webSearch.objects.all()
# 		print [str(i) + " : " + a.queryText for i,a in enumerate(all)]
# 		query = all[int(raw_input())].queryText
# 		print query

# 	search = webSearch.objects.get(queryText = query)
# 	if url == "":
# 		url = search.results.all()[0].url
# 		print url
	
# 	all_results = []
# 	for r in search.results.all():
# 		i = [r.url, r.text, r.keywords.split(), r.title]
# 		all_results.append({
# 			'url' : i[0],
# 			'text' : i[1],
# 			'keywords' : i[2],
# 			'title' : i[3],
# 			'sentences' : [],
# 			'words' : [],
# 		})
	
# 	# converting object to dic data structures
# 	# for i in all_results:
# 	# 	i = {
# 	# 		'url' : i[0],
# 	# 		'text' : i[1],
# 	# 		'keywords' : i[2],
# 	# 		'title' : i[3],
# 	# 		'sentences' : [],
# 	# 		'words' : [],
# 	# 	}

# 	data = {
# 		'search' : query,
# 		'url' : url,
# 		'similar' : [],
# 		'related' : [],
# 		'duplicates' : [],
# 		'sub' : [],
# 		'super' : [],
# 	}

# 	for i in all_results:
# 		i['sentences'] = []
# 		i['words'] = []
# 		for sent in nltk.sent_tokenize(i.get('text')):
# 			sentence = []
# 			for word in nltk.word_tokenize(sent):
# 				word = word.lower().strip()
# 				word = stemmer.stem(word)
# 				if word not in stop and len(word) > 2:
# 					i['words'].append(word)
# 					sentence.append(word)
# 			sentence.sort()
# 			# print sentence
# 			i['sentences'].append(" ".join(sentence))
# 		i['words'].sort()

# 	source = {}

# 	for i in all_results:
# 		if i.get('url') == url:
# 			source = i
# 			all_results.remove(i)
# 			break
	
# 	frequent_words = set([])
# 	for i in all_results:
# 		total = len(i.get('words'))
# 		# source_words = [{i: 0}for i in source.get('words')]
# 		for word in set(i.get('words')):
# 			count = i['words'].count(word)
# 			if word in source.get('words'): frequent_words.add(word)
	
# 	for i in frequent_words:
# 		print i
	
# 	for i in all_results:
# 		for sent in i.get('sentences'):
# 			if sent in source.get('sentences'): print sent

# 	return data


# # analyseSource()

# def sample():
# 	if query == "":
# 		all = webSearch.objects.all()
# 		print [str(i) + " : " + a.queryText for i,a in enumerate(all)]
# 		query = all[int(raw_input())].queryText
# 		print query

# 	search = webSearch.objects.get(queryText = query)

# 	text = search.first().text

# 	text = parse(text)
# 	print text

# sample()