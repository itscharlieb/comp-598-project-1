#!/usr/bin/env python

###############################################
### COMP 598 : Project #1                   ###
### ---------------------					###
### Authors:                                ###
###  + Nicolas Angelard-Gontier - 260532513 ###
###  + Genevieve Fried - 260564432          ###
###  + Charlie Bloomfield - 260520615       ###
###############################################

"""
This class parses URL to grab some features about a website.
"""

from alchemyapi.alchemyapi import AlchemyAPI
import re, pprint, urllib
from nltk import word_tokenize
from bs4 import BeautifulSoup


#Alchemy API key
#Access to:
#	1,000 daily transactions
#	Technical email support
#	All of our text and image analysis APIs
APIKEY = "http://www.slate.com/articles/arts/culturebox/2015/09/banned_books_week_no_one_bans_books_anymore_and_censorship_of_books_is_incredibly.single.html"
# Create the AlchemyAPI Object
alchemyapi = AlchemyAPI()


"""
Retrieve features according to a given URL by using the AlchemyAPI.
@param url - the url to be parsed.
@return stats of given url as a dictionary
{
    text_length: int
    title_length: int
    numOutgoingUrls: int
    numKeywords: int
## TODO? ##
    numKeywordRepeatsInDoc: int
    numKeywordRepeatsInTitles: int
    semanticRelevance: int
    numImages: int
    numVideos: int
}
"""
def parseUrl(url):

    print('Processing url: ', url)

    text = ""
    title = ""
    links = 0
    keywords = []
    
    ## Get keywords (with relevance > 0.8) and title in 1 API call
    response = alchemyapi.combined('url', url, {'extract':'keyword,title'})
    if response['status'] == 'OK':
        #print response
        title = response['title'].encode('utf-8')
        for kw in response['keywords']:
            if kw['relevance'] > 0.8 :
                keywords.append(kw['text'].encode('utf-8'))
    else:
        print('Error in combined call: ', response['statusInfo'])
    
    ## Get the text of the article (include links)
    response = alchemyapi.text('url', url, {'extractLinks':1})
    if response['status'] == 'OK':
        #print response
        text = response['text'].encode('utf-8')
        links = text.count("<a href=")
    else:
        print('Error in text extraction call: ', response['statusInfo'])

    features = {
        'text_length': len(text.split()),
        'title_length': len(title.split()),
        'numOutgoingUrls': links,
        'numKeywords': len(keywords)
    }

    return features
"""
Extract html from our stories on the internet in order to perform feature analysis
@param: url of the article online 
"""



#print parseUrl('http://www.racecar-engineering.com/cars/porsche-919/')

