from __future__ import unicode_literals

from django.db import models

features = (
	('0','title'),
	('1','content'),
	)

structural_tags = (
	('0','title'),
	('1','document'),
	('2','content'),
	('3','reference'),
	)

class link(models.Model):
	url = models.TextField(blank = True)
	text = models.TextField(blank = True)
	keywords = models.TextField(blank = True)
	structuralCandidates = models.ManyToManyField('structuralCandidates')
	# wordCandidates = models.ManyToManyField('wordCandidate')
	# contextualCandidates = models.ManyToManyField('contextualCandidates')
	# structuralCandidates = models.ManyToManyField('structuralCandidates')

class wordCandidate(models.Model):
	text = models.TextField()
	feature = models.TextField()

class contextualCandidates(models.Model):
	# order = models.IntegerField(default = 0)
	feature = models.CharField(max_length = 20, choices=features)
	wordCandidates = models.ManyToManyField('wordCandidate')

class structuralCandidates(models.Model):
	tag = models.CharField(max_length = 2, choices = structural_tags, default = "2")
	# order = models.IntegerField(default = 0)

	contextualCandidates = models.ManyToManyField('contextualCandidates')