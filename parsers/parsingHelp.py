import logging, json
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

	# meta info = list of dictionaries
	# data (string) = meta info we're interested in e.g. url, title, author 
	def __init__(self, URL, metainfo, data):
		self.URL = URL
		self.fp = metainfo
		self.data = data

	def createDocuments(self):
		fp = self.fp
		items = self.metainfo
		data = self.data
		documents = []

		for dic in items:
			[documents.append(dic[data]) if data in dic.keys()]

		return documents

	def basicParse(self, documents):
		#remove common words and tokenize
		stoplist = set('for a of the and to in'.split())
		texts = [[word for word in document.lower().split() if word not in stoplist] for document in documents]

		#remove words that appear only once
		for text in texts:
			for token in text:
				frequency[token] += 1

		texts = [[token for token in text if frequency[token] > 1] for text in texts]

		return texts


	def doc2vec(self, data, parsedDoc):
		dictionary = corpora.Dictionary(parsedDoc)

		new_doc = data
		new_vec = dictionary.doc2bow(new_doc.lower().split())

		"""

		the function doc2bow counts the number of occurences of each distinct word in a string
		in a document (an array of strings which could range from sentences to entire corpuses). 
		Here we're creating a sparse vector of number of times the distinct words in data appear in 
		parsedDoc, our document of strings defining a certain type of data (e.g. title) in our articles
		from hackernews

		"""

		corpus = [dictionary.doc2bow(text) for text in texts]