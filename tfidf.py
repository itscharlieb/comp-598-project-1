import logging, json
from gensim import corpora, models, similarities
from collections import defaultdict
from pprint import pprint 



 
"""
returns a list of articles that has common words removed and is tokenized; 
@param documents: list of titles
"""
def basicParse(documents):
	#remove common words and tokenize
	stoplist = set('for a of the and to in'.split())
	texts = [[word for word in document.lower().split() if word not in stoplist] for document in documents]

	return texts

"""

	the function doc2bow counts the number of occurences of each distinct word in a string
	in a document (an array of strings which could range from sentences to entire corpuses). 
	Here we're creating a sparse vector of number of times the distinct words in data appear in 
	parsedDoc, our document of strings defining a certain type of data (e.g. title) in our articles
	from hackernews

@params title: single title
@params parsedDocument: documents that have been parsed by basicParse
"""

def doc2vec(title, parsedDocuments):
	dictionary = corpora.Dictionary(parsedDocument)
	doc_bow = dictionary.doc2bow(title.lower().split())			# bag of words vector

	return doc_bow

"""
returns a list of tf-idf weights for each of the words in the title as they're represented in bow
@params doc_bow: bag of word vector for specific title
@params documents: list of titles to train our model
"""
def tfidf(doc_bow, documents):	
	#corpus = listoftitles
	corpus_tfidf = models.TfidfModel(documents)	##initializing a model with docum
	tfidf_weight = corpus_tfidf[title]
	return tfidf_weight


"""
@params tfidf_weight: pass in list of tuples of (id,tf-idf weights) from tfidf function above
"""
def take_min(tfidf_weight):
	for 

def take_max(tfidf_weight):

def take_avg(tfidf_weight)