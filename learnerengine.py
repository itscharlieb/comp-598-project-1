###############################################
### COMP 598 : Project #1                   ###
### ---------------------					###
### Authors:                                ###
###  + Nicolas Angelard-Gontier - 260532513 ###
###  + Genevieve Fried - #########          ###
###  + Charlie Bloomfield - #########       ###
###############################################

import sys
import numpy as np
import random

"""
function with params: data, number of sets, percentage for training
returns: list (size=number of sets) of (training,test) tuples.
"""
def partition(data, training_percentage = 0.5):
    training = []
    test = []

    training_size = len(data) * training_percentage
    random_examples = random.sample(data, int(training_size))
    for i in range(len(data)):
        if i in random_examples:
            training.append(data[i])
        else:
            test.append(data[i])

    return training, test


"""
partitions data into r sets of size p partitions
"""
def multiParition(data, p = 0.5, r = 10):
	partitions = []
	for _ in range(r):
		partitions.append(partition(data, p))
	return partitions


"""
returns a training and error function pair on a partitioned set of data
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


