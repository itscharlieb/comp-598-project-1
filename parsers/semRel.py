import logging
from gensim import corpora, models, similarities


"""
- tokenize each title, remove words that appear only once
- lemmatize words in title
- convert tokenized documents to vectors
- perform some sort of indexing algorithm, lsi or tdidf
"""