#!/usr/bin/env python

###############################################
### COMP 598 : Project #1                   ###
### ---------------------					###
### Authors:                                ###
###  + Nicolas Angelard-Gontier - 260532513 ###
###  + Genevieve Fried - 260564432          ###
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

from learner import *
import datetime

start = datetime.datetime.now()

weightSoln = ols

path_to_given_data = "./OnlineNewsPopularity/OnlineNewsPopularity.csv"
path_to_new_data = "./data/stories.csv"

given_data = readData(path_to_given_data)
# Try with k = 1,2,4,8,11,17,22,34,44, ..., 187,212, ..., 901,1166,1802,2332,3604,4918,9911,19822,39644.
subsets = multiPartition(given_data, 39644) #creates k subsets of equal size.

new_data = readData(path_to_new_data, True)
# Try with k = 1,2,3,5,6,7,10,14,15,21,...,105,206,...,1030,1442,1545,2163,3090,3605,4326,7210,10815,21630.
new_subsets = multiPartition(new_data, 21630) #creates k subsets of equal size.

print "There are %d subsets." % len(new_subsets)
print "Each subset has %d examples." % len(new_subsets[0])
averageWeights, averageError = multiTrain(weightSoln, new_subsets) # k-fold cross validation
print averageError

end = datetime.datetime.now()
print end-start

"""
print "100'%' training:"
# take all the data as training data.
training_data, testing_data = partition(data, 1)
print "length of training: %d/%d" % (len(training_data), len(data))
print "length of testing: %d/%d" % (len(testing_data), len(data))
W = train(weightSoln, training_data)
#W = train(gradientDescent, training_data)
print W
"""

"""
print "75'%' as training, 25'%' as test:"
training_data, testing_data = partition(data, 0.75)
print "length of training: %d/%d" % (len(training_data), len(data))
print "length of testing: %d/%d" % (len(testing_data), len(data))
W = train(weightSoln, training_data)
#W = train(gradientDescent, training_data)
#print W
error = squaredError(W, testing_data)
print "error: %e" % error
"""

"""
print "50'%' as training, 50'%' as test:"
training_data, testing_data = partition(data, 0.50)
print "length of training: %d/%d" % (len(training_data), len(data))
print "length of testing: %d/%d" % (len(testing_data), len(data))
W = train(weightSoln, training_data)
#W = train(gradientDescent, training_data)
#print W
error = squaredError(W, testing_data)
print "error: %e" % error
"""
