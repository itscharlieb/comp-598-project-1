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

import json, csv, string, datetime
from urlhacker import parseUrl
from collections import defaultdict
from nltk.tokenize import word_tokenize, sent_tokenize
import textExtractor as TE

# api arguments
diffbot_token1 = "b78400cc0f6795ded5fa3d980d1348c6"     #Genevieve's      #10,000 k articles each 
diffbot_token2 = "09e512545e45166138161870d3f9a541"     #Nico's
diffbot_token3 = "3a738834f4767fac91f317689b7aec21"

request = "http://api.diffbot.com/v3/article"

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
@param list of hacker-news items
@return list of hacker-news valid stories

Validity is determined by testing the item for containing a set of features.
"""
def filterStories(items):
    return [story for story in items if all(map(lambda attribute: attribute in story and story[attribute]!='', requiredStoryAttributes))]


def weekday(time):
    return False

"""
@param unixtime object (@see https://en.wikipedia.org/wiki/Unix_time)
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
"""
def parseYear(unixTime):
    return datetime.datetime.fromtimestamp(int(unixTime)).year


"""
features: user karma, number of published stories, year user created
"""
def authorFeatures(author):
    return [
        author['karma'],
        len(author['submitted']) if 'submitted' in author else 0,
        parseYear(author['created'])
    ]


"""
features: URL, #of comments, year, month, day, hour, isMon, isTue, isWed, isThu, isFri, isSat, isSun
"""
def storyFeatures(story):
    features = [
        story['url'].split(';')[0] if story['url'] else 'N.A.', #remove weird formating after ';'
        len(story['title'].split()) if story['title'] else -1,
        story['descendants'] if story['descendants'] > 0 else 0
    ]
    features.extend(parseTime(story['time'])) #relevant time data
    return features


""" ==> TODO <==
Grabs features for a given story (in json format)
@param story - the dictionary object that represents a story.
@param users - dictionary of users
@return - an array of features for the given story.
"""
def grabFeatures(story, users):
    author = story['by']
    if(author not in users):
        raise ValueError("Could not find information on author of this story: "+story['url'])

    features = []
    features.extend(storyFeatures(story))
    features.extend(authorFeatures(users[author]))
    #features.extend(parseUrl(story))
    features.append(story['score'])
    return features


""" ==> TODO <==
Goes through the 100,000 items, and grab features for each of them.
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
        ['url', 'tile_length', 'num_of_comments', 'year_published', 'month_published', 'day_published',
        'hour_published', 'published_on_monday', 'published_on_tuesday','published_on_wednesday',
        'published_on_thursday','published_on_friday','published_on_saturday','published_on_sunday',
        'user_karma', 'user_published_stories', 'year_user_created', 'score']
    ]
    for story in stories:
        try:
            featureList = grabFeatures(story, users)
            features.append(featureList)
        except ValueError as e:
            print e
        
    return features


"""
frequency of websites across articles
@param data - list of all urls
"""
def website_Freq(list_of_urls):
    wCount = defaultdict(int)
    wFreq = {}
    total_count = len(list_of_urls)
    for url in listofurls:
        parse = url.split('.')
        for pou in range(len(parse)):
            if "www" in parse[pou]:
                wCount[parse[pou+1]] +=1.0
    for k,v in wCount.iteritems():
        wFreq[k] = (v/total_count)
    return wFreq

"""
returns count of words in article or title
@param article text extracted from diffbot api
"""
def count_words_string(text):
    tokens = []
    no_punct = text.translate(None, string.punctuation)
    tokens = word_tokenize(no_punct)
    return len(tokens)

"""
inputs url, returns sentiment of url
note: sentiment analysis ranges from -1 (absolutely negative) to 1 (absolutely positive)
@param list of urls we want to grab the sentiment analysis of
"""
def grab_sentiment_articles(sentiment):
    return sentiment

def grab_diffbotapi_objs(url):
    ti,txt,a,sent = TTE.diffbot_api(request, diffbot_token, url)
    return ti,txt,a,sent


##NOTE listofurls needs to be comprised from hackernewsapi
def single_diffbotapi_call(request, token, list_of_urls):
    features = {}
    list_of_websites=[]
    list_of_titles=[]

    url_authors={}
    url_websites={}
    # count number of words in text
    #sentiment analysis
    for url in list_of_urls:
        
        ti,txt,sent,num_of_images, num_of_links = TE.diffbot_api(request, token, url)
        
        cw_title = count_word_string(ti)
        cw_article = count_word_string(txt)
        sentiment = grab_sentiment_articles(sent)

        features[url] = [cw_title, cw_article, sentiment, num_of_images, num_of_links]     #5features

        list_of_websites.append(url)
        list_of_titles.append(ti)         # need for semantic relevance

    wf = website_Freq(list_of_websites)       # 1 feature

    return features, wf, list_of_titles     


################## END OF FEATURES LIST ##################

"""
Create a csv file with given data
@param data - a 2D array returned by the extractFeatures() function.
"""
def createFile(data):
    with open('./data/stories.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile)
        for row in data:
            writer.writerow(row)


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
    urls = []
    for s in stories:
        urls.append(re.split(",|;", s['url']))
    stories = filterStories(items)
    featureTable = extractFeatures(stories, users)
    createFile(featureTable)

    return urls

list_of_urls = process()



##################################
## more features
