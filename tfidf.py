from gensim import corpora, models
 
"""
returns a list of articles that has common words removed and is tokenized; 
@param documents: list of titles
"""
def basicParse(urls, documents):
	url_title = {}
	#remove common words and tokenize
	stoplist = set('for a of the and to in'.split())
	texts = [[word for word in document.lower().split() if word not in stoplist] for document in documents]
	url_title = dict(zip(urls, texts))
	
	#returns dictionary of urls: parsed titles of that url
	return url_title

"""
the function doc2bow counts the number of occurences of each distinct word in a string
in a document (an array of strings which could range from sentences to entire corpuses). 
Here we're creating a sparse vector of number of times the distinct words in data appear in 
parsedDoc, our document of strings defining a certain type of data (e.g. title) in our articles
from hackernews
@params title: single title
@params parsedDocument: documents that have been parsed by basicParse
"""

def doc2vec(parsedUrlDocuments):
	doc2vec_dict = {}
	pd = []
	for k,v in parsedUrlDocuments.iteritems():
		pd.append(v)

	dictionary = corpora.Dictionary(pd)
	for url, title in parsedUrlDocuments.iteritems():
		sp = " "
		title = sp.join(title)
		doc_bow = dictionary.doc2bow(title.lower().split())			# bag of words vector
		doc2vec_dict[url] = doc_bow
	
	return doc2vec_dict

"""
returns a list of tf-idf weights for each of the words in the title as they're represented in bow
@params doc_bow: bag of word vector for specific title
@params documents: list of titles to train our model
"""
def tfidf(doc2vec_dict, bp):	
	texts = []
	for k,v in bp.iteritems():
		texts.append(v)
	tfidf_weights_dict = {}
	dictionary = corpora.Dictionary(texts)
	corpus = [dictionary.doc2bow(text) for text in texts]
	corpus_tfidf = models.TfidfModel(corpus)	##initializing a model with docum
	
	for url,doc_bow in doc2vec_dict.iteritems():
		tfidf_weight = corpus_tfidf[doc_bow]
		tfidf_weights_dict[url] = tfidf_weight
	return tfidf_weights_dict


"""
@params tfidf_weight: pass in list of tuples of (id,tf-idf weights) from tfidf function above
"""
def take_min(tfidf_weight):
	min_tfidf = tfidf_weight[0][1]
	for tup in tfidf_weight:
		if tup[1] < min_tfidf:
			min_tfidf = tup[1]
	return min_tfidf

def take_max(tfidf_weight):
	max_tfidf = tfidf_weight[0][1]
	for tup in tfidf_weight:
		if tup[1] > max_tfidf:
			max_tfidf = tup[1]
	return max_tfidf

def take_avg(tfidf_weight):
	avg_tfidf = 0.0
	for tup in tfidf_weight:
		avg_tfidf = avg_tfidf + tup[1]
	avg_tfidf = avg_tfidf/len(tfidf_weight)
	return avg_tfidf
