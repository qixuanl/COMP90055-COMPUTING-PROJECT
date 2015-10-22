# Author :  Qixuan Li
# Student Number : 708115
# Supervisor : Prof. Richard Sinnott
# COMP90055 COMPUTING PROJECT
# Project Title : Co-realationship between bottle shop and crime data

# This program is aim to calculate user defined cluster 
# result information will be store in two txt files.

import json
from math import sin, cos, sqrt, atan2, radians
import pickle


rc = open('crimeData.txt','r')
rb = open('bottleshopjsonFile.txt','r')
crimeData = []
locationData = []
resultList = []
pairList = []


# Load Crime data and Bottleshop location
def loadData():

	for lineB in rb:
		lineB = lineB.split()
		locationContent = lineB[0] +' ' +lineB[1]
		locationData.append([locationContent])
	
	for lineC in rc:
		lineC = lineC.split()
		crimeContent = lineC[0] + ' ' + lineC[1]
		crimeData.append([crimeContent])

	print 'Load Data done!'

# Calculate bottleshop distance from crime data

def calculateDistance(lat1R,lon1R,lat2R,lon2R):
	R = 6373.0

	lat1 = radians(lon1R)
	lon1 = radians(lat1R)
	lat2 = radians(lon2R)
	lon2 = radians(lat2R)

	dlon = lon2 - lon1
	dlat = lat2 - lat1

	a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
	c = 2 * atan2(sqrt(a), sqrt(1 - a))

	distance = R * c

	return distance

# Claculate the distance between bottle shop and a crime tweet
def countCrimedataAroundBottleshop(dis):
	d = dis * 0.001
	for i in range(len(locationData)):
			item = locationData[i]
			bottleshopLocation = item[0].split()
			lat1R = float(bottleshopLocation[0])
			lon1R = float(bottleshopLocation[1])
			content1 = str(lat1R) + ' ' + str(lon1R)
			temp = compare(lat1R,lon1R,d)
			print str(i) + '\n'
			if temp == []:
				pass
			else:
				pairList.append([content1])

# Find all crime tweets data around a bottle shop, and append to crime tweets dataset			
def compare(lat1,lon1,d):
	reTweet = []
	for j in range(len(crimeData)):
				item2 = crimeData[j]
				crimeDataLocation = item2[0].split()
				lat2R = float(crimeDataLocation[0])
				lon2R = float(crimeDataLocation[1])
				distance = calculateDistance(lat1,lon1,lat2R,lon2R)
				if distance <= d:
					content = str(lat2R) + ' ' + str(lon2R)
					reTweet.append(str(content))
	if list(set(reTweet)) == []:
		return []
	else:
		resultList.append(list(set(reTweet)))


loadData()
countCrimedataAroundBottleshop(100)


#Write to file
with open('bottleshopLocation.txt', 'wb') as f:
    pickle.dump(pairList, f)
with open('crimeDataLocation.txt', 'wb') as f:
    pickle.dump(resultList, f)


