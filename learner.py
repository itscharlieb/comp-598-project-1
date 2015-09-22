###############################################
### COMP 598 : Project #1                   ###
### ---------------------					###
### Authors:                                ###
###  + Nicolas Angelard-Gontier - 260532513 ###
###  + Genevieve Fried - #########          ###
###  + Charlie Bloomfield - 260520615       ###
###############################################

import csv, random
import numpy as np

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

    return training, testing


"""
Partitions data into p/100 of training data and 1-(p/100) testing data, r times.
@param data - an array of tuples of the form (url, timedelta, array of features, array of target).
@param p - the percentage of the data that will be used to train our learner. (default is 50%).
@param r - the number of time we split the data. (default is 10 times).
@return - an array of arrays of the form: [training, testing],
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
Train some given learner with some given data.
@param trainFunc - the learner that we want to use.
@param trainingData - the data that we want to train on, of the form: [(URL, timedelta, [1,2,3], [4]), (...), ...]
@return - whatever the learner returns.
"""
def train(trainFunc, trainingData):
	return trainFunc(trainingData)

"""
"""
def multiTrain(trainFunc, partitions):
    results = []
    for p in partitions:
        trainingData = p[0]
        testingData = p[1]
        results.append(train(trainFunc, trainingData))
    return results


"""
Calculate the Ordinary Least Squares coefficients for some features and their targets.
@param trainingData - the data that we want to train on, of the form: [(URL, timedelta, [1,2,3], [4]), (...), ...]
@return - the coefficient matrix corresponding to the OLS line estimate.
"""

def generateMatrixes(trainingData):
    features = []
    targets = []
    for example in trainingData:
        features.append(example[2]) #features are the 3rd element of an example tuple.
        targets.append(example[3]) #the target is the 4th element of an example tuple.

    X = np.matrix(features, dtype = np.float64)
    Y = np.matrix(targets, dtype = np.float64)
    
    return X,Y

def ols(trainingData):

    X,Y = generateMatrixes(trainingData)

    # product1 = (X^t * X)^-1
    product1 = (X.transpose() * X)
    # product2 = (X^t * Y)
    product2 = X.transpose() * Y

    W = product1.getI() * product2
    return W

"""
returns the set of weights that define the gradient descent estimate over the parameter data
"""

def ErrW(wVec, xVec, yVec):

    p1 = xVec.transpose() * xVec
    p2 = p1 * wVec.transpose()
    p3 = xVec.transpose() * yVec
    p4 = p2-p3
    return np.multiply(2.0, p4)

    #TOD0: Look into wolfe conditions or robin monroe's sequence for alpha
def gradientDescent(trainingData):

    ## constant values
    alpha = random.random()  #to be replaced later with a more sophisticated alg
    epsilon = 0.0001    
    X,Y = generateMatrixes(trainingData)
    lenM = X.shape[1]

   # initial construction of gradient descent alg
    tmp = [random.random() for x in range(lenM)]
    wCrt = np.matrix(tmp)
    aErr = np.multiply(alpha, ErrW(wCrt, X, Y))
    wNext = wCrt - aErr

    ## gradient descent
    while( np.linalg.norm(wNext - wCrt) > epsilon):
        print np.linalg.norm(wNext - wCrt)
        wCrt = wNext
        aErr = np.multiply(alpha, ErrW(wCrt, X, Y))
        wNext = wCrt - aErr
        

        if np.linalg.norm(wCrt) == np.linalg.norm(wNext):
            return wNext
    return wNext    

"""
returns the squared error of points over the function defined by weights
"""
def squaredError(weights, points):
    pass