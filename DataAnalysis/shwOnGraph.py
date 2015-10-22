# Author :  Qixuan Li
# Student Number : 708115
# Supervisor : Prof. Richard Sinnott
# COMP90055 COMPUTING PROJECT
# Project Title : Co-realationship between bottle shop and crime data

# This program is aim to generate plot graph of first 50 bottle shop distance = 100 and 50 m


import pickle
from numpy import *
import matplotlib
import matplotlib.pyplot as plt


xcord0 = []
ycord0 = []
xcord1 = []
ycord1 = []
markers =[]
colors =[]
index = []
crimeData = []
bottleShopData = []
crimePonintData = []
bottlePointData = []
tempbottlePointData = []
tempcrimePonintData = []

# read the File
with open('crimeDataLocation(100).txt', 'rb') as f:
    crimeData = pickle.load(f)

with open('bottleshopLocation(100).txt', 'rb') as f:
    bottleShopData = pickle.load(f)


# read crime data distance = 50 m from file & how many crime data in a cluster
def readCrimeData(k):

	for index in range(3000):
	
		for j in range(len(crimeData[index])):
			
			if len(crimeData[index])>=k:
	
				a = crimeData[index][j].split()
				crimePonintData.append((str(a[0]) +' '+str(a[1]))) 
				b = bottleShopData[index][0].split()
				bottlePointData.append((str(b[0])+' '+str(b[1])))
			else:
				pass

# Remove Duplicat crime data
def removeDuplicate(seq):
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if not (x in seen or seen_add(x))]


#---show data visualization
readCrimeData(20)
tempbottlePointData = removeDuplicate(bottlePointData)
tempcrimePonintData = removeDuplicate(crimePonintData)


for j in range(50):
	a = tempbottlePointData[j].split()
	b = float(a[0])
	c = float(a[1]) 
	xcord0.append(b)
	ycord0.append(c)


for j in range(50):
	a = tempcrimePonintData[j].split()
	b = float(a[0])
	c = float(a[1]) 
	xcord1.append(b)
	ycord1.append(c)
print xcord1
print ycord1

for i in range(0,34):
	i = i +1
	index.append(i)


fig, ax = plt.subplots()
ax.scatter(xcord0,ycord0, color ='red')
ax.scatter(xcord0,ycord1)
plt.show()
