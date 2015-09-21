###############################################
### COMP 598 : Project #1                   ###
### ---------------------					###
### Authors:                                ###
###  + Nicolas Angelard-Gontier - 260532513 ###
###  + Genevieve Fried - #########          ###
###  + Charlie Bloomfield - 260520615       ###
###############################################

import csv
import linreg
import learnerengine

"""
Read the data from a CSV file and put it all in an array.
Assume a title line at the begining of the file.
@param path - the path to the file to read.
@param num_features - the number of features in one row.
@return - an array of tuples of the form (array of features, array of target).
"""
def readData(path, num_features):
    data = []
    with open(path, 'rb') as datafile:
        reader = csv.reader(datafile)
        example = 0
        for row in reader:      # go through each line
            if example > 0:     # skip the first line (title of each feature)

                if len(row) != num_features: # check that nuber of features is correct
                    print "ERROR: number of features for this row is not %d" % num_features
                    print row
                    continue

                url = row[0]                                 # URL is at 1st column
                timedelta = float(row[1])                    # time delta is at 2nd column
                features = map(float,row[2:len(row)-1])  # features are from 3rd column to 60th column
                target = [float(row[len(row)-1])]        # shares is at 61st column

                data.append((features, target))

            example=example+1   # increment example counter

    return data


path = "./OnlineNewsPopularity/OnlineNewsPopularity.csv"
num_features = 61
data = readData(path, num_features)

# split data into 2 with 70% being training data.
training_data, testing_data = learnerengine.partition(data, 0.7)
#TODO: learn on training.
#TODO: check error on test.