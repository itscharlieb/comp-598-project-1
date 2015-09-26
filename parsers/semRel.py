import logging
from gensim import corpora, models, similarities
from collections import defaultdict
from pprint import pprint 


"""
- tokenize each title, remove words that appear only once
- lemmatize words in title
- convert tokenized documents to vectors
- perform some sort of indexing algorithm, lsi or tdidf
"""

class Tokenize:

	def __init__(self, URL, article_dictionary):
		self.URL = URL
		self.ad = article_dictionary
	
	def createDocuments(self):
		ad = self.ad

		for 




	def basicParse(self, document):
		#remove common words and tokenize
		stoplist = set('for a of the and to in'.split())
		texts = [[word for word in document.lower().split() if word not in stoplist] for document in documents]

		#remove words that appear only once
		for text in texts:
			for token in text:
				frequency[token] += 1

		texts = [[token for token in text if frequency[token] > 1] for text in texts]




