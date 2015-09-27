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
                # skip features 6,19-20,22-23,25-26,28-29,31-37,51-52,54-55.
                features = features[:6]+features[7:19]+features[21:22]+features[24:25]+features[27:28]+features[30:31]+features[38:51]+features[53:54]+features[56:]
                target = [float(row[num_features-1])]           # target feature is at the 61st column.

                data.append((url, timedelta, features, target)) # add the tuple for this example.

            example=example+1 # increment example counter

    random.shuffle(data)
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
Partitions the data into k subsets of size len(data)/k.
@param data - an array of tuples of the form (url, timedelta, array of features, array of target).
@param k - the number of subsets we want.
@return - an array of data subsets with subsets of the form [(url, timedelta, array of features, array of target), (...), ...].
example of partitions: [
    [
        (url1, timedelta1, [1,2,3,4,5], [6]),
        (url2, timedelta2, [2,1,4,4,6], [3]),
        ...,
        (urlk, timedeltak, [4,2,3,5,5], [5])
    ],
    [
        ...
    ],
    ...
]
"""
def multiPartition(data, k):
    print "Dividing the data into %d subsets..." % k

    size = len(data) / k # size is the subset size.

    # let's go step by step with this one-liner:
    # we return an array: return [...].
    # this array is made of subsets of the data from i to i+size: data[i:i+size].
    # so we have: return [[data[i],data[i+1],...,data[i+size-1]], [...], ...].
    # i is going to be an index from 0 to len(data), but by jumping over k values,
    #  which leaves space for our 'size' data items (at i,i+1,...,i+size-1) in one subset.
    partitions = [data[i:i+size] for i in range(0, len(data), size)]

    
    # because len(data) / k might not be an perfect integer, we may have fewer examples: len(data)modulo(k).
    if len(data)%k != 0:
        print "Warning, %d is not a multiple of %d. Skipping %d elements." % (len(data), k, len(data)%k)
        return partitions[:-1]
    else:
        return partitions


"""
Calculates the average weigth for each feature given a set of weights.
@param weights - the set of different weights, of the form: [ [[w11],...,[w1size]], ..., [] ]
@return one set of weights (as a matrix): the average.
"""
def averageWeights(weights):
    # Create the average 2D array:
    average = []
    for _ in range(len(weights[0])): # for each feature in  a set of weights:
        average.append([]) # create an empty array.

    for w in weights: # go through each set of weights
        for feature_index in range(len(w)): # go through each feature weight:
            # append to average the new weight of the corresponding feature.
            average[feature_index].append(w[feature_index][0])
    # Now average looks like this: [
    #   [f1w1, f1w2, f1w3, ..., f1wm], <-- different weights (m of them) of feature 1
    #   [f2w1, f2w2, f2w3, ..., f2wm], <-- different weights (m of them) of feature 2
    #   ...
    #   [fnw1, fnw2, fnw3, ..., fnwm], <-- different weights (m of them) of feature n
    # ]
    #
    # We now want to average each array (a=[fw1,...,fwm]) for each feature.
    # We map to each element 'a' of 'average' a function: map(lambda a : ... , average)
    # This function returns an array with 1 element inside it: the average of all other elements.
    # The average of an array is calculated by 'reducing' all elements to their sum: reduce(lambda x,y: x+y, a)
    #  and dividing by the number of elements: reduce(lambda x,y: x+y, a) / len(a)
    W = map(lambda a : [reduce(lambda x,y: x+y, a)/len(a)], average)
    return np.matrix(W)

"""
Calculates the average of the squared errors we got by training multiple times the data.
@param errors - the array of squared errors for each training.
@return the average of the parameter array.
"""
def crossValidation(errors):
    # return the average of the array. See one-liner details in 'averageWeights()'
    return reduce(lambda x,y: x+y, errors) / len(errors)

"""
Train some given learner with some given data.
@param trainFunc - the learner that we want to use.
@param trainingData - the data that we want to train on, of the form: [(URL, timedelta, [1,2,3], [4]), (...), ...]
@return - whatever the learner returns.
"""
def train(trainFunc, trainingData):
	return trainFunc(trainingData)

"""
Train some given learner with different sets of trainingData & testingData.
@see: k-fold cross validation.
@param trainFunc - the learner that we want to use.
@param partitions - an array of data subsets with subsets of the form [(url, timedelta, array of features, array of target), (...), ...].
@return - an array of different sets of weights for each iteration of the learning.
example of weights: [
    [
        [w11],
        [w12],
        ...,
        [w1f],
    ],
    ...
]
"""
def multiTrain(trainFunc, partitions):

    """Custom flattening function for training array"""
    def customFlat(train):
        a = []
        for subset in train:
            for example in subset:
                a.append(example)
        return a

    weights = []
    errors = []
    print "Training %d times..." % len(partitions)
    for i in range(len(partitions)):    # for each subset of data:
        print "    %d / %d" % (i, len(partitions)-1)
        testingData = partitions[i]     # the testing data is one subset.
        trainingData = partitions[:i] + partitions[i+1:] # the training data is all the other subsets.
        trainingData = customFlat(trainingData)          # merge all subsets into one big training data.
        weights.append(train(trainFunc, trainingData).tolist()) # get the weights learned by this training data.
        errors.append(squaredError(weights[-1], testingData))   # get the error of those weights on the testing data.

    #return averageWeights(weights), crossValidation(errors)
    return None, crossValidation(errors)



"""
Generates the features (X) and target (Y) matrices.
@param trainingData - the data that we want to convert to matrices, of the form: [(URL, timedelta, [1,2,3], [4]), (...), ...]
@return - two matrices X and Y for the features and the targets respectively.
example of X: [     |    example of Y: [
    [1,2,3,4,5],    |        [6],
    [2,1,4,4,6],    |        [3],
    [4,2,3,5,5]     |        [5]
]                   |    ]
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

"""
Calculate the Ordinary Least Squares coefficients for some features and their targets.
@param trainingData - the data that we want to train on, of the form: [(URL, timedelta, [1,2,3], [4]), (...), ...]
@return - the coefficient matrix corresponding to the OLS line estimate.
"""
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
Calculates the squared error made by a given set of weights on a given test data.
@param weights - a column matrix of coefficients for different features, of the form: [[1.234],[-2.123],...]
@param testData - the data that we want to test our weights on, of the form: [(URL, timedelta, [1,2,3], [4]), (...), ...]
@return the the sum (over all examples) of the squared difference between the real target value and the prediction value.
"""
def squaredError(weights, testData):
    error = 0
    for test in testData:   # Go through each test example:
        features = test[2]  # array of features.
        target = test[3][0] # real target value is in an array with one element.
        # Make sure that matrix multiplication is possible:
        if len(features) != len(weights):
            print "ERROR: number of features for this test is not %d" % len(weights)
            print test
            continue
        prediction = np.matrix(features) * weights
        # prediction is a 2D matrix with only 1 element, so need to cast to list and grab the element.
        prediction = prediction.tolist()[0][0]
        # the squared error is the sum (over all examples) of the squared difference
        #   between the real target value and the prediction value.
        error = error + (target - prediction)**2

    return error
