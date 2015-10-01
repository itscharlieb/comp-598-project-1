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
This file is responible for:
    - extracting features from the data we downloaded
    - creating a CSV file with all the data examples and features
"""


import json, csv, datetime, re
from collections import defaultdict
import textExtractor as TE
from tfidf import *
from urlparse import urljoin

# api arguments
request = "http://api.diffbot.com/v3/article"
# 1 token = 10,000 k requests.
diffbot_token1 = "b78400cc0f6795ded5fa3d980d1348c6" #Genevieve's
diffbot_token2 = "09e512545e45166138161870d3f9a541" #Nico's
diffbot_token3 = "3a738834f4767fac91f317689b7aec21" #Charlie's

#necessary attributes to consider an item as a valid story
requiredStoryAttributes = [
    'url',
    'id',
    'title',
    'type',
    'by',
    'time',
    'descendants',
    'score'
]


"""
Filter valid stories. Validity is determined by testing the item for containing a set of features.
@param list of hacker-news items
@return list of hacker-news valid stories
"""
def filterStories(items):
    return [story for story in items if all(map(lambda attribute: attribute in story and story[attribute]!='', requiredStoryAttributes))]


"""
Parse a given unix time object to readable time elements.
@param unixTime - unixtime object (@see https://en.wikipedia.org/wiki/Unix_time)
@return - an array of comprehensive time features: [year, month, day, hour, ...]
"""
def parseTime(unixTime):
    time = datetime.datetime.fromtimestamp(int(unixTime))
    day = time.strftime("%A") #returns the day of week of the given datetime

    isMon = 1 if day == 'Monday' else 0
    isTue = 1 if day == 'Tuesday' else 0
    isWed = 1 if day == 'Wednesday' else 0
    isThu = 1 if day == 'Thursday' else 0
    isFri = 1 if day == 'Friday' else 0
    isSat = 1 if day == 'Saturday' else 0
    isSun = 1 if day == 'Sunday' else 0

    return [
        time.year,
        time.month,
        time.day,
        time.hour,
        isMon,
        isTue,
        isWed,
        isThu,
        isFri,
        isSat,
        isSun
    ]

"""
Parse a given unix time object to the corresponding year.
@param unixTime - unixtime object (@see https://en.wikipedia.org/wiki/Unix_time)
@return - the year of the given time.
"""
def parseYear(unixTime):
    return datetime.datetime.fromtimestamp(int(unixTime)).year


"""
Create a set of features for a given author.
@param author - the dictionary representing a hacker-news author.
@return - an array of features: [user karma, number of published stories, year user created]
"""
def authorFeatures(author):
    return [
        author['karma'],
        len(author['submitted']) if 'submitted' in author else 0,
        parseYear(author['created'])
    ]


"""
Create a set of features for a given story.
@param story - the dictionary representing a hacker-news story.
@return - an array of features: [URL, #of words in the title, #of comments,
    year, month, day, hour, isMon, isTue, isWed, isThu, isFri, isSat, isSun]
"""
def storyFeatures(story):
    features = [
        re.split(",|;", story['url'])[0] if story['url'] else 'N.A.', #remove weird formating after ';'
        len(story['title'].split()) if story['title'] else -1,
        story['descendants'] if story['descendants'] > 0 else 0
    ]
    features.extend(parseTime(story['time'])) #relevant time data
    return features


"""
Calls a function to grab features for a given story.
Calls another function to grab the features of the story author.
@param story - the dictionary object that represents a story.
@param users - dictionary of users
@return - an array of features for the given story and it's user.

"""
def grabFeatures(story, users):
    features = []
    features.extend(storyFeatures(story))
    author = story['by']
    if author not in users:
        raise ValueError("Could not find information on author of this story: "+story['url'])
    else :
        features.extend(authorFeatures(users[author]))
        return features


"""
Goes through the all stories, and grab features for each of them.
@param stories - set of stories.
@param users - set of users.
@return - a 2D array with line = array of feature values for 1 story.
example of features: [
    [url, f1, f2, ..., fm], <-- title line
    [&&&, ###, ###, ..., ###], <-- feature set for story #1
    [&&&, ###, ###, ..., ###], <-- feature set for story #2
    ...,
    [&&&, ###, ###, ..., ###] <-- feature set for story #n
]
"""
def extractFeatures(stories, users):
    features = [
        ['url', 'title_length', 'num_of_comments', 'year_published', 'month_published', 'day_published',
        'hour_published', 'published_on_monday', 'published_on_tuesday','published_on_wednesday',
        'published_on_thursday','published_on_friday','published_on_saturday','published_on_sunday',
        'user_karma', 'user_published_stories', 'year_user_created',
        'article_length', 'sentiment', 'num_of_links', 'avg_tfidf', 'freq_of_domain',
        'score']
    ]

    print "extracting data from URLs with API calls..."
    urls = []
    i=0
    for s in stories:
        if i<2000 : #only do 2K API calls
            urls.append(re.split(",|;", s['url'])[0])
            i=i+1
        else:
            break
    parsedURLFeatures = single_diffbotapi_call(request, diffbot_token2, urls) # get the features for the 2K urls.
    print parsedURLFeatures # dictionary of key (url), value (set of features).
    """
    parsedURLFeatures = {
        'url': [article_length, sentiment, #of links, avg_tfidf, freq of domain],
        'url': [...],
        ...
    }
    """
    print "done with the API calls."

    for story in stories: #for each story, try to get all features and append to 'features' 2D list.
        try:
            featureList = grabFeatures(story, users) # grab features from hacker-news api
            if len(parsedURLFeatures)!=0 and story['url'] in parsedURLFeatures:
                featureList.extend(parsedURLFeatures[story['url']]) # if possible, grab features from diffbot API.
            else:
                print "skip this story: %s" % story['url']
                continue
            featureList.append(story['score']) # append the score at the end.
            features.append(featureList) # append the list of features to the 2D list that will be written in the csv.
        except ValueError as e:
            print "skip this story: %s" % story['url']
            print e
        
    return features


"""
returns dictionary of url and domain name frequency
@param data - list of all urls
"""
def website_Freq(list_of_urls):
    wCount = defaultdict(int)
    wFreq = {}
    total_count = len(list_of_urls)
    for url in list_of_urls:
        parse = urljoin(url,'/')
        wCount[(url, parse)] +=1.0
    for k,v in wCount.iteritems():
        wFreq[k[0]] = (v/total_count)
    return wFreq

"""
returns count of words in article or title
@param article text extracted from diffbot api
"""
def count_words_string(text):
    tokens = text.split()
    return len(tokens)

"""
inputs url, returns sentiment of url
note: sentiment analysis ranges from -1 (absolutely negative) to 1 (absolutely positive)
@param list of urls we want to grab the sentiment analysis of
"""
def grab_sentiment_articles(sentiment):
    return sentiment

"""
Creates the features from an API call.
@param request - the request url for the API.
@param token - the token id for the API.
@param list_of_urls - list of urls we want features for.
@return - a dictionary with key (url) and value (array of features).
ex of features: {
    'url': [article_length, sentiment, #of links, avg_tfidf, freq of domain],
    'url': [...],
    ...
}
"""
def single_diffbotapi_call(request, token, list_of_urls):
    features = {}
    list_of_titles=[]
    i=0
    for url in list_of_urls:
        print i
        try:
            ti,txt,sent, num_of_links = TE.diffbot_api(request, token, url)
            cw_article = count_words_string(txt)
            sentiment = grab_sentiment_articles(sent)
            features[url] = [cw_article, sentiment, num_of_links]
            list_of_titles.append(ti)
        except KeyError as e:
            print e
        i=i+1

    update_urls = [url for url in features]

    wf = website_Freq(update_urls)
    bp = basicParse(list_of_titles)
    d2v = doc2vec(update_urls, bp)
    tfidf_r = tfidf(d2v,bp)
    for url,data in features.iteritems():
        avg_tf = take_avg(tfidf_r[url])
        features[url].append(avg_tf)   
        features[url].append(wf[url])
    return features

################## END OF FEATURES LIST ##################

"""
Create a csv file with given data
@param data - a 2D array returned by the extractFeatures() function.
"""
def createFile(data):
    with open('./data/stories2.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile)
        for row in data:
            writer.writerow(row)


"""
Main function of this file.
Puts the hacker-news items into dictionaries, and grab features for all stories.
Eventually, call the method responsible for creating the final csv data file.
"""
def process():
    #build user dictionary
    userFile = open("data/cleanedusers.json")
    users = {}
    for line in userFile:
        user = json.loads(line)
        users[user['id']] = user

    #build item list
    itemFile = open("data/items100000.json")
    items = []
    for line in itemFile:
        item = json.loads(line)
        items.append(item)

    stories = filterStories(items)
    featureTable = extractFeatures(stories, users)
    createFile(featureTable)


process()
