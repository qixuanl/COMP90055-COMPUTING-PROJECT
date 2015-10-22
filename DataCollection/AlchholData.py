# Author :  Qixuan Li
# Student Number : 708115
# Supervisor : Prof. Richard Sinnott
# COMP90055 COMPUTING PROJECT
# Project Title : Co-realationship between bottle shop and crime data

# This program is aim to collect tweets about alcohol from Twitter by Search API
# result information will be store into Couchdb



import tweepy
import time
import couchdb
import os
import json
import urllib2
from textblob import TextBlob
from math import sin, cos, sqrt, atan2, radians
from textblob.classifiers import NaiveBayesClassifier


#access_token ="3117777675-akJ3VP1wB0JmQyQYxpKSCkcI1NxsjqCxyIMwKFw"
#access_token_secret ="KHlPUcX0VqNcwLyAMUOVbim1FCgx5BiPj1HrNJ2oEww8J"
#consumer_key ="xIiP1sOFvDRyqgTIjCXe7gdzJ"
#consumer_secret ="u6mEk6WmfX0W22eZizw7WaElywSmlc4PLVeFzp5yk9D3YKoTzx"



#access_token ="3117777675-eEaaoPx92zjouBXwaxogIXltK7IjZ0ys3lrW0hq"
#access_token_secret ="fW70MdRHHiNMqOz1bBLJH3kuzMduH6tfSopk58ffAuTO2"
#consumer_key ="bnOyfnvoYbFCjHFCjPaLHo6GY"
#consumer_secret ="V5J8ZcHD2wEYK2EdG6KlRdrnmLFFebYvMrdCWYI0R71rsAvHD5"

access_token ="3117777675-aLMfbwbugNEsbKqz5gkzMqeQUhpiDFLCsgxKu5X"
access_token_secret ="XBs6x0yQFOD674N0qefMNufqAL5IFxb2ig1f1VzbOupTT"
consumer_key ="WqkUrOD3qEIIqKFVGNTUqielz"
consumer_secret ="fObSAs1AvltXvSY7TrcxJEjUnbARyO7xJhjeQX9f9iUnE9hjWp"



auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

couch = couchdb.Server()
#couch = couchdb.Server('http://115.146.86.105:5984')
couch = couchdb.Server('http://localhost:5984')
#db = couch.create('alcoholdata')
db = couch['alcoholdata']

api = tweepy.API(auth)

trainBase = [("crime","pos"),("illegal","pos"),("arrest","pos"),("kidnapping","pos"),("murder","pos"),("violence","pos"),("drug","pos"),("fraud","pos"),("homcide","pos"),("drunk driving","pos"),("theft","pos"),("stealing","pos"),
("smuggling","pos"),("rob","pos"),("gun","pos"),("morning","neg"),("apple","neg"),("orange","neg"),("good","neg"),("time","neg"),("sport","neg"),("basketball","neg"),("watch","neg"),("water","neg"),("book","neg"),("ring","neg"),("swimming","neg"),("tea","neg")]

train = NaiveBayesClassifier(trainBase)


def addPostcode(lon, lat):
    geoGoogle = "http://maps.googleapis.com/maps/api/geocode/json?address="
    page = urllib2.urlopen(geoGoogle+lon+','+lat)
    pageString = page.read().decode("utf-8")
    json_data = json.loads(pageString)['results']
    for result in json_data:
        if result['types'] == ["postal_code"]:
            for addr in result["address_components"]:
                if addr['types'] == ["postal_code"]:
                    #print addr['long_name']
                    return addr['long_name']

def sentimentAnalysis(text):
    blob = TextBlob(text)
    blob.tags
    blob.noun_phrases
    sentimentValue = 0
    finalResult =''
    for sentence in blob.sentences:
        sentimentValue = sentence.sentiment.polarity
    if sentimentValue > 0:
        finalResult = 'po'
    else:
        finalResult = 'neg'
    return finalResult


def get_all_tweets(user_id):

    alltweets = []  
    new_tweets = api.user_timeline(user_id = user_id,count=200)
    alltweets.extend(new_tweets)
    oldest = alltweets[-1].id - 1
        
    while len(new_tweets) > 0:
        new_tweets = api.user_timeline(user_id = user_id,count=200,max_id=oldest)
        alltweets.extend(new_tweets)
        oldest = alltweets[-1].id - 1
    
    for tweet in alltweets:
        try:
            if tweet._json["coordinates"] !=None:
                lat1 = tweet.coordinates["coordinates"][0]
                lon1 = tweet.coordinates["coordinates"][1]
                distance = int(distanceCalculation(lat1,lon1,144.647029,-37.633875))
                if distance <=50:
                    saveTweet(tweet)

        except AttributeError:
            continue
        except couchdb.http.ResourceConflict:
            continue

def saveTweet(tweet):
    
            createTime = 'created_at'
            content = 'content'
            userId = 'user_id'
            tweetId = 'tweet_id'
            location = 'location'
            sentiment = 'sentiment'
            coordinates = 'coordinates'
            postal_code = 'postal_code'
            crimeTweet = 'crimeTweet'

            if tweet._json["coordinates"] !=None:
                
                contentValue = str(tweet.text.encode('ascii','ignore'))
                createTimeValue = str(tweet.created_at)
                userIdValue = str(tweet.user.id_str)
                tweetIdValue = str(tweet.id_str)
                locationValue = str(tweet.place.bounding_box.coordinates)
                sentimentValue = sentimentAnalysis(contentValue)
                coordinatesValue = tweet.coordinates
                lat1 = str(tweet.coordinates["coordinates"][0])
                lon1 = str(tweet.coordinates["coordinates"][1])
                postCodeValue = str(addPostcode(lon1,lat1))
                relevantContent = train.prob_classify(contentValue.lower())
                crimeTweetValue = round(relevantContent.prob("pos"),2)
                #print crimeTweetValue

                #if crimeTweetValue > 0.55:

                finalFormat = {"_id": tweetIdValue,createTime: createTimeValue,userId: userIdValue,tweetId: tweetIdValue,content: contentValue,location: locationValue,sentiment: sentimentValue,coordinates: coordinatesValue,postal_code: postCodeValue,crimeTweet: crimeTweetValue}
                db.save(finalFormat)

def distanceCalculation(lat1,lon1,lat2,lon2):
    
    R = 6373.0
    lat1F = radians(lat1)
    lon1F = radians(lon1)
    lat2F = radians(lat2)
    lon2F = radians(lon2)

    dlon = lon2F - lon1F
    dlat = lat2F - lat1F

    a = sin(dlat / 2)**2 + cos(lat1F) * cos(lat2F) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    return distance

c=tweepy.Cursor(api.search,                                           
                           result_type="recent",
                           include_entities=True,
                           count = 100,
                           q = '#alcohol',
                           geocode="-37.633875,144.647029,30km").items(1000000)

userIdCollection = []
while True:
    try:
        tweet = c.next()

        if tweet._json["coordinates"] !=None:
            
            lat1 = tweet.coordinates["coordinates"][0]
            lon1 = tweet.coordinates["coordinates"][1]
            distance = int(distanceCalculation(lat1,lon1,144.647029,-37.633875))

            if distance <=50:
                saveTweet(tweet)
                print 'ok2'

        if userIdCollection.count(tweet.user.id_str)==0:

            userIdCollection.append(tweet.user.id_str)
            get_all_tweets(tweet.user.id_str)

    except tweepy.TweepError:
        time.sleep(60 * 15)
        continue
    except couchdb.http.ResourceConflict:
        continue
    except StopIteration:
        break   
    
    
   