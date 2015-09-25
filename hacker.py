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
import threading
import time
from collections import deque

class ThreadsafeIterator(object):
    def __init__(self, it):
        self.lock = threading.Lock()
        self.it = it.__iter__()

    def __iter__(self):
    	return self

    def next(self):
        self.lock.acquire()
        try:
            return self.it.next()
        finally:
            self.lock.release()


class ThreadsafeFileWriter(object):
	def __init__(self, f):
		self.lock = threading.Lock()
		self.f = f

	def write(self, data):
		self.lock.acquire()
		try:
			self.f.write(str(data))
		finally:
			self.lock.release()


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


def recordItem(jsonItem, itemFile):
	"""
	@param json item to be recorded
	stores the item in the appropriate text file
	"""
	itemFile.write(str(jsonItem))


def recordUser(jsonUser, userFile):
	"""
	@param json item to be recorded
	stores the item in the appropriate text file
	"""
	userFile.write(str(jsonUser))


def getItem(id, itemFile):
	"""
	@param id of item to be pulled from hacker-news
	@returns dict associated with id
	automatically stores the item in a file
	"""
	if not id in itemCache:
		jsonItem = requests.get(itemUri(id)).json()
		recordItem(jsonItem, itemFile)
		itemCache[id] = jsonItem
	return itemCache[id]


def getUser(id, userFile):
	"""
	@param id of user to be pulled from hacker-news
	@returns dict associated with id
	automatically stores the user in a file
	"""
	if not id in userCache:
		jsonUser = requests.get(userUri(id)).json()
		recordUser(jsonUser, userFile)
		userCache[id] = jsonUser
	return userCache[id]


def recordStory(jsonItem, itemFile, userFile):
	"""
	@param id of story item
	The data of interest in this search is hacker-news stories.
	Handle story finds all data relates to a story, including comments and user information,
	"""
	userId = jsonItem["by"]
	getUser(userId, userFile)

	if "kids" in jsonItem:
		commentIds = deque(jsonItem["kids"])

	#while comments is not empty
	while commentIds:
		commentId = commentIds.popleft()
		comment = getItem(commentId, itemFile)
		if "kids" in comment:
			childCommentIds = comment["kids"]
			commentIds.extend(childCommentIds)
		if "by" in comment:
			getUser(comment["by"], userFile)


def searchItems(itr, itemFile, userFile):
	itemsRecorded = 0
	storiesRecorded = 0
	try:
		while(True):
			itemId = itr.next()
			item = getItem(itemId, itemFile)
			itemsRecorded += 1

			if item["type"] == "story":
				recordStory(item, itemFile, userFile)
				storiesRecorded += 1 

	except StopIteration:
		print ("{} stories were recorded.".format(storiesRecorded))


itemCache = {}
userCache = {}

reportFile = open("./data/report.txt", "a")
reportFile.write("Testing optimal number of threads for downloading data from hacker-news.")
reportFile.write("The first 24 items posted on hacker-news (ids 1 thru 24) will be processed.")
reportFile.write("If an item represents a story, all items related to that story will also be downloaded.")
reportFile.write("Execution will be tested serially, and with 1, 2, 4 ... 256 threads.")
reportFile.write("========================================================================\n\n")

start = time.time()
itemsSerial = open("./data/itemsSerial.json", "a")
usersSerial = open("./data/usersSerial.json", "a")
serialItr = ThreadsafeIterator([x for x in range(1, 25)])
searchItems(serialItr, itemsSerial, usersSerial)
stop = time.time()

reportString = "[Serial exexcution time] {}".format(stop - start)
print(reportString)
reportFile.write(reportString)

itemCache.clear()
userCache.clear()

for numThreads in [2**x for x in range(1, 9)]:
	start = time.time()

	itemFileName = "./data/itemsParallel" + str(numThreads) + ".json"
	userFileName = "./data/usersParallel" + str(numThreads) + ".json"

	parallelItr = ThreadsafeIterator(range(1, 25))
	itemsParallel = ThreadsafeFileWriter(open(itemFileName, "a"))
	usersParallel = ThreadsafeFileWriter(open(userFileName, "a"))

	threads = []
	for i in range(numThreads):
		thread = threading.Thread(target=searchItems, args=(parallelItr, itemsParallel, usersParallel))
		threads.append(thread)
		thread.start()

	while threads:
		thread = threads.pop()
		thread.join()

	stop = time.time()

	itemCache.clear()
	userCache.clear()

	reportString = "[Parallel execution time with {} threads] {}".format(numThreads, (stop - start))
	print (reportString)
	reportFile.write(reportString)




