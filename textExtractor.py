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
# api arguments
diffbot_token = "b78400cc0f6795ded5fa3d980d1348c6"
diffbot_tokenN = "09e512545e45166138161870d3f9a541"
diffbot_tokenCB = ""

request = "http://api.diffbot.com/v3/article"


@params url: list of urls to grab data from
types: text, title, html, author,  discussion
"""
def diffbot_api(request, token, url):

	params= {'token':token, 'url' : url, 'fields': 'sentiment,links'}
	json_r = requests.get(request, params=params).json()
	if json_r['objects']:
		objs = json_r['objects']
		json_a = objs[0]

		title = json_a['title']
		text = json_a['text']
		sentiment = json_a['sentiment']
		links = json_a['links']

		num_of_links = len(links)
		return title, text, sentiment, num_of_links
	else: 
		return 0,0,0,0


