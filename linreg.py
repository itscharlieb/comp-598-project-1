###############################################
### COMP 598 : Project #1                   ###
### ---------------------					###
### Authors:                                ###
###  + Nicolas Angelard-Gontier - 260532513 ###
###  + Genevieve Fried - #########          ###
###  + Charlie Bloomfield - 260520615       ###
###############################################

import sys, random
import numpy as np



#returns the set of weights that define the ols line estimate over the parameter data
#data is a list of [feature, val] lists
"""
def ols(features, instances): 
	X = np.matrix(features)
	Y = np.matrix(instances)

	product1 = X.transpose() * X
	product2 = X.transpose() * Y
	W = product1.getI() * product2
"""

#returns the set of weights that define the gradient descent estimate over the parameter data

def ErrW(wVec, xVec, yVec):
	
	print np.array.shape(wVec)

	print wVec.size
	print xVec.size
	print yVec.size

	p1 = np.dot(np.transpose(xVec),xVec)
	p2 = np.dot(p1,wVec)
	p3 = np.dot(np.transpose(xVec),yVec)

	
	return np.dot(2,np.subtract(p2,p3))


#TOD0: Look into wolfe conditions or robin monroe's sequence for alpha
def gradientDescent(features, instances):
	alpha = random.randint(0,1) #to be replaced later with a more sophisticated alg
	epsilon = 0.0001	
	##initial construction of gradient descent alg
	lenM = len(features)
	#wCrt = [random.random() for x in range(lenM)]
	wCrt = (np.matrix.append(random.random()) for x in range(lenM))
	aErr = np.dot(alpha, ErrW(wCrt, features, instances))
	wNext = np.subtract(wCrt, aErr)

	## gradient descent

	count = 500

	while (500 != 0):
		while( np.absolute(np.subtract(wNext, wCrt)) > epsilon):
			wCrt = wNext
			aErr(np.dot(alpha, Err(wCrt, features, instances)))
			wNext = np.subtract(wCrt, aErr)

			print "current weight value is" + wNext
		count = count - 1
	return wNext	


#returns the squared error of points over the function defined by weights

def squaredError(weights, points):
	pass