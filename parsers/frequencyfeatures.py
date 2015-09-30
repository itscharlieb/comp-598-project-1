#!/usr/bin/env python

###############################################
### COMP 598 : Project #1                   ###
### ---------------------					###
### Authors:                                ###
###  + Nicolas Angelard-Gontier - 260532513 ###
###  + Genevieve Fried - 260564432          ###
###  + Charlie Bloomfield - 260520615       ###
###############################################

from collections import defaultdict
"""
Features:
- frequency of an author amongst our articles
- frequency of a website (e.g. nytimes, youtube) occurring
"""
def author_Freq(listofauthors):
	aCount = defaultdict(int)
	aFreq={}
	total_count = len(listofauthors)
	for author in listofauthors:
		author.lower()		# lowercase (just in case)
		aCount[author] +=1.0 
	for k,v in aCount.iteritems():
		aFreq[k] = float(v/total_count)
	return aFreq

def website_Freq(listofurls):
	wCount = defaultdict(int)
	wFreq = {}
	total_count = len(listofurls)
	for url in listofurls:
		parse = url.split('.')
		for pou in range(len(parse)):
			if "www" in parse[pou]:
				wCount[parse[pou+1]] +=1.0
	for k,v in wCount.iteritems():
		wFreq[k] = (v/total_count)
	return wFreq


