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

	params= {'token':diffbot_token, 'url' : url, 'fields': 'sentiment,links'}
	json_r = requests.get(request, params=params).json()
	objs = json_r['objects']
	json_r = objs[0]

	title = json_r['title']
	text = json_r['text']
	author = json_r['author']
	sentiment = json_r['sentiment']
	images = json_r['images']
	links = json_r['links']

	num_of_im = len(images)
	num_of_link = len(links)

	return title, text, author, sentiment, num_of_im, num_of_link
