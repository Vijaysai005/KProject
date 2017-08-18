# usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 13:15:05 2017

@author: Vijayasai S
"""
# Use python3

from pymongo import MongoClient
from datetime import datetime

from operator import itemgetter
import numpy as np

def TimeInMinutes(hours, minutes, seconds):
	return 60*int(hours) + int(minutes) + (int(seconds) / 60)

def Generate_Alert(ride_id, cluster_instance, threshold_minute):

	"""
	Parameters
    ----------
    ride_id : int, required
        The id number given for particular ride.
    cluster_instance : int, required
        No. of latest cluster instances should be taken.
    threshold_minute : int, required
        The minute required to check whether the biker is outside the
        	cluster or not
	"""

	client = MongoClient("localhost", 27017)
	collection = client.maximus_db.clus

	current_time = datetime(2017,3,26,15,7)

	if ride_id is None:
		items = collection.find({"timestamp":{"$lte":current_time}},{"timestamp":1,"cluster_number":1,"unit_id":1,"latitude":1,"longitude":1,"_id":0}).sort([("timestamp", -1)])
		data = [item for item in items]
		latest_data = sorted(data[:cluster_instance], key=itemgetter('timestamp'))

		try:
			max_cluster = int(max([latest_data[i]["cluster_number"] for i in range(cluster_instance) if latest_data[i]["cluster_number"] != "outlier"]))
		except ValueError:
			max_cluster = 1
		
		FixClus = [[] for i in range(max_cluster)]
		OutClus = {} ; timeFixClus = []

		current_time_stamp = latest_data[0]["timestamp"]
		OutClus[current_time_stamp] = []

		for i in range(cluster_instance):
			
			if latest_data[i]["timestamp"] != current_time_stamp:

				timeFixClus.append(FixClus) 
				try:
					FixClus = [[] for i in range(max_cluster)]
				except ValueError:
					pass
				current_time_stamp = latest_data[i]["timestamp"]
				OutClus[current_time_stamp] = []

			if latest_data[i]["cluster_number"] != "outlier":

				FixClus[latest_data[i]["cluster_number"] - 1].append(latest_data[i]["unit_id"])
				for j in range(max_cluster):
					if j != latest_data[i]["cluster_number"] - 1:
						try:
							FixClus[j].remove(latest_data[i]["unit_id"])
						except ValueError:
							pass
			
			if latest_data[i]["cluster_number"] == "outlier":
				OutClus[current_time_stamp].append(latest_data[i]["unit_id"])

		timeFixClus.append(FixClus)
		current_time_stamp = latest_data[0]["timestamp"]
		
		for i in range(cluster_instance):
			if latest_data[i]["timestamp"] != current_time_stamp:
				
				diff = abs(current_time_stamp - latest_data[i]["timestamp"])
				diff = TimeInMinutes(str(diff)[0:1], str(diff)[2:4], str(diff)[5:7])
				for l in range(len(OutClus[current_time_stamp])):
					
					sum_min = 0 ; PreClus = 1
					for m in range(len(timeFixClus)):
						for n in range(max_cluster):
							if OutClus[current_time_stamp][l] in timeFixClus[m][n]:
								sum_min += diff
								PreClus = n + 1
										
					if sum_min >= threshold_minute:
						print ("Alert:",OutClus[current_time_stamp][l],"is outside of cluster ",PreClus)

				current_time_stamp = latest_data[i]["timestamp"]		
		
if __name__ == "__main__":
	Generate_Alert(None, 10, 1)



