###############################################
### COMP 598 : Project #1                   ###
### ---------------------					###
### Authors:                                ###
###  + Nicolas Angelard-Gontier - 260532513 ###
###  + Genevieve Fried - #########          ###
###  + Charlie Bloomfield - 260520615       ###
###############################################

import csv
import numpy as np
import random

"""
Read the data from a CSV file and put it all in an array.
Assume a title line at the begining of the file.
@param path - the path to the file to read.
@return - an array of tuples of the form (url, timedelta, array of features, array of target).
example of data: [
    (url1, timedelta1, [1,2,3,4,5], [6]),
    (url2, timedelta2, [2,1,4,4,6], [3]),
    (url3, timedelta3, [4,2,3,5,5], [5])
]
"""
def readData(path):
    data = []
    num_features = 0
    with open(path, 'rb') as datafile:
        reader = csv.reader(datafile)
        example = 0
        for row in reader:      # go through each line:
            if example == 0:    # first line assumed to be title line,
                num_features = len(row) #so get the number of features.
            elif example > 0:   # for all other lines, grab the data.

                if len(row) != num_features: # check that nuber of features is correct
                    print "ERROR: number of features for this row is not %d" % num_features
                    print row
                    continue

                url = row[0]                                    # URL is at the 1st column.
                timedelta = float(row[1])                       # time delta is at the 2nd column.
                features = map(float,row[2:num_features-1])     # features are from 3rd column to 60th column.
                target = [float(row[num_features-1])]           # target feature is at the 61st column.

                data.append((url, timedelta, features, target)) # add the tuple for this example.

            example=example+1 # increment example counter

    print "length of data: %d" % len(data)
    return data


"""
Partitions data into p/100 of training data and 1-(p/100) testing data.
@param data - an array of tuples of the form (url, timedelta, array of features, array of target).
@param p - the percentage of the data that will be used to train our learner. (default is 50%).
@return - two 2D arrays of tuples of the form (url, timedelta, array of features, array of target).
    One array is for training, the other for testing.
"""
def partition(data, p = 0.5):
    training = []
    testing = []

    training_size = int(len(data) * p)
    # create an array of size 'training_size' with random indices from 1 to len(data)-1
    random_examples = random.sample(range(len(data)), training_size)
    for i in range(len(data)):
        if i in random_examples:
            training.append(data[i])
        else:
            testing.append(data[i])

    print "length of training: %d" % len(training)
    print "length of testing: %d" % len(testing)
    return training, testing


"""
Partitions data into p/100 of training data and 1-(p/100) testing data, r times.
@param data - an array of tuples of the form (url, timedelta, array of features, array of target).
@param p - the percentage of the data that will be used to train our learner. (default is 50%).
@param r - the number of time we split the data. (default is 10 times).
@returns - an array of arrays of the form: [training, testing],
           with training and testing being arrays of tuples of the form (url, timedelta, array of features, array of target).
example of partitions: [
    [
        [
            (url1, timedelta1, [1,2,3,4,5], [6]),
            (url2, timedelta2, [2,1,4,4,6], [3]),
            (url3, timedelta3, [4,2,3,5,5], [5])
        ],
        [
            (url4, timedelta4, [3,2,3,1,5], [2]),
            (url5, timedelta5, [2,1,6,6,1], [4])
        ]
    ],
    [
        ...
    ],
    ...
]
"""
def multiPartition(data, p = 0.5, r = 10):
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


"""
returns the set of weights that define the ols line estimate over the parameter data
data is a list of [feature, val] lists
"""
def ols(features, dependents):
    product1 = X.transpose() * X
    product2 = X.transpose() * Y
    return product1.getI() * product2
"""
    X = np.matrix(x)
    Y = np.matrix(y)

    print "X = "
    print X
    print ""
    print "Y = "
    print Y
    print ""

    # product1 = (X^t * X)^-1
    product1 = (X.transpose() * X)
    print "X^t * X ="
    print product1

    # product2 = (X^t * Y)
    product2 = X.transpose() * Y
    print "X^t * Y ="
    print product2

    W = product1.getI() * product2
    print "W ="
    print W
    print W.shape
"""

"""
returns the set of weights that define the gradient descent estimate over the parameter data
"""
def gradientDescent(features, dependents):
    pass

"""
returns the squared error of points over the function defined by weights
"""
def squaredError(weights, points):
    pass