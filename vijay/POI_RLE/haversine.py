# usr/bin/env python

"""
Created on Fri Jun 23
@author : Vijayasai S
"""

import numpy as np

def haversine(theta):
	return (1 - np.cos((theta))) * 0.5

def distance(lat1, lat2, long1, long2):
	
	radius = 6371.0 # mean radius of the earth (in KM)
	# haversine formula for determining the distance haversine function
	func = (haversine(np.abs(np.radians(np.float(lat1)) - np.radians(np.float(lat2))))) +\
		(np.cos(np.radians(np.float(lat1)))*np.cos(np.radians(np.float(lat2)))*\
			haversine(np.abs(np.radians(np.float(long1)) - np.radians(np.float(long2)))))
	# angle from distance haversine function
	angle = 2.0*np.arctan2(np.sqrt(func), np.sqrt(1-func))
	# distance between the two locations
	distance = radius*angle
	return distance
