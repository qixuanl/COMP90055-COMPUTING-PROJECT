# Author :  Qixuan Li
# Student Number : 708115
# Supervisor : Prof. Richard Sinnott
# COMP90055 COMPUTING PROJECT
# Project Title : Co-realationship between bottle shop and crime data

# This program is aim to collect tweets about alcohol from Twitter by Stemming API
# result information will be store into Couchdb



from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import tweepy
import couchdb
import os
import json
from textblob import TextBlob
import urllib2
from math import sin, cos, sqrt, atan2, radians




access_token ="3117777675-akJ3VP1wB0JmQyQYxpKSCkcI1NxsjqCxyIMwKFw"
access_token_secret ="KHlPUcX0VqNcwLyAMUOVbim1FCgx5BiPj1HrNJ2oEww8J"
consumer_key ="xIiP1sOFvDRyqgTIjCXe7gdzJ"
consumer_secret ="u6mEk6WmfX0W22eZizw7WaElywSmlc4PLVeFzp5yk9D3YKoTzx"
couch = couchdb.Server()

couch = couchdb.Server('http://localhost:5984')
db = couch['alcoholdata']
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


def addPostcode(lon, lat):
    geoGoogle = "http://maps.googleapis.com/maps/api/geocode/json?address="
    page = urllib2.urlopen(geoGoogle+lon+','+lat)
    pageString = page.read().decode("utf-8")
    json_data = json.loads(pageString)['results']
    for result in json_data:
        if result['types'] == ["postal_code"]:
            for addr in result["address_components"]:
                if addr['types'] == ["postal_code"]:
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

class StdOutListener(StreamListener):

	def on_status(self, status):
		while True:
			try:
				createTime = 'created_at'
				content = 'content'
				userId = 'user_id'
				tweetId = 'tweet_id'
				retweetCount = 'retweet_count'
				statusesCount = 'statuses_count'
				followersCount = 'followers_count'
				favoriteCount = 'favorite_count'
				location = 'location'
				retweetStatus = 'retweeted_status'
				language = 'lang'
				sentiment = 'sentiment'
				suburb = 'suburb'
				postal_code = 'postal_code'

				if status._json["coordinates"] !=None:

					contentValue = str(status.text.encode('ascii','ignore'))
					createTimeValue = str(status.created_at)
					userIdValue = str(status.user.id_str)
					tweetIdValue = str(status.id_str)
					retweetCountValue = status.retweet_count
					statusesCountValue = status.user.statuses_count
					followersCountValue = status.user.followers_count
					favoriteCountValue = status.favorite_count
					lat1 = str(status.coordinates["coordinates"][0])
					lon1 = str(status.coordinates["coordinates"][1])
					postCodeValue = str(addPostcode(lon1,lat1))
					locationValue = str(status.place.bounding_box.coordinates)
					languageValue = str(status.lang)
					sentimentValue = sentimentAnalysis(contentValue)


					finalFormat = {"_id": tweetIdValue,createTime: createTimeValue,userId: userIdValue,tweetId: tweetIdValue,content: contentValue,retweetCount: retweetCountValue,statusesCount: statusesCountValue,followersCount: followersCountValue,favoriteCount: favoriteCountValue,location: locationValue,language: languageValue, sentiment: sentimentValue, postal_code: postCodeValue}
					db.save(finalFormat)
					print 'ok'

			except AttributeError:
				continue
			except couchdb.http.ResourceConflict:
				continue

		return True

	def on_error(self, status_code):
		print str(status_code)
		return True

	def on_timeout(self):
		print('Timeout...')
		return True # To continue listening

sapi = tweepy.streaming.Stream(auth, StdOutListener())    
sapi.filter(locations=[144.406703,-38.174037,145.747035,-37.475468],track = ['alcohol','crime','police'],async = True)
