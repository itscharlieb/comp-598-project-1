###############################################
### COMP 598 : Project #1                   ###
### ---------------------					###
### Authors:                                ###
###  + Nicolas Angelard-Gontier - 260532513 ###
###  + Genevieve Fried - #########          ###
###  + Charlie Bloomfield - 260520615       ###
###############################################

import sys
import numpy as np
import random

"""
Split data into 2.
@param data - an array of tuples of the form (array of features, array of target).
@param p - the percentage of the data that will be used to train our learner.
@returns - two 2D arrays of tuples of the form (array of features, array of target).
    One array is for training, the other for testing.
"""
def partition(data, p = 0.5):
    training = [] # array of tuples of the form (array of features, array of target).
    test = [] # array of tuples of the form (array of features, array of target).

    training_size = len(data) * p
    # create an array of size 'training_size' with random indices from 1 to len(data)-1
    random_examples = random.sample(range(len(data)), int(training_size))
    for i in range(len(data)):
        if i in random_examples:
            training.append(data[i])
        else:
            test.append(data[i])

    return training, test


"""
Partitions data into p/100 of training, r times.
@param data - an array of tuples of the form (array of features, array of target).
@param p - the percentage of the data that will be used to train our learner.
@param r - the number of time we split the data.
@returns - an array of arrays of the form: [training, testing].
    With training and testing being arrays of tuples of the form (array of features, array of target).
"""
def multiParition(data, p = 0.5, r = 10):
	partitions = []
	for _ in range(r):
        training, testing = partition(data, p)
		partitions.append([training, testing])
	return partitions


"""
Returns a training and error function pair on a partitioned set of data
"""
def train(trainFunc, trainingData, testData):
	weights = trainFunc(trainingData[0], trainingData[1])

	#errorFunc may need different parameters. Specifically, it probably needs a function
	#and not just a set of weights.
	#error = errorFunc(weights, testData)
	return weights


"""
"""
def multiTrain(trainFunc, partitions):
	results = []
	for trainingData, testData in partitions:
		results.append(train(trainFunc, trainingData, testData))
	return results


