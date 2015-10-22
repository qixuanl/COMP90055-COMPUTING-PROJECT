 Author :  Qixuan Li
# Student Number : 708115
# Supervisor : Prof. Richard Sinnott
# COMP90055 COMPUTING PROJECT
# Project Title : Co-realationship between bottle shop and crime data

# This program is aim to get all bottleshop location in melbourne
# result information will be store in a txt file


import json
from pprint import pprint

f = open('bottleshopjsonFile.txt','w')

# Write to file
with open('bottleshopdata.json') as json_file:
	json_data = json.load(json_file)
	print len(json_data.get('features')) 

	for index in range(len(json_data.get('features'))):
		
		lon = json_data.get('features')[index].get('geometry').get('coordinates')[0]
		lat = json_data.get('features')[index].get('geometry').get('coordinates')[1]

		content = str(lat) + ' ' + str(lon)+'\n'
		print content
		f.write(content)

