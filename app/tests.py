from django.test import TestCase
from app.models import webSearch, WebResource
from app.parse2 import get_results
# Create your tests here.


class apptestCases(TestCase):

	def makeResults(self):
		sample = ['protest india', 'gandhi murder', 'isis mumbai']
		for q in sample:
			print len(get_results(q, 50))

	def testName(self):
		self.makeResults()
		