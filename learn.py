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
part = learnerengine.partition([1, 2, 3])
print(part)

"""
Returns a list of 2-tuples.
Each 2-tuple takes the form (featureList * instance)
Assume a title line at the begining of the file.
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

                url = row[0]                              # URL is at 1st column
                timedelta = float(row[1])                 # time delta is at 2nd column
                featureList = map(float,row[2:num_features-1])  # features are from 3rd column to 61st column
                instance = [float(row[num_features-1])]     # shares is at 61st column
                data.append((featureList, instance))

            example=example+1   # increment example counter

    return data


path = "./OnlineNewsPopularity/OnlineNewsPopularity.csv"
num_features = 61
data = readData(path, num_features)
results = learnerengine.multiTrain(linreg.ols, data)
print(len(results))