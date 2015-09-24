###############################################
### COMP 598 : Project #1                   ###
### ---------------------					###
### Authors:                                ###
###  + Nicolas Angelard-Gontier - 260532513 ###
###  + Genevieve Fried - #########          ###
###  + Charlie Bloomfield - 260520615       ###
###############################################

import json
import requests
from collections import deque

items = open("./data/items", "a")
users = open("./data/users", "a")
topStories = open("./data/topStories", "a")

itemCache = {}
userCache = {}
# comments = open("./data/comments", "a")
# jobs     = open("./data/jobs", "a")
# pollopts = open("./data/pollopts", "a")
# polls    = open("./data/polls", "a")
# stories  = open("./data/stories", "a")
# users    = open("./data/users", "a")


def itemUri(id):
	"""
	@param id of a hacker-news item
	@returns uri that represents the item to be pulled
	"""
	return "https://hacker-news.firebaseio.com/v0/item/" + str(id) + ".json"


def userUri(id):
	"""
	@param id of hacker-news user
	@returns uri that represents the user to be pulled
	"""
	return "https://hacker-news.firebaseio.com/v0/user/" + id + ".json"


def recordItem(jsonItem):
	"""
	@param json item to be recorded
	stores the item in the appropriate text file
	"""
	topStories.write(str(jsonItem))


def recordUser(jsonUser):
	"""
	@param json item to be recorded
	stores the item in the appropriate text file
	"""
	users.write(str(jsonUser))


def getItem(id):
	"""
	@param id of item to be pulled from hacker-news
	@returns json item associated with id
	automatically stores the item in a file
	"""
	if not id in itemCache:
		jsonItem = requests.get(itemUri(id)).json()
		recordItem(jsonItem)
		itemCache[id] = jsonItem
	return itemCache[id]


def getUser(id):
	"""
	@param id of user to be pulled from hacker-news
	@returns json user associated with id
	automatically stores the user in a file
	"""
	if not id in userCache:
		jsonUser = requests.get(userUri(id)).json()
		recordUser(jsonUser)
		userCache[id] = jsonUser
	return userCache[id]


def recordStory(jsonItem):
	"""
	@param id of story item
	The data of interest in this search is hacker-news stories.
	Handle story finds all data relates to a story, including comments and user information,
	"""
	userId = jsonItem["by"]
	getUser(userId)

	if "kids" in jsonItem:
		commentIds = deque(jsonItem["kids"])

	#while comments is not empty
	while commentIds:
		commentId = commentIds.popleft()
		comment = getItem(commentId)
		if "kids" in comment:
			childCommentIds = comment["kids"]
			commentIds.extend(childCommentIds)
		if "by" in comment:
			getUser(comment["by"])


def main():
	topStories = requests.get("https://hacker-news.firebaseio.com/v0/topstories.json").json()
	for storyId in topStories:
		story = getItem(storyId)

		print ("Recording story with id {}".format(storyId))
		print (str(story))

		recordStory(story)


if __name__ == "__main__":
	main()