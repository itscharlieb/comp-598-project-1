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
from urlhacker import parseUrl

""" ==> TODO <==
Grabs features for a given story (in json format)
@param story - the json object that represents a story.
@return - an array of features for the given story.
"""
def grabFeatures(story):
    features = []
    #1: grab from json object
    #2: call parseUrl() to get other features
    # add features to the array in the same order as in the CSV file.
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
def extractFeatures():
    features = [['url', 'feature1', 'feature2']]
    #for each item in items100000.json:
    #    if it's a story:
    #        f = grabFeatures(story)
    #        features.append(f)
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


