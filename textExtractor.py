#!/usr/bin/env python

###############################################
### COMP 598 : Project #1                   ###
### ---------------------					###
### Authors:                                ###
###  + Nicolas Angelard-Gontier - 260532513 ###
###  + Genevieve Fried - 260564432          ###
###  + Charlie Bloomfield - 260520615       ###
###############################################
import requests, json

"""
@params url: list of urls to grab data from
types: text, title, html, author,  discussion
"""
def diffbot_api(request, token, url):

	params= {'token':token, 'url' : url, 'fields': 'sentiment,links'}
	json_r = requests.get(request, params=params).json()
	if 'objects' in json_r:
		objs = json_r['objects']
		json_a = objs[0]

		title = json_a['title']
		text = json_a['text']
		sentiment = json_a['sentiment']
		links = json_a['links']

		num_of_links = len(links)
		return title, text, sentiment, num_of_links
	else:
		raise KeyError("no objects in the returned API call for: %s" % url)
