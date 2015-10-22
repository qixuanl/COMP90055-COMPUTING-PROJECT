# Author :  Qixuan Li
# Student Number : 708115
# Supervisor : Prof. Richard Sinnott
# COMP90055 COMPUTING PROJECT
# Project Title : Co-realationship between bottle shop and crime data

# This program is aim to get data from couchdb
# result information will be store in two txt files.


import csv
import json
from couchdb import Server
import couchdb
from geopy.geocoders import Nominatim
from pygmaps_ng import *

couch = couchdb.Server()
couch = couchdb.Server('http://115.146.86.105:5984')
db = couch['victoriapolice']


coor = []
addressName = []
geolocator = Nominatim()
BottleShopLocation = []

#----- Get address of data point 

def getAddressName(lat,lon):
	location = geolocator.reverse(lat,lon)
	return location.address

#---- Get bottle shop location 
def getBottleShopLocation():

	f = open('crimeDatajsonFile.txt','w')

	with open('bottleshopdata.json') as json_file:
		json_data = json.load(json_file)
		for index in range(len(json_data.get('features'))):
		
			lon = json_data.get('features')[index].get('geometry').get('coordinates')[0]
			lat = json_data.get('features')[index].get('geometry').get('coordinates')[1]

			content = str(lat) + ' ' + str(lon)+'\n'
			BottleShopLocation.append([lat,lon])
		print "Bottle Done"
			
#---- Get Coodinates from data

coordinates_map = '''function(doc){
	emit(doc.coordinates, doc.id);
}'''
coordinates_result = db.query(coordinates_map, descending = True)

#---- Save Data into document
wf = open('crimeData.txt','w')

for index in range(len(coordinates_result.rows)):
	lonA = coordinates_result.rows[index].key.get('coordinates')[1]
	latA = coordinates_result.rows[index].key.get('coordinates')[0]

	coor.append([lonA,latA])
	content = str(lonA) + ' ' + str(latA) +'\n'
	wf.write(content)
	
print 'Tweet Done'

getBottleShopLocation()



