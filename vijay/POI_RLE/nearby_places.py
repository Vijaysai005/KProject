#! usr/bin/env python

import googlemaps
import numpy as np
import time

from optparse import OptionParser

def main():
	parser = OptionParser("prog -d <date> -t <time>")
	parser.add_option("-d", "--dat", dest="date")
	parser.add_option("-t", "--tim", dest="time")
	(options,args) = parser.parse_args()
	if options.date == None or options.time == None:
		print parser.usage
	else:
		filename = "POI_more_than_" + str(options.time) + "_minutes/POI_"+ str(options.date) +".csv"
		radius = input("Enter the circle radius of POI: ")		
		nearby(filename,radius)
	return

def nearby(filename,radius):
	with open(filename,"r") as doc:
		lat = [] ; long = []
		count = 0
		for line in doc:
			count += 1
			if count == 1:
				continue
			line = line.split(",")			
			lat.append(float(line[0]))
			long.append(float(line[1]))
	
	gmaps = googlemaps.Client(key = "AIzaSyBs90UUNEoEicdk7Jo5YlATNaJPehCRXdA")
	lat1 = [] ; long1 = []
	for i in range(len(lat)-1):
		nearby = gmaps.places_nearby((lat[i],long[i]), radius)
		for j in range(len(nearby['results'])):
			lat1.append(float(nearby['results'][j]['geometry']['location']['lat'])) 
			long1.append(float(nearby['results'][j]['geometry']['location']['lng']))
	return lat1, long1

if __name__ == "__main__":
	main()
