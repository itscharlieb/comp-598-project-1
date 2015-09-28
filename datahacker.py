#!/usr/bin/env python

###############################################
### COMP 598 : Project #1                   ###
### ---------------------					###
### Authors:                                ###
###  + Nicolas Angelard-Gontier - 260532513 ###
###  + Genevieve Fried - #########          ###
###  + Charlie Bloomfield - 260520615       ###
###############################################

"""
This file is responible for:
    - extracting features from the data we downloaded
    - creating a CSV file with all the data examples and features
"""

import csv
import datetime
from urlhacker import parseUrl


#necessary attributes to consider an item as a valid story
requiredStoryAttributes = [
    'url',
    'id',
    'title',
    'type',
    'by',
    'time',
    'descendants',
    'score'
]


"""
@param list of hacker-news items
@return list of hacker-news valid stories

Validity is determined by testing the item for containing a set of features.
"""
def filterStories(items):
    return [story for story in items if all(map(lambda attribute: attribute in story, requiredStoryAttributes))]

def weekday(time):
    return False

"""
@param unixtime object (@see https://en.wikipedia.org/wiki/Unix_time)
"""
def parseTime(unixTime):
    time = datetime.datetime.fromtimestamp(int(unixTime))
    day = time.strftime("%A") #returns the day of week of the given datetime

    isMon = 1 if day == 'Monday' else 0
    isTue = 1 if day == 'Tuesday' else 0
    isWed = 1 if day == 'Wednesday' else 0
    isThu = 1 if day == 'Thursday' else 0
    isFri = 1 if day == 'Friday' else 0
    isSat = 1 if day == 'Saturday' else 0
    isSun = 1 if day == 'Sunday' else 0

    return [
        time.year,
        time.month,
        time.day,
        time.hour,
        isMon,
        isTue,
        isWed,
        isThu,
        isFri,
        isSat,
        isSun
    ]


"""
"""
def parseYear(unixTime):
    return datetime.datetime.fromtimestamp(int(unixTime)).year


"""
"""
def authorFeatures(author):
    return [
        author['karma'],
        len(author['submitted']) if 'submitted' in author else 0,
        parseYear(author['created'])
    ]


"""
"""
def storyFeatures(story):
    features = [
        story['url'],
        story['descendants']
    ]
    features.extend(parseTime(story['time'])) #relevant time data
    return features


""" ==> TODO <==
Grabs features for a given story (in json format)
@param story - the dictionary object that represents a story.
@param users - dictionary of users
@return - an array of features for the given story.
"""
def grabFeatures(story, users):
    author = story['by']
    if(author not in users):
        raise ValueError("Could not find information on author of the story.")

    features = []
    features.extend(storyFeatures(story))
    features.extend(authorFeatures(users[author]))
    #features.extend(parseUrl(story))
    return features


""" ==> TODO <==
Goes through the 100,000 items, and grab features for each of them.
@return - a 2D array with line = array of feature values for 1 story.
example of features: [
    [url, f1, f2, ..., fm], <-- title line
    [&&&, ###, ###, ..., ###], <-- feature set for story #1
    [&&&, ###, ###, ..., ###], <-- feature set for story #2
    ...,
    [&&&, ###, ###, ..., ###] <-- feature set for story #n
]
"""
def extractFeatures(items):
    features = [['url', 'feature1', 'feature2']]
    for story in filterStories(items):
        try:
            storyFeatures = grabFeatures(story)
        except ValueError as e:
            print e
        
    features.append(storyFeatures)
    return features


"""
Create a csv file with given data
@param data - a 2D array returned by the extractFeatures() function.
"""
def createFile(data):
    with open('./data/stories.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile)
        for row in data:
            writer.writerow(row)


#createFile(extractFeatures())


