###############################################
### COMP 598 : Project #1                   ###
### ---------------------					###
### Authors:                                ###
###  + Nicolas Angelard-Gontier - 260532513 ###
###  + Genevieve Fried - #########          ###
###  + Charlie Bloomfield - 260520615       ###
###############################################

import numpy as np

"""
returns the set of weights that define the ols line estimate over the parameter data
data is a list of [feature, val] lists
"""
def ols(features, dependents):
	product1 = X.transpose() * X
	product2 = X.transpose() * Y
	return product1.getI() * product2


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