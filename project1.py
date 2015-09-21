###############################################
### COMP 598 : Project #1                   ###
### ---------------------					###
### Authors:                                ###
###  + Nicolas Angelard-Gontier - 260532513 ###
###  + Genevieve Fried - #########          ###
###  + Charlie Bloomfield - 260520615       ###
###############################################

"""
used database: https://archive.ics.uci.edu/ml/datasets/Online+News+Popularity#

K. Fernandes, P. Vinagre and P. Cortez. A Proactive Intelligent Decision
    Support System for Predicting the Popularity of Online News. Proceedings
    of the 17th EPIA 2015 - Portuguese Conference on Artificial Intelligence,
    September, Coimbra, Portugal.

Number of Instances: 39797
Number of Attributes: 61 (58 predictive attributes, 2 non-predictive, 1 goal field)
Attribute Information:
    00. url:                           URL of the article (non-predictive)
    01. timedelta:                     Days between the article publication and the dataset acquisition (non-predictive)
    02. n_tokens_title:                Number of words in the title
    03. n_tokens_content:              Number of words in the content
    04. n_unique_tokens:               Rate of unique words in the content
    05. n_non_stop_words:              Rate of non-stop words in the content
    06. n_non_stop_unique_tokens:      Rate of unique non-stop words in the content
    07. num_hrefs:                     Number of links
    08. num_self_hrefs:                Number of links to other articles published by Mashable
    09. num_imgs:                      Number of images
    10. num_videos:                    Number of videos
    11. average_token_length:          Average length of the words in the content
    12. num_keywords:                  Number of keywords in the metadata
    13. data_channel_is_lifestyle:     Is data channel 'Lifestyle'?
    14. data_channel_is_entertainment: Is data channel 'Entertainment'?
    15. data_channel_is_bus:           Is data channel 'Business'?
    16. data_channel_is_socmed:        Is data channel 'Social Media'?
    17. data_channel_is_tech:          Is data channel 'Tech'?
    18. data_channel_is_world:         Is data channel 'World'?
    19. kw_min_min:                    Worst keyword (min. shares)
    20. kw_max_min:                    Worst keyword (max. shares)
    21. kw_avg_min:                    Worst keyword (avg. shares)
    22. kw_min_max:                    Best keyword (min. shares)
    23. kw_max_max:                    Best keyword (max. shares)
    24. kw_avg_max:                    Best keyword (avg. shares)
    25. kw_min_avg:                    Avg. keyword (min. shares)
    26. kw_max_avg:                    Avg. keyword (max. shares)
    27. kw_avg_avg:                    Avg. keyword (avg. shares)
    28. self_reference_min_shares:     Min. shares of referenced articles in Mashable
    29. self_reference_max_shares:     Max. shares of referenced articles in Mashable
    30. self_reference_avg_sharess:    Avg. shares of referenced articles in Mashable
    31. weekday_is_monday:             Was the article published on a Monday?
    32. weekday_is_tuesday:            Was the article published on a Tuesday?
    33. weekday_is_wednesday:          Was the article published on a Wednesday?
    34. weekday_is_thursday:           Was the article published on a Thursday?
    35. weekday_is_friday:             Was the article published on a Friday?
    36. weekday_is_saturday:           Was the article published on a Saturday?
    37. weekday_is_sunday:             Was the article published on a Sunday?
    38. is_weekend:                    Was the article published on the weekend?
    39. LDA_00:                        Closeness to LDA topic 0
    40. LDA_01:                        Closeness to LDA topic 1
    41. LDA_02:                        Closeness to LDA topic 2
    42. LDA_03:                        Closeness to LDA topic 3
    43. LDA_04:                        Closeness to LDA topic 4
    44. global_subjectivity:           Text subjectivity
    45. global_sentiment_polarity:     Text sentiment polarity
    46. global_rate_positive_words:    Rate of positive words in the content
    47. global_rate_negative_words:    Rate of negative words in the content
    48. rate_positive_words:           Rate of positive words among non-neutral tokens
    49. rate_negative_words:           Rate of negative words among non-neutral tokens
    50. avg_positive_polarity:         Avg. polarity of positive words
    51. min_positive_polarity:         Min. polarity of positive words
    52. max_positive_polarity:         Max. polarity of positive words
    53. avg_negative_polarity:         Avg. polarity of negative  words
    54. min_negative_polarity:         Min. polarity of negative  words
    55. max_negative_polarity:         Max. polarity of negative  words
    56. title_subjectivity:            Title subjectivity
    57. title_sentiment_polarity:      Title polarity
    58. abs_title_subjectivity:        Absolute subjectivity level
    59. abs_title_sentiment_polarity:  Absolute polarity level
    60. shares:                        Number of shares (target)

"""
import csv
import numpy as np
import random

"""
Split data into 2.
@param data_length - the number of examples in the dataset.
@param training_percentage - the percentage of the data that will be used to train our learner.
@returns - two 2D array: the first one being training data, the other being test data.
"""
def splitData(data_length, training_percentage=0.5):
    training = []
    test = []

    training_size = data_length * training_percentage
    # create an array of size 'training_size' with random indices from 1 to len(data)-1
    random_examples = random.sample(range(data_length)[1:], training_size)
    for i in range(data_length)[1:]:
        if i in random_examples:
            training.append(data[i])
        else:
            test.append(data[i])

    return training, test

"""
Asume a title line at the begining of the file.
"""
def readData(path, num_features):
    x = []
    y = []
    
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
                x.append(map(float,row[2:num_features-1]))  # features are from 3rd column to 61st column
                y.append([float(row[num_features-1])])      # shares is at 61st column

            example=example+1   # increment example counter

    return x,y


path = "./OnlineNewsPopularity/OnlineNewsPopularity.csv"
num_features = 61
num_examples = 39644

x,y = readData(path, num_features)

#train, test = splitData(x , 0.7)

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


