# Author :  Qixuan Li
# Student Number : 708115
# Supervisor : Prof. Richard Sinnott
# COMP90055 COMPUTING PROJECT
# Project Title : Co-realationship between bottle shop and crime data

# This program is aim to generate web application distance = 100 and 50 m


import pickle
import csv
import json
from couchdb import Server
import couchdb
from geopy.geocoders import Nominatim
from pygmaps_ng import *
from collections import OrderedDict


crimeData = []
crimeData100 = []
bottleShopData = []
bottleShopData100 =[]
crimePonintData = []
crimePonintData100 = []
bottlePointData = []
bottlePointData100 = []
count = 0

with open('crimeDataLocationF(50).txt', 'rb') as f:
    crimeData = pickle.load(f)

with open('BottleshopLocationF(50).txt', 'rb') as f:
    bottleShopData = pickle.load(f)

with open('crimeDataLocation(100).txt', 'rb') as f:
    crimeData100 = pickle.load(f)

with open('bottleshopLocation(100).txt', 'rb') as f:
    bottleShopData100 = pickle.load(f)


# read crime data distance = 50 m from file & how many crime data in a cluster
def readCrimeData(k):

	for index in range(3000):
	
		for j in range(len(crimeData[index])):
			
			if len(crimeData[index])>=k:
				global count 
				count = count +1
				a = crimeData[index][j].split()
				crimePonintData.append([float(a[0]),float(a[1])]) 
				b = bottleShopData[index][0].split()
				bottlePointData.append((float(b[0]),float(b[1])))
			else:
				pass

# read crime data distance = 100 m from file
def readCrimeData100(k):

	for index in range(3000):
	
		for j in range(len(crimeData100[index])):
			
			if len(crimeData100[index])>=k:
				global count 
				count = count +1
				a = crimeData100[index][j].split()
				crimePonintData100.append([float(a[0]),float(a[1])]) 
				b = bottleShopData100[index][0].split()
				bottlePointData100.append((float(b[0]),float(b[1])))
			else:
				pass


# Remove Duplicat crime data
def removeDuplicate(seq):
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if not (x in seen or seen_add(x))]

#---show data visualization
def drawMap():
	
	mymap = Map()
	app1 = App('test1',title="The Crime Data around Bottle Shop: 50m")
	app2 = App('test1',title="The Crime Data around Bottle Shop: 100m")
	mymap.apps.append(app1)
	mymap.apps.append(app2)
	
	dataset1 = DataSet('data1', title="Crime Data" ,key_color='FF0088')
	dataset2 = DataSet('data2', title="Bottle shop" ,key_color='FF0000')
	
	dataset3 = DataSet('data3', title="Crime Data" ,key_color='FF0089')
	dataset4 = DataSet('data4', title="Bottle shop" ,key_color='FF0001')
	app1.datasets.append(dataset1)
	app1.datasets.append(dataset2)

	app2.datasets.append(dataset3)
	app2.datasets.append(dataset4)


	for index in range(len(crimePonintData)):
		pt = crimePonintData[index]

		w = '<a href="https://www.google.com.au/maps/place/">'+str(str(crimePonintData[index][0])+ ' '+ str(crimePonintData[index][1]))+'</a>'
		dataset1.add_marker(pt ,title="click me",color="000000",text=w)
	
	temp = removeDuplicate(bottlePointData)
	print len(temp)
	for index in range(len(temp)):
		pt = temp[index]
		t = '<a href="https://www.google.com.au/maps/place/">'+ 'BottleShop: ' + str(len(crimeData[index])) + '</a>'
		dataset2.add_marker(pt ,title="click me",color="FF0000",text=t)




	for index in range(65000):
		pt = crimePonintData100[index]
		l = '<a href="https://www.google.com.au/maps/place/">'+str(str(crimePonintData100[index][0])+ ' '+ str(crimePonintData[index][1]))+'</a>'
		
		dataset3.add_marker(pt ,title="click me",color="000000",text=l)
	
	temp1 = removeDuplicate(bottlePointData100)
	print len(temp1)
	for index in range(len(temp1)):
		pt = temp1[index]
		t = '<a href="https://www.google.com.au/maps/place/">'+ 'BottleShop: '  +str(len(crimeData[index])) + '</a>'
		dataset4.add_marker(pt ,title="click me",color="FF0000",text=t)

	mymap.build_page(center=pt,zoom=14,outfile="Melb1.html")
	print 'Graph Down'


readCrimeData(10)

readCrimeData100(10)
print ''
print '--------------------'
drawMap()