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
requiredSoryAttributes = [
    'url',
    'id',
    'title',
    'type',
    'by',
    'time',
    'descendants'
    'score',
]

features = [
    'url',
    'title',
    'userKarma',
    'numComments'
    'year',
    'month',
    'hour',
    'isWeekday',
    'isWeekend',
    'score'
]


"""
@param list of hacker-news items
@return list of hacker-news valid stories

Validity is determined by testing the item for containing a set of features.
"""
def filterStories(items):
    return [story for story in items if all(map(lambda attribute: attribute in story, requiredStoryAttributes))]

def isWeekday(time):
    return False

"""
@param unixtime object (@see https://en.wikipedia.org/wiki/Unix_time)
"""
def parseTime(unixTime):
    time = datetime.datetime.fromtimestamp(int(unixTime))
    weekday = isWeekday(time)

    return [
        time.year,
        time.month,
        time.hour,
        weekday,
        (not weekday)
    ]

"""
"""
def parseYear(unixTime):
    return datetime.datetime.fromtimestamp(int(unixTime)).year


""" ==> TODO <==
Grabs features for a given story (in json format)
@param story - the dictionary object that represents a story.
@param users - dictionary of users
@return - an array of features for the given story.
"""
def grabFeatures(story, users):
    if(story['by'] not in users):
        raise Error("Could not find information on the user.")
    author = users[story['by']]

    features = []

    #story info
    features.append(story['url'])
    features.append(story['title'])
    features.append(story['descendants']) #number of comments

    #author info
    features.append(author['karma'])
    features.append(parseYear(author('created')))
    features.append( #number of stories added by author
        len(author['submitted']) if 'submitted' in author else 0
    )

    #url info
    urlFeatures = parseUrl(story)

    # add features to the array in the same order as in the CSV file.
    return features.extend(urlFeatures)


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
        except (StoryException):

        
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


createFile(extractFeatures())


