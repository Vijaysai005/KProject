# usr/bin/env python

"""
Created on Fri Jun 23
@author : Vijayasai S
"""
from timedate import DateMonthYear
from ignitionstatus import IgnitionStatus

def FindingDistance(data):
	dist = [] 
	date, month, year = DateMonthYear(data)
	for index in range(len(data["latitude"])-1):
		if year[index] >= 2017:
			if month[index] >= 6:
				if date[index] >= 9: 
					dist.append(distance(data["latitude"][index], data["latitude"][index+1], \
						data["longitude"][index], data["longitude"][index+1]))
	return sum(dist)

def MaxAvgSpeed(data):
	speed = []
	date, month, year = DateMonthYear(data)
	for index in range(len(data["ground_speed"])):
		if IgnitionStatus(data["ignition_status"][index]) is True:
			if year[index] >= 2017:
				if month[index] >= 6:
					if date[index] >= 9: 
						speed.append(np.float(data["ground_speed"][index]))
	return max(speed)*(10**-2)*(18.0/5.0), np.mean(speed)*(10**-2)*(18.0/5.0)
